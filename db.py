import psycopg2
import os
import random
import hashlib
import urlparse

con=None
databasename="postgres://barisser:password@localhost:5432/coindelve"
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(databasename)

def dbexecute(sqlcommand, receiveback):
  #username=''
  print sqlcommand
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

def add_input_tx(input_address, tx_hash, amount):
    dbstring = "insert into inputs values ('"+str(input_address)+"', '"+str(tx_hash)+"', '"+str(amount)+"');"
    dbexecute(dbstring, False)

def add_output_tx(output_address, tx_hash, amount):
    dbstring = "insert into outputs values ('"+str(output_address)+"', '"+str(tx_hash)+"', '"+str(amount)+"');"
    dbexecute(dbstring, False)
