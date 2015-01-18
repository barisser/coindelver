import bitcoind
import db
import math

def all_txs_on_address(public_address):
        txs = bitcoind.get_address_info_chain(public_address)
        return txs

def connect_addresses(from_address, to_address, weight):
    dbstring = "select * from address_address_correlation where from_address='"+str(from_address)+"' and to_address='"+str(to_address)+"';"
    result = db.dbexecute(dbstring, True)
    if len(result) > 0:
        current_weight = result[0][2]
        new_weight = float(current_weight) + weight
        dbstring = "update address_address_correlation set weight = '"+str(new_weight)+"' where from_address='"+str(from_address)+"' and to_address='"+str(to_address)+"';"
    else:
        dbstring = "insert into address_address_correlation values ('"+str(from_address)+"', '"+str(to_address)+"', '"+str(weight)+"');"
    db.dbexecute(dbstring, False)

def addresses_txs(public_address):
    txs = all_txs_on_address(public_address)
    result = {}
    result['inputs'] = []
    result['outputs'] = []
    for tx in txs:
        from_me = False
        to_me = False
        inputters = []
        outputees = []
        for inp in tx['inputs']:
            if 'addresses' in inp:
                input_address = inp['addresses'][0]
                if input_address == public_address:
                    from_me = True
                else:
                    if not input_address in inputters:
                        inputters.append(input_address)
        if not from_me:
            result['inputs'] = result['inputs'] + inputters
        for out in tx['outputs']:
            if 'addr' in out:
                output_address = out['addresses'][0]
                if output_address == public_address:
                    to_me = True
                else:
                    if not output_address in outputees:
                        outputees.append(output_address)
        if not to_me:
            result['outputs'] = result['outputs'] + outputees
    return result

def addresses_txs_local(public_address):
    result = {}
    result['inputs'] = addresses_backwards_local(public_address)
    result['outputs'] = addresses_forward_local(public_address)

    a=[]
    for x in result['inputs']:
        b=searchAddress(x, public_address)
        a.append(b)
    q=[]
    for x in result['outputs']:
        c=searchAddress(x, public_address)
        q.append(c)
    result['inputs'] = a
    result['outputs'] = q
    return result

def assign_weights(source_address, other_address, generations, occurrences, other_multiplier):
    weight = 1.0 / float(generations) * math.pow(2, occurrences) * other_multiplier
    connect_addresses(other_address, source_address, weight)

class searchAddress:
    def __init__(self, public_address, parent_address):
        self.public_address = public_address
        self.parent_address = parent_address

def addresses_at_n(public_address, n):
    result=[]
    for i in range(n):
        if i>0:
            addrs = result[i-1]
            for addr in addrs:
                newaddrs = []
                r=addresses_txs_local(addr.public_address)
                caddrs = r['inputs'] + r['outputs']
            result.append(caddrs)
        else:
            q=addresses_txs_local(public_address)
            e=q['outputs'] + q['inputs']
            result.append(e)
    return result



def record_address_correlations(public_address, n):
    data = addresses_at_n(public_address, n)
    i=1
    for gen in data:
        addresses = {}
        for x in gen:
            addresses[x] = gen.count(x)
        for y in addresses:
            scalar = 1.0
            assign_weights(y.public_address, public_address, i, addresses[y], scalar)
        print i
        i=i+1
    return get_address_vector(public_address)

def get_address_vector(public_address):
    dbstring = "select * from address_address_correlation where from_address='"+str(public_address)+"' order by weight desc;"
    result = db.dbexecute(dbstring, True)
    vector = []
    m=0
    if len(result)>0:
        for x in result:
            vector.append([x[1], x[2]])
            m=m+math.pow(x[2],2)
    # m=math.pow(m, 0.5)
    # if m>0:
    #     for i in range(len(vector)):
    #         vector[i][1] = vector[i][1] / m
    return vector

def upstream_txs_on_address(public_address):
    dbstring = "select * from outputs where public_address='"+str(public_address)+"';"
    results = db.dbexecute(dbstring, True)
    txs = []
    if len(results)>0:
        for x in results:
            txs.append(x[1])
    txs = list(set(txs)) #removes duplicates from db saving errors
    return txs

def downstream_txs_on_address(public_address):
    dbstring = "select * from inputs where public_address='"+str(public_address)+"';"
    results = db.dbexecute(dbstring, True)
    txs = []
    if len(results)>0:
        for x in results:
            txs.append(x[1])
    txs = list(set(txs)) #removes duplicates from db saving errors
    return txs

def addresses_forward_local(public_address):
    txs = downstream_txs_on_address(public_address)
    addresses = []
    for tx in txs:
        dbstring = "select * from outputs where txhash='"+str(tx)+"';"
        r = db.dbexecute(dbstring, True)
        if len(r)>0:
            for x in r:
                addresses.append(x[0])
    return addresses

def addresses_backwards_local(public_address):
    txs = upstream_txs_on_address(public_address)
    addresses = []
    for tx in txs:
        dbstring = "select * from inputs where txhash='"+str(tx)+"';"
        r = db.dbexecute(dbstring, True)
        if len(r)>0:
            for x in r:
                addresses.append(x[0])
    return addresses
