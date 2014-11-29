import db

def address_count_per_person_id(person_id):
    dbstring = "SELECT count(*) FROM ADDRESSES INNER JOIN PEOPLE ON ADDRESSES.person_id = PEOPLE.person_id where addresses.person_id = '"+str(person_id)+"';"
    address_count = db.dbexecute(dbstring, True)
    return address_count[0][0]

def get_all_people():
    dbstring = "select person_id from people;"
    person_ids = db.dbexecute(dbstring, True)
    n=len(person_ids)
    for i in range(0,n):
        person_id = person_ids[i][0]
        n= address_count_per_person_id(person_id)
        if n>1:
            addresses= db.get_address_on_person(person_id)
            na = len(addresses)
            print person_id
            for x in range(0, na):
                print addresses[x][0]
            print ''
