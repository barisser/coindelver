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

def assign_weights(source_address, other_address, generations, occurrences):
    weight = 1.0 / float(generations) * math.pow(2, occurrences)
    connect_addresses(other_address, source_address, weight)

def addresses_at_n(public_address, n):
    result = []

    for i in range(n):
        if i>0:
            out_addrs = result[i-1]['outputs']  #predecessors
            in_addrs = result[i-1]['inputs']
            new_generation = {}
            new_generation['inputs'] = []
            new_generation['outputs'] = []

            for out in out_addrs:
                new_outs = addresses_txs(out)['outputs']
                new_generation['outputs'] = new_generation['outputs'] + new_outs

            for inp in in_addrs:
                new_ins = addresses_txs(inp)['inputs']
                new_generation['inputs'] = new_generation['inputs'] + new_ins
        else:
            new_generation = addresses_txs(public_address)
        result.append(new_generation)
    return result

def record_address_correlations(public_address, n):
    data = addresses_at_n(public_address, n)
    i=1
    for gen in data:
        inputzers = {}
        outputzers = {}
        for x in set(gen['inputs']):
            inputzers[x] = gen['inputs'].count(x)
        for x in set(gen['outputs']):
            outputzers[x] = gen['outputs'].count(x)

        for inp in inputzers:
            assign_weights(inp, public_address, i, inputzers[inp])
        for out in outputzers:
            assign_weights(out, public_address, i, outputzers[out])
        print i
        i=i+1

def get_address_vector(public_address):
    dbstring = "select * from address_address_correlation where from_address='"+str(public_address)+"' order by weight desc;"
    result = db.dbexecute(dbstring, True)
    vector = []
    m=0
    if len(result)>0:
        for x in result:
            vector.append([x[1], x[2]])
            m=m+math.pow(x[2],2)
    m=math.pow(m, 0.5)
    if m>0:
        for i in range(len(vector)):
            vector[i][1] = vector[i][1] / m
    return vector
