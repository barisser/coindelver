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

def add_new_person(public_address):
  random_id = generate_new_id()
  dbexecute("insert into people values ('"+random_id+"', '', '');", False)
  dbexecute("update addresses set person_id = '"+str(random_id)+"' where public_address='"+str(public_address)+"';", False)

def add_output(txhash, output_index, type, destination_address, bitcoin_id, output_id, spent, value):
    dbstring = "insert into outputs values ("+str(output_index)+", '"+str(txhash)+"', '"+str(type)+"', '"+str(destination_address)+"', '"+str(bitcoin_id)+"', '"+str(output_id)+"', '"+str(spent)+"', "+str(value)+");"
    dbexecute(dbstring, False)

def spend_output(output_id, spent):
    dbstring = "update outputs set spent = "+str(spent)+" where output_id = '"+str(output_id)+"';"
    dbexecute(dbstring, False)

def get_outputs_on_address(address, unspent_only):
    if unspent_only:
        dbstring = "select * from outputs where destination_address = '"+str(address)+"' and spent = 'False';"
        outputs = dbexecute(dbstring, True)
    else:
        dbstring = "select * from outputs where destination_address = '"+str(address)+"';"
        outputs = dbexecute(dbstring, True)

def add_correlation(output_id, weight, person_id):
    existing_correlations = dbexecute("select * from correlations where output_id = '"+str(output_id)+"' and person_id = '"+person_id+"';", True)
    if len(existing_correlations) == 0:
        dbstring = "insert into correlations values ( '"+str(output_id)+"', "+str(weight)+", '"+str(person_id)+"');"
        dbexecute(dbstring, False)
    else:
        #add to previous weight
        weight = existing_correlations[0][1] + weight
        dbstring = "update correlations set weight = "+str(weight)+" where output_id = '"+str(output_id)+"' and person_id = '"+str(person_id)+"';"
        dbexecute(dbstring, False)

def get_correlations(output_id):
    dbstring = "select * from correlations where output_id = '"+str(output_id)+"';"
    correlations = dbexecute(dbstring, True)
    results = []
    for index, item in enumerate(correlations):
        item = {}
        item['output_id'] = item[0]
        item['weight'] = item[1]
        item['person_id'] = item[2]
        results.append(item)
    return results

def identify_person(public_address, name):
  preexisting_id = dbexecute("select person_id from addresses where public_address='"+str(public_address)+"';",True)
  if len(preexisting_id)==0:
    add_new_person(public_address)
    dbexecute("update people set name = '"+str(name)+"' where public_address='"+str(public_address)+"';",False)

def add_new_tx(txdata):
    #add transaction
    bitcoin_id = ''
    dbstring = "INSERT INTO transactions VALUES ("+txdata['hash']+","+ bitcoin_id + ");"
    dbexecute(dbstring, False)

    #add outputs
    index_position = 0
    for output in txdata['out']:
        type = "unknown"
        destination_address = output['addr']
        dbstring = "INSERT INTO outputs VALUES ("+str(index_position)+","+txdata['hash']+","+ type +","+str(destination_address)+","+bitcoin_id+")"
        index_position = index_position + 1
        dbexecute(dbstring, False)

def get_address_on_person(person_id):
    dbstring = "SELECT * FROM ADDRESSES INNER JOIN PEOPLE ON ADDRESSES.person_id = PEOPLE.person_id where addresses.person_id = '"+str(person_id)+"';"
    addresses = dbexecute(dbstring, True)
    return addresses

def delete_all():
    dbexecute("delete from outputs *;", False)
    dbexecute("delete from addresses *;", False)
    dbexecute("delete from correlations *;", False)
    dbexecute("delete from people *;", False)
