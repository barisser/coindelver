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

def add_new_person(public_address):
  random_id = generate_new_id()
  dbexecute("insert into persons values ('"+random_id+"', '', '');", False)
  dbexecute("update addresses set person_id = '"+str(random_id)+"' where public_address='"+str(public_address)+"';", False)

def identify_person(public_address, name):
  preexisting_id = dbexecute("select person_id from addresses where public_address='"+str(public_address)+"';",True)
  if len(preexisting_id)==0:
    add_new_person(public_address)
    dbexecute("update people set nane = '"+str(name)+"' where public_address='"+str(public_address)+"';",False)
