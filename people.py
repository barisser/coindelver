import db
import bitcoind
import addresses

def merge_people(person_ids, cloned_person_id):
    for person_id in person_ids:
        dbstring = "update addresses set person_id = '"+str(cloned_person_id)+"' where person_id ='"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        dbstring = "update outputs set person_id = '"+str(cloned_person_id)+"' where person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        dbstring = "update correlations set from_person_id = '"+str(cloned_person_id)+"' where from_person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)
        dbstring = "update correlations set to_person_id = '"+str(cloned_person_id)+"' where to_person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        dbstring = "delete from people * where person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        #merge duplicate rows in correlations table
        #TO DO


class Person:
    def __init__(self, person_id):
        self.person_id = person_id
        self.name = ''

    def load(self): #creates new entry if not found
        dbstring = "select * from people where person_id = '"+str(self.person_id)+"';"
        person_info = db.dbexecute(dbstring, True)
        if len(person_info)>0:
            self.name = person_info[0][1] #there should never be more than one entry
            self.firstblock = person_info[0][2]
        else:
            dbstring = "insert into people values ('"+str(self.person_id)+"', '"+str(self.name)+"', -1);"
            db.dbexecute(dbstring, False)

    def addresses(self):
        dbstring = "select public_address from addresses where person_id='"+str(self.person_id)+"';"
        addresses = db.dbexecute(dbstring, True)
        results = []
        for address in addresses:
            results.append(address[0])
        return results

    def txs_relevant_to_person(self):
        addresses = self.addresses()
        txs = []
        for address in addresses:
            txs.append([address, bitcoind.get_address_info_blockchaininfo(address)['txs']])
        return txs

    def incoming_transactions(self, txs):
        incoming = []
        for x in txs:
            address = addresses.Address(x[0])
            tx_set = x[1]
            incoming = incoming + address.incoming_transactions(tx_set)
            del address
        return incoming

    def outgoing_transactions(self, txs):
        outgoing = []
        for x in txs:
            address = addresses.Address(x[0])
            tx_set = x[1]
            outgoing = outgoing + address.outgoing_transactions(tx_set)
            del address
        return outgoing
