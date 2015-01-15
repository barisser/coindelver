import db
import bitcoind

class Transaction:
    def __init__(self, txhash, height):
        self.txhash = txhash
        self.height = height

    def save(self):
        dbstring = "insert into transactions values ('"+str(txhash)+"','"+str(height)+"');"
        db.dbexecute(dbstring, False)

    def load(self):
        dbstring = "select * from transactions where txhash = '"+str(self.txhash)+"';"
        result = db.dbexecute(dbstring, True)
        if len(result) > 0:
            self.txhash = result[0][0]
            self.height = result[0][1]
