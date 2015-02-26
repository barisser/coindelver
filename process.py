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
        result['inputs'] = result['inputs'] + inputters
        for out in tx['outputs']:
            if 'addr' in out:
                output_address = out['addresses'][0]
                if output_address == public_address:
                    to_me = True
                else:
                    if not output_address in outputees:
                        outputees.append(output_address)
        result['outputs'] = result['outputs'] + outputees
    return result

def addresses_txs_local(public_address, parent):
    result = {}
    result['inputs'] = addresses_backwards_local(public_address)
    result['outputs'] = addresses_forward_local(public_address)

    a=[]
    for x in result['inputs']:
        if not x==parent:
            b=searchAddress(x, public_address)
            a.append(b)
        else:
            print "Intercepted PARENT "+str(parent)
    q=[]
    for x in result['outputs']:
        if not x==parent:
            c=searchAddress(x, public_address)
            q.append(c)
        else:
            print "Intercepted Parent "+str(parent)
    result['inputs'] = a
    result['outputs'] = q

    return result

def scoring_equation(generations, occurrences, other_multiplier):
    weight = 1.0 / float(generations) * math.pow(2, occurrences) * other_multiplier
    return weight

def assign_weights(source_address, other_address, generations, occurrences, other_multiplier):
    weight = scoring_equation(generations, occurrences, other_multiplier)
    connect_addresses(other_address, source_address, weight)

class searchAddress:
    def __init__(self, public_address, parent_address):
        self.public_address = public_address
        self.parent_address = parent_address

def iterate_once(all_generations, last_score_set, appearance_count, limit_n): #not the first time here
    last_generation = all_generations[len(all_generations)-1]  #list of searchAddress objects
    parents = {}   #NEEDS WORK HERE
    for y in last_generation:
        parents[y.public_address] = y.parent_address
    last_generation_scores = {}
    for x in last_generation:
        last_generation_scores[x.public_address] = last_score_set[x.public_address]
    top_few = sorted(last_generation_scores, key=last_generation_scores.get)[::-1]
    gen=[]
    if len(top_few)<limit_n:
        k=0 #do nothing
    else:
        top_few = top_few[0:limit_n]
    for x in top_few:
        parent = ""
        if x in parents:
            parent = parents[x]  #NEEDS WORK HERE
            print "PARENT "+str(parent)
        r = addresses_txs_local(x, parent)   #NEEDS WORK HERE< NOT EVEN SURE IF PARENT THING IS WORKING
        neighbors = r['inputs'] + r['outputs']
        gen = gen + neighbors
        #add to scoreset
        for y in neighbors:
            if y.public_address in appearance_count:
                appearance_count[y.public_address] += 1
            else:
                appearance_count[y.public_address] = 1
            #MAKE THIS MORE EFFICIENT?
            last_score_set[y.public_address] = scoring_equation(len(all_generations), appearance_count[y.public_address], 1.0)
    all_generations.append(gen)
    return all_generations, last_score_set, appearance_count


def correlations(public_address, n, limit_n):
    score = {}
    generations = [] #running tally non-scored
    appearance = {}
    for i in range(n):
        if i>0:
            a = iterate_once(generations, score, appearance, limit_n)
            generations = a[0]
            score = a[1]
            appearance = a[2]
        else:
            r = addresses_txs_local(public_address, '')
            r=r['inputs']+r['outputs']
            generations.append(r)
            for x in r:
                if x.public_address in appearance:
                    appearance[x.public_address] += 1
                else:
                    appearance[x.public_address] = 1
            for k, v in appearance.iteritems():
                score[k] = scoring_equation(1, v, 1.0)
    return score, generations, appearance

def address_blacklisted(public_address):
    r = db.dbexecute("select count(*) from blacklisted_addresses where public_address='""+str(public_address)+';",True)
    if r[0][0] > 0:
        return True
    else:
        return False

def addresses_at_n(public_address, n):
    result=[]
    for i in range(n):
        if i>0:
            addrs = result[i-1]
            newaddrs = []
            for addr in addrs:
                r=addresses_txs_local(addr.public_address, addr.parent_address)
                newaddrs = newaddrs + r['inputs'] + r['outputs']
            result.append(newaddrs)
        else:
            q=addresses_txs_local(public_address, "")
            e=q['outputs'] + q['inputs']
            result.append(e)
    return result

def delete_address_correlations_on_address(public_address):
    db.dbexecute("delete from address_address_correlation * where from_address='"+str(public_address)+"';",False)

def get_temporary_address_correlations(public_address, depth):
    a = record_address_correlations(public_address, depth)
    delete_address_correlations_on_address(public_address)
    return a

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
    #txs = list(set(txs)) #removes duplicates from db saving errors
    return txs

def downstream_txs_on_address(public_address):
    dbstring = "select * from inputs where public_address='"+str(public_address)+"';"
    results = db.dbexecute(dbstring, True)
    txs = []
    if len(results)>0:
        for x in results:
            txs.append(x[1])
    #txs = list(set(txs)) #removes duplicates from db saving errors
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

def write_header(height):
    n = bitcoind.connect("getblockhash", [height])
    db.add_header(n, '', height)

def write_headers(j):
    n = bitcoind.connect("getblockcount", [])
    m = db.last_header()

    if n - m > j:
      r = j
    else:
      r = n-m

    for i in range(m + 1, m+r):
      write_header(i)
      print "wrote header: "+str(i)
