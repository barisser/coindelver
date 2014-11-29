import db
import people

def link_addresses(addresses):
    person_ids = []
    for address in addresses:
        person_id = db.dbexecute("select person_id from addresses where public_address='"+str(address)+"';", True)
        if len(person_id)>0:
            person_ids.append(person_id[0][0])

    if len(person_ids)>1:
        cloned_into = person_ids[0]
        people.merge_people(person_ids, cloned_into) #merging with first arbitrarily


class Addresses:
    def __init__(self, public_address):
        self.public_address = public_address
