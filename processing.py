import bitcoind
import db
import random
import hashlib

def get_txs(height):
  blockdata = bitcoind.get_block_blockchaininfo(height)
  return blockdata['tx']

def generate_new_id():
  return hashlib.sha256(str(random.random())).hexdigest()

def assign_new_id_to_mined(tx, height):
  if not 'prev_out' in tx['inputs'][0]:
    receiving_address = tx['out'][0]['addr']
    #check if address already exists
    dbstring = "select * from addresses where public_address='"+str(receiving_address)+"';"
    found = db.dbexecute(dbstring, True)
    if len(found)==0:  #create new address in DB since this one hasnt been seen before
      the_id = generate_new_id()
      dbstring = "insert into people (person_id, firstblock) values ('"+str(the_id)+"', "+str(height)+");"
      print dbstring
      db.dbexecute(dbstring, False)
      dbstring = "insert into addresses (public_address, person_id) values ('"+str(receiving_address)+"', '"+str(the_id)+"');"
      print dbstring
      db.dbexecute(dbstring, False)

def link_inputs(tx, height):
  ins = []
  for x in tx['inputs']:
    if 'prev_out' in x:
      ins.append(x['prev_out']['addr'])
  link_addresses(ins, height)

def link_inputs_in_block(height, txs):
  for tx in txs:
    link_inputs(tx, height)

def mined_tx_in_block(txs, height):
  for tx in txs:
    if not 'prev_out' in tx['inputs'][0]:
      assign_new_id_to_mined(tx, height)

def process_block(height):
  txs = get_txs(height)
  link_inputs_in_block(height, txs)
  mined_tx_in_block(txs, height)

def process_blocks_in_range(start_height, last_height):
  for i in range(start_height, last_height+1):
    process_block(i)
    print "processed block "+str(i)


def link_addresses(address_list, block_height):
  known_ids = []

  if len(address_list)>0:
    for addr in address_list:  #CHECK HOW MANY ARE KNOWN, if more than 1 do nothing
      found_id = db.dbexecute("select person_id from addresses where public_address='"+str(addr)+"';", True)
      print found_id
      if len(found_id)>0:
        known_ids.append(found_id[0][0])
      else:
        dbstring = "insert into addresses (public_address) values ('"+str(addr)+"');"
        print dbstring
        db.dbexecute(dbstring, False)

    if len(known_ids)>1:
      j=0 #do nothing
    elif len(known_ids)==1:
      #make all addresses in list under this person id
      the_id = known_ids[0]
      for x in address_list:
        dbstring="update addresses set person_id = '"+str(the_id)+"' where public_address='"+str(x)+"';"
        print dbstring
        db.dbexecute(dbstring, False)
    else:
      #give them all a new person id
      the_id = generate_new_id()
      dbstring = "insert into people (person_id, firstblock) values ('"+str(the_id)+"', "+str(block_height)+");"
      db.dbexecute(dbstring, False)
      for x in address_list:
        dbstring="update addresses set person_id = '"+str(the_id)+"' where public_address='"+str(x)+"';"
        print dbstring
        db.dbexecute(dbstring, False)
