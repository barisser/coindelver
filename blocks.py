import requests
import json

import util
import bitcoind
import headers
import saved

prev_genesis_hash='0000000000000000000000000000000000000000000000000000000000000000'
genesis_hash='000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'

def get_block_count():
  return bitcoind.connect('getblockcount',[])

def get_best_block_hash():
  return bitcoind.connect('getbestblockhash', [])

def get_block_from_hash(blockhash):
  return bitcoind.connect('getblock',[blockhash])

def check_block_legitimacy(blockhash, previous_block_hash, version):
  theblock = get_block_from_hash(blockhash)
  merkleroot = util.merkle(theblock['tx'])
  bits = int(theblock['bits'],16)  #NEED BETTER WAY OF TRACKING THIS
  time = theblock['time']
  nonce = theblock['nonce']

  header = headers.construct_header(version, previous_block_hash, merkleroot, time, bits, nonce)
  newblockhash = header[0]
  veracity = header[1]

  if header[1]:
    return veracity, newblockhash
  else:
    return veracity, ""

def backtrace_blocks(known_block_hashes, proposed_block_hash, maximum_attempts):
  lasthash= proposed_block_hash
  hashes_seen=[]
  connected=False

  n=0
  if proposed_block_hash in known_block_hashes:
    return True, []
  else:

    cont=True
    while n<maximum_attempts and cont==True:
        proposed_block = get_block_from_hash(lasthash)

        if proposed_block == None:
          cont=False
          print "Block Not Found for hash "+str(lasthash)
          return False, []
        else:

          previous_hash = proposed_block['previousblockhash']

          legit=check_block_legitimacy(lasthash, previous_hash, 2)[0]  #VERSION IS HARDCODED
          if legit:
            hashes_seen.append(lasthash)
            print "seen lasthash "+str(lasthash)
            if previous_hash in known_block_hashes:
              connected=True
              print "Found that it is connected after "+str(len(hashes_seen))+" blocks"
              return connected, hashes_seen
            else:  #continue backtracing
              n=n+1
              lasthash = previous_hash


          else:
            cont=False
            return connected, []

    if n>=maximum_attempts:
      return False, []

def get_next_block(current_block_hash):
  current_block = get_block_from_hash(current_block_hash)
  current_height = current_block['height']
  print current_height
  version = current_block['version']

  if 'nextblockhash' in current_block:
    proposed_next_block_hash = current_block['nextblockhash']

    legit = check_block_legitimacy(proposed_next_block_hash, current_block_hash, version)

    if legit[0]==False:
      if version ==1:
        version = 2
      else:
        version=1
      legit = check_block_legitimacy(proposed_next_block_hash, current_block_hash, version)

    if legit[0]:
      #new block is legitimacy
      #add to db
      return True, proposed_next_block_hash
    else:
      return False, ''
  else:
    return False, ''


def build_block(last_block):
  newblocks=[]
  print last_block.hash
  last_block_hash = last_block.hash
  last_block_height = last_block.height

  nextblock = get_next_block(last_block_hash)
  if nextblock[0]:
    new_block_hash = nextblock[1]
    new_block = saved.hash(new_block_hash, last_block_hash, None, last_block_height+1)
  return new_block

def build_blocks(blockn):
  block_hashes = saved.load_last_n_hashes(1000)
  last_block = block_hashes[len(block_hashes)-1]
  newblocks=[]
  for i in range(0,blockn):
    last_block = build_block(last_block)
    newblocks.append(last_block)
  saved.add_hashes(newblocks)
  saved.stitch()
  return newblocks


#knownblocks=['00000000000000001e1b83860b3556cbc1f14d5f95dbc3a7c5a92b20bf6a81fa']
#r=backtrace_blocks(knownblocks, '00000000000000001dae13213912e2f8c3ba01002006969f0101683694f7a5ec', 10)
#r=check_block_legitimacy('00000000000000000bcfe28b1e0d16448ac86672e9d3fc99e7b87f312061b386', '000000000000000016cf7b4df4a1f955c5714f57e2991112b35ec7dee674b722',2)
