import db

def init():
    dbstring = "create table meta (lastblockdone int);"
    db.dbexecute(dbstring, False)

    dbstring = "create table correlations (from_person_id varchar(200), to_person_id varchar(200), weight float);"
    db.dbexecute(dbstring, False)

    dbstring = "create table people (person_id varchar(200), name varchar(500), firstblock int);"
    db.dbexecute(dbstring, False)

    dbstring = "create table addresses (public_address varchar(200), person_id varchar(200), bitcoin_id varchar(200));"
    db.dbexecute(dbstring, False)

    dbstring = "create table outputs (output_id varchar(200), person_id varchar(200), transaction_hash varchar(200), output_index int, bitcoin_id varchar(200), spent bool, value bigint, type varchar(100), destination_address varchar(200));"
    db.dbexecute(dbstring, False)

    
