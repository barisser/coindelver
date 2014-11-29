import db

class Transactions:
    def __init__(self, txdata):
        self.txdata = txdata
        self.txhash = txdata['hash']
        self.inputs = txdata['inputs']
        self.outputs = txdata['out']
