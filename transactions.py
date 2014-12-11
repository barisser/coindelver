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
        self.maintain_outputs_addresses_new_persons()
        self.check_for_mining_transactions()
        self.merge_identities_many_inputs()
        self.pass_on_inputs_correlations()
        self.inherit_upstream_correlations()

    def get_my_correlations():
        correlations = []
        for input in self.inputs:
            previous_output = Outputs("")

    def pass_on_inputs_correlations():


    def inherit_upstream_correlations():

    def maintain_outputs_addresses_new_persons(self):
        if 'prev_out' in self.inputs[0]: #make sure its not a mining transaction
            for output in self.outputs:
                #add output to db
                output_id = self.txhash+":"+str(output['n'])
                destination_address = output['addr']
                #check for existing person_id destination pair
                found_addresses = db.dbexecute("select * from addresses where public_address='"+str(destination_address)+"';",True)
                if len(found_addresses)>0:
                    person_id = found_addresses[0][1]
                else:
                    person_id = other.generate_new_id()
                    db.add_person(person_id, '', self.height)
                    db.add_address(destination_address, person_id, '')

                db.add_output(output_id, person_id, self.txhash, str(output['n']), '', output['spent'], output['value'], 'standard', output['addr'])


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
