import psycopg2
import os

def dbexecute(sqlcommand, receiveback):
  databasename=os.environ['DATABASE_URL']
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
