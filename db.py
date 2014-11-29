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

def add_output(output_id, person_id, transaction_hash, output_index, bitcoin_id, spent, value, type, destination_address):
    dbstring = "insert into outputs values ('"+str(output_id)+"', '"+str(person_id)+"', '"+str(transaction_hash)+"', "+str(output_index)+", '"+str(bitcoin_id)+"', "+str(spent)+", "+str(value)+", '"+str(type)+"', '"+str(destination_address)+"');"
    dbexecute(dbstring, False)
