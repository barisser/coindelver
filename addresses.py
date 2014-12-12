import db
import people
import bitcoind

def link_addresses(addresses):
    person_ids = []
    for address in addresses:
        person_id = db.dbexecute("select addresses.person_id from addresses inner join people on addresses.person_id = people.person_id where addresses.public_address='"+str(address)+"' order by people.firstblock asc;", True)
        if len(person_id)>0:
            person_ids.append(person_id[0][0])

    if len(person_ids)>1:
        cloned_into = person_ids[0]
        people.merge_people(person_ids, cloned_into) #merging with first arbitrarily


class Address:
    def __init__(self, public_address):
        self.public_address = public_address
        self.person_id = '-1'

        #self.outputs = []
        #outputs = db.dbexecute("select * from outputs where destination_address='"+str(public_address)+"';", True)
        #for output in outputs:
        #    self.outputs.append(output[0])

    def load(self):
        dbstring = "select * from addresses where public_address='"+str(public_address)+"';"
        result = db.dbexecute(dbstring, True)
        if len(result) > 0:
            self.public_address=result[0][0]
            self.person_id = result[0][1]

    def save(self):
        exists = False
        dbstring = "select * from addresses where public_address='"+str(public_address)+"';"
        result = db.dbexecute(dbstring, True)
        if len(result) > 0:
            exists=True

        if exists:
            dbstring = "update addresses set person_id='"+str(self.person_id)+"';"
            db.dbexecute(dbstring, False)
        else:
            dbstring = "insert into addresses values ('"+str(self.public_address)+"', '"+str(self.person_id)+"', '"+str(self.bitcoin_id)+"');"
            db.dbexecute(dbstring, False)

    def all_txs(self):
        txs = bitcoind.get_address_info_blockchaininfo(self.public_address)['txs']
        return txs

    def outgoing_transactions(self, txs):  #named right
        incoming_txs = [] #named wrong
        for tx in txs:
            incoming = False
            for input in tx['inputs']:
                if 'prev_out' in input:
                    if 'addr' in input['prev_out']:
                        source_address = input['prev_out']['addr']
                        if source_address == self.public_address:
                            incoming=True
            if incoming:
                incoming_txs.append(tx)
        return incoming_txs

    def incoming_transactions(self, txs):
        outgoing_txs = []  #named wrong
        for tx in txs:
            outgoing = False
            for output in tx['out']:
                if 'addr' in output:
                    if output['addr'] == self.public_address:
                        outgoing=True


            # #dont count if sent back to self
            # for input in tx['inputs']:  #if one of the senders is ME, dont count this
            #     if 'prev_out' in input:
            #         if 'addr' in input['prev_out']:
            #             if input['prev_out']['addr'] == self.public_address:
            #                 outgoing=False
            if outgoing:
                outgoing_txs.append(tx)
        return outgoing_txs
        
