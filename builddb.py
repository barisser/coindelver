import bitcoind
import db

while True:
    last_block_meta = db.dbexecute("select * from meta;", True)
    last_block_meta = last_block_meta[0][0]

    last_block_node = bitcoind.connect("getblockcount". [])

    if last_block_meta < last_block_node-100:
        bitcoind.save_next_blocks(100)
