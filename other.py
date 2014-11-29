import hashlib
import random
import db

def generate_new_id():
  return hashlib.sha256(str(random.random())).hexdigest()

def merge_people(person_ids, cloned_person_id):
    for person_id in person_ids:
        dbstring = "update addresses set person_id = '"+str(cloned_person_id)+"' where person_id ='"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        dbstring = "update outputs set person_id = '"+str(cloned_person_id)+"' where person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        dbstring = "update correlations set from_person_id = '"+str(cloned_person_id)+"' where from_person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)
        dbstring = "update correlations set to_person_id = '"+str(cloned_person_id)+"' where to_person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        #merge duplicate rows in correlations table
        #TO DO
