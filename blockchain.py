import bitcoind
import db

def download_block_chain(height):
    api_url = "/blocks/"+str(height)+"?api"
