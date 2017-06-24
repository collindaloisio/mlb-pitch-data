from mlblib import settings
import psycopg2


def callSQL(filename):
    filename = settings.localDir
    with open(filename) as f:
        sqlQuery = f.read()
    #We should add dbname, user, password to settings.py
    conn = psycopg2.connect("dbname=postgres user=postgres password=crump123")
    cur = conn.cursor()
    cur.execute(sqlQuery)
    conn.commit() #commit changes
    cur.close()
    conn.close()
