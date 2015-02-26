import psycopg2
import os
import random
import hashlib
import urlparse

con=None
databasename="postgres://barisser:password@localhost/delver"
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(databasename)

def dbexecute(sqlcommand, receiveback):
  #username=''
  #print sqlcommand
  con=psycopg2.connect(database= url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
  result=''
  cur=con.cursor()
  cur.execute(sqlcommand)
  if receiveback:
    result=cur.fetchall()
  con.commit()
  cur.close()
  con.close()
  return result

def add_input_tx(input_address, tx_hash, amount, height):
    dbstring = "insert into inputs values ('"+str(input_address)+"', '"+str(tx_hash)+"', '"+str(amount)+"', '"+str(height)+"');"
    dbexecute(dbstring, False)

def add_output_tx(output_address, tx_hash, amount, height):
    dbstring = "insert into outputs values ('"+str(output_address)+"', '"+str(tx_hash)+"', '"+str(amount)+"', '"+str(height)+"');"
    dbexecute(dbstring, False)

def add_tx_output(txhash, index, spent, spent_at_txhash, height, height_spent, amount):
    dbstring = "insert into tx_outputs values ('"+str(txhash)+"', "+str(index)+", '"+str(spent)+"', '"+str(spent_at_txhash)+"', "+str(height)+", "+str(height_spent)+", "+str(amount)+");"
    dbexecute(dbstring, False)

def spent_tx_output(txhash, index, spent_at_txhash, height_spent):
    dbstring = "update tx_outputs set spent=True, spent_at_txhash='"+str(spent_at_txhash)+"', height_spent="+str(height_spent)+" where txhash='"+str(txhash)+"' and index='"+str(index)+"';"
    dbexecute(dbstring, False)

def select_tx_output(txhash):
    dbstring = "select * from tx_outputs where txhash='"+str(txhash)+"';"
    results = dbexecute(dbstring, True)
    return results

def add_header(hash, prev_hash, height):
    dbstring = "insert into headers values ('"+str(hash)+"', '"+str(prev_hash)+"', "+str(height)+");"
    dbexecute(dbstring, False)

def check_header(hash):
    dbstring = "select count(*) from headers where hash='"+str(hash)+"';"
    a = dbexecute(dbstring, True)
    if a[0][0] > 0:
      return True
    else:
      return False

def last_header():
    dbstring = "select * from headers order by height desc limit 1;"
    a = dbexecute(dbstring, True)
    if len(a)>0:
      b = a[0][2]
    else:
      b=-1
    return b
