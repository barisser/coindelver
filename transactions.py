import bitcoind
import blocks
import util
import hashlib
import headers
import pybitcointools
import saved
import identity

def get_raw_tx(txhash):
  return bitcoind.connect("getrawtransaction", [txhash])

def txhash_from_raw(rawtx):
  r=rawtx.decode('hex')
  r=hashlib.sha256(r).digest()
  r=hashlib.sha256(r).hexdigest()
  r=r.decode('hex')
  r=r[::-1].encode('hex')
  return r

def verify_merkle(height, txhash):  #FEED IN A KNOWN HASH
  hash = saved.find_hash(height)
  blockhash= hash.hash
  previous_block_hash=hash.previoushash
  theblock = blocks.get_block_from_hash(blockhash)
  version = theblock['version']
  merkleroot = util.merkle(theblock['tx'])
  bits = int(theblock['bits'],16)  #NEED BETTER WAY OF TRACKING THIS
  time = theblock['time']
  nonce = theblock['nonce']

  header = headers.construct_header(version, previous_block_hash, merkleroot, time, bits, nonce)
  newblockhash = header[0]
  veracity = header[1]

  tx_in_merkle=False
  if txhash in theblock['tx']:
    tx_in_merkle = True

  if veracity==True and tx_in_merkle==True:
    return True, txhash
  else:
    return False, ''

def verify_tx(txhash, height):
  merkleresponse = verify_merkle(height, txhash)
  if merkleresponse[0]:
    #Txhash is in merkle root in block (assuming known block hashes)

    #verify that raw tx matches txhash in merkle root
    rawtx = get_raw_tx(txhash)
    calculated_tx_hash = txhash_from_raw(rawtx)

    if calculated_tx_hash == txhash:
      #pulled raw tx data is correct
      jsontx = pybitcointools.deserialize(rawtx)
      return jsontx
    else:
      return {}
  else:
    return {}


def check_for_special_output(height, txhash, special_output, special_output_index):
  jsontx = verify_tx(txhash, height)

  if 'ins' in jsontx:
    inputs = jsontx['ins']
    outputs = jsontx['outs']

    special_output_in_tx=False
    special_output_position=-1
    n=0
    for x in inputs:
      if x['outpoint']['hash'] == special_output and x['output']['index']==special_output_index:
        #this is is
        special_output_in_tx=True
        special_output_position=n
      else:
        n=n+1
    if special_output_in_tx:
      newoutput = txhash
      newoutput_index = special_output_position
  
