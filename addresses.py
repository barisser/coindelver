import db
import bitcoind

class Address:
    def __init__(self, public_address):
        self.public_address = public_address

    def load(self):
        dbstring = "select * from addresses where public_address='"+str(self.public_address)+"';"
        result = db.dbexecute(dbstring, True)
        if len(result) > 0:
            self.public_address=result[0][0]

    def save(self):
        exists = False
        dbstring = "select * from addresses where public_address='"+str(self.public_address)+"';"
        result = db.dbexecute(dbstring, True)
        if len(result) > 0:
            exists=True

        if exists:
            k=0 #update something
        else:
            dbstring = "insert into addresses values ('"+str(self.public_address)+"');"
            db.dbexecute(dbstring, False)


def txs_pertaining_to_address(address):
    inputted = db.dbexecute("select * from inputs where public_address='"+str(address)+"';", True)
    outputted = db.dbexecute("select * from outputs where public_address='"+str(address)+"';", True)
    txs = []
    for tx in inputted:
        txs.append(tx[1])
    for tx in outputted:
        txs.append(tx[1])
    return txs
