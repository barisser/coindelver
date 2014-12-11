import db

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

        dbstring = "delete from people * where person_id = '"+str(person_id)+"';"
        db.dbexecute(dbstring, False)

        #merge duplicate rows in correlations table
        #TO DO


class Person:
    def __init__(self, person_id):
        self.person_id = person_id
        self.name = ''

    def load(self): #creates new entry if not found
        dbstring = "select * from people where person_id = '"+str(self.person_id)+"';"
        person_info = db.dbexecute(dbstring, True)
        if len(person_info)>0:
            self.name = person_info[0][1] #there should never be more than one entry
            self.firstblock = person_info[0][2]
        else:
            dbstring = "insert into people values ('"+str(self.person_id)+"', '"+str(self.name)+"', -1);"
            db.dbexecute(dbstring, False)

    def addresses(self):
        dbstring = "select public_address from addresses where person_id='"+str(self.person_id)+"';"
        addresses = db.dbexecute(dbstring, True)
        return addresses
