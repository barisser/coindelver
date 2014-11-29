import db
import other
import addresses
import people

class Transactions:
    def __init__(self, txdata, height):
        self.txdata = txdata
        self.txhash = txdata['hash']
        self.inputs = txdata['inputs']
        self.outputs = txdata['out']
        self.height = height

    def process(self):
        #all processing occurs here
        self.check_for_mining_transactions()
        self.merge_identities_many_inputs()

    def check_for_mining_transactions(self):
        if not 'prev_out' in self.inputs[0]:
            #then it is a mining transaction
            receiving_address = self.outputs[0]['addr']

            #check if receiving address already exists in address db
            found_addresses = db.dbexecute("select * from addresses where public_address='"+str(receiving_address)+"';", True)
            if len(found_addresses) > 0:
                person_id = found_addresses[0][1]
            else:
                #if no, add new address entry,  also add new person entry
                person_id = other.generate_new_id()
                db.dbexecute("insert into people values ('"+str(person_id)+"', '', "+str(self.height)+");", False)

                dbstring = "insert into addresses values ('"+str(receiving_address)+"', '"+str(person_id)+"', '');"
                db.dbexecute(dbstring, False)

            #create output
                #assign person id to this output
            transaction_hash = self.txhash
            output_index = self.outputs[0]['n']
            bitcoin_id = ''
            spent = self.outputs[0]['spent']
            value = self.outputs[0]['value']
            type = "mining"
            output_id = transaction_hash + ":0"
            destination_address = receiving_address
            db.add_output(output_id, person_id, transaction_hash, output_index, bitcoin_id, spent, value, type, destination_address)

    def merge_identities_many_inputs(self):
        if len(self.inputs)>1:
            ins = []
            for tx in self.inputs:
                if 'prev_out' in tx:
                    ins.append(tx['prev_out']['addr'])
            addresses.link_addresses(ins)
