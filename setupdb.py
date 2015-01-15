import db

def init():
    dbstring = "create table meta (lastblockdone int);"
    db.dbexecute(dbstring, False)

    dbstring = "insert into meta values (-1);"
    db.dbexecute(dbstring, False)

    dbstring = "create table correlations (from_person_id varchar(200), to_person_id varchar(200), weight float);"
    db.dbexecute(dbstring, False)

    dbstring = "create table people (person_id varchar(200), name varchar(500), firstblock int);"
    db.dbexecute(dbstring, False)

    dbstring = "create table addresses (public_address varchar(200));"
    db.dbexecute(dbstring, False)

    dbstring = "create table address_person_correlation (public_address varchar(200), person_id varchar(200), weight float);"
    db.dbexecute(dbstring, False)

    dbstring = "create table address_address_correlation (from_address varchar(200), to_address varchar(200), weight float);"
    db.dbexecute(dbstring, False)

    dbstring = "create table transactions (transaction_hash varchar(200), height int);"
    db.dbexecute(dbstring, False)

    dbstring = "create table inputs (public_address varchar(200), txhash varchar(200), amount float);"
    db.dbexecute(dbstring, False)

    dbstring = "create table outputs (public_address varchar(200), txhash varchar(200), amount float);"
    db.dbexecute(dbstring, False)

def delete_all():
    dbstring = "drop table inputs;drop table address_address_correlation;drop table address_person_correlation;drop table addresses;drop table outputs; drop table people; drop table correlations; drop table meta; drop table transactions"
    db.dbexecute(dbstring, False)

def reset():
    delete_all()
    init()
