import os
#100 BYTES PER HASH, 32 current hash, 32 previous, 32 next, 4 height

hashes_to_store=1000

class hash:
  def __init__(self, hash, previoushash, nexthash, height):
    self.hash=hash
    self.previoushash=previoushash
    self.nexthash=nexthash
    self.height=height

def load_last_n_hashes(n):
  filename='blockhashes.txt'
  filesize = os.path.getsize(filename)
  lines = filesize / 200

  file = open(filename, 'r+b')
  results=[]
  start = lines - n
  for i in range(start,lines):
    file.seek(i*200)
    buffhash_current = file.read(64)
    buffhash_prev = file.read(64)
    buffhash_next = file.read(64)
    if buffhash_next == "9"*64:
      buffhash_next = None
    buffhash_height = int(file.read(8))
    newhash = hash(buffhash_current, buffhash_prev, buffhash_next, buffhash_height)
    results.append(newhash)
  file.close()
  return results

def find_hash(height):   #WORKS IF ALL BLOCKHASHES STORED IN FILE
                          #ASSUMES BLOCKS ARE IN ORDER WITH NO ERRORS IN ORDER
  filename='blockhashes.txt'
  filesize = os.path.getsize(filename)
  lines = filesize / 200

  file = open(filename, 'r+b')
  results=[]
  i = height
  file.seek(i*200)
  buffhash_current = file.read(64)
  buffhash_prev = file.read(64)
  buffhash_next = file.read(64)
  if buffhash_next == "9"*64:
    buffhash_next = None
  buffhash_height = int(file.read(8))
  newhash = hash(buffhash_current, buffhash_prev, buffhash_next, buffhash_height)
  return newhash

def load_hashes():
  filename='blockhashes.txt'
  filesize = os.path.getsize(filename)
  lines = filesize / 200

  file = open(filename, 'r+b')
  results=[]
  for i in range(0,lines):
    file.seek(i*200)
    buffhash_current = file.read(64)
    buffhash_prev = file.read(64)
    buffhash_next = file.read(64)
    if buffhash_next == "9"*64:
      buffhash_next = None
    buffhash_height = int(file.read(8))
    newhash = hash(buffhash_current, buffhash_prev, buffhash_next, buffhash_height)
    results.append(newhash)
  file.close()
  return results

def add_hashes(hashes):
  filename='blockhashes.txt'
  file = open(filename, 'rb+')

  file.seek(-72,2)
  file.write(bytes(hashes[0].hash))
  file.seek(0,2)

  data_to_write=''
  for hash in hashes:
    current_hash = hash.hash
    prev_hash = hash.previoushash
    next_hash = hash.nexthash
    if next_hash== None:
      next_hash = "9"*64
    height = hash.height
    height = '0'*(8-len(str(height)))+str(height)
    newstuff=str(current_hash) + str(prev_hash) + str(next_hash)+ height
    print newstuff
    data_to_write= data_to_write+str(current_hash) + str(prev_hash) + str(next_hash)+ height

  data_to_write=bytes(data_to_write)
  file.write(data_to_write)
  file.close()

def stitch():
  filename='blockhashes.txt'
  filesize = os.path.getsize(filename)
  lines = filesize / 200

  file = open(filename, 'rb+')

  file.seek(64)
  previous_next_hash = file.read(64)

  for i in range(1,lines):
    file.seek(i*200)
    thishash = file.read(64)
    if previous_next_hash=="9"*64:
      #change previous hash to this hash
      file.seek((i-1)*200+64*2)
      file.write(bytes(thishash))

    file.seek(i*200+64*2)
    previous_next_hash = file.read(64)

  file.close()

def save_hashes(hashes):
  filename='blockhashes.txt'
  file = open(filename, 'wb')

  data_to_write=''
  for hash in hashes:
    current_hash = hash.hash
    prev_hash = hash.previoushash
    next_hash = hash.nexthash
    if next_hash== None:
      next_hash = "9"*64
    height = hash.height
    height = '0'*(8-len(str(height)))+str(height)
    newstuff=str(current_hash) + str(prev_hash) + str(next_hash)+ height
    print newstuff
    data_to_write= data_to_write+str(current_hash) + str(prev_hash) + str(next_hash)+ height

  data_to_write=bytes(data_to_write)
  file.write(data_to_write)
  file.close()


a=hash('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f', '0000000000000000000000000000000000000000000000000000000000000000', None, 0)
