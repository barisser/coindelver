import bitcoind
import db
import transactions

class Blocks:
    def __init__(self, height):
        self.height = height
        self.txdata = ''

    def download_data(self):
        blockdata = bitcoind.get_block_blockchaininfo(height)
        self.txdata = blockdata['tx']

    def process(self):
        #process stuff here
        for tx_data in self.txdata:
            tx = Transactions(tx_data)
            tx.process()
            del r
