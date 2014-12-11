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

def add_address(public_address, person_id, bitcoin_id):
    dbstring = "insert into addresses values ('"+str(public_address)+"', '"+str(person_id)+"', '"+str(bitcoin_id)+"');"
    dbexecute(dbstring, False)

def edit_address(public_address, person_id, bitcoin_id):
    dbstring = "update addresses set person_id ='"+str(person_id)+"', bitcoin_id='"+str(bitcoin_id)+"' where public_address='"+str(public_address)+"';"
    dbexecute(dbstring, False)

def add_person(person_id, name, firstblock):
    dbstring = "insert into people values ('"+str(person_id)+"', '"+str(name)+"', "+str(firstblock)+");"
    dbexecute(dbstring, False)

def add_correlation(from_person_id, to_person_id, weight): #also edits if already exists
    #check if exists
    dbstring = "select * from correlations where from_person_id ='"+str(from_person_id)+"';"
    existing_correlation = dbexecute(dbstring, True)

    if len(existing_correlation) > 0:
        dbstring = "update correlations set weight="+str(weight)+") where from_person_id = '"+str(from_person_id)+"' and to_person_id='"+str(to_person_id)+"';"
        dbexecute(dbstring, False)
    else:
        dbstring = "insert into correlations values ('"+str(from_person_id)+"', '"+str(to_person_id)+"', "+str(weight)+");"
        dbexecute(dbstring, False)

def get_correlations(from_person_id):
    dbstring = "select to_person_id, weight from correlations where from_person_id='"+str(from_person_id)+"';"
    correlations = dbexecute(dbstring, True)
    return correlations
