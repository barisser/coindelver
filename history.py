import db

def downstream_txs(txhash):
    results = db.select_tx_output(txhash)
    txs = []
    for x in results:
        if x[2]:
            txs.append([x[3], x[1], x[6]])
    return txs

def sum_inputs_txhash(txhash):
    results = db.dbexecute("select sum(amount) from tx_outputs where spent_at_txhash='"+str(txhash)+"';", True)
    return results[0][0]

def process_children(parent_txhash, parent_index, parent_amount):
    results = db.dbexecute("select * from tx_outputs where txhash='"+str(parent_txhash)+"' and index='"+str(parent_index)+"';", True)
    children  = []
    for x in results:
        child = {}
        child['parent_txhash'] = parent_txhash
        child['parent_index'] = parent_index
        children.append([x[3], x[1], x[6]])



def downstream(txhash, generations_n):
    first_generation = []
    first_tx = db.select_tx_output(txhash)
    for tx in first_tx:
        tx_object = {}
        tx_object['parent'] = txhash
        tx_object['txhash'] = tx[3]
        tx_object['index'] = tx[1]
        tx_object['amount'] = tx[6]/100000000
        tx_object['children'] = []
        first_generation.append(tx_object)

    for x in first_generation:


def downstream_history(txhash, generations_n):
    generations = []
    first_tx = db.select_tx_output(txhash)

    for x in first_tx:
        first_generation.append([x[3], x[1], x[6]/100000000])
    generations.append(first_generation)

    for i in range(generations_n):
        new_generation = []
        for tx in generations[len(generations)-1]:
            txhash = tx[0]
            tx_index = tx[1]
            tx_amount = tx[2]/100000000

            downstream = downstream_txs(txhash)
            #modify amounts on downstream txs by proportion coming from original
            modifier = tx[2] / sum_inputs_txhash(txhash)  #fraction of this tx's inputs that came from previous output
            print modifier
            for i in range(len(downstream)):
                downstream[i][2] = downstream[i][2] * modifier
            new_generation = new_generation + downstream
        generations.append(new_generation)
    return generations
