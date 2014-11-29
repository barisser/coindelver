import bitcoind
import db

def get_txs(height):
  blockdata = bitcoind.get_block_blockchaininfo(height)
  return blockdata['tx']
