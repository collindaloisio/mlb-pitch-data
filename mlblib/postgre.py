import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import LoggingConnection



def initiateSQLdb():
    filename = settings.sqlInitiate
    with open(filename) as f:
        sqlQuery = f.read()
    #We should add dbname, user, password to settings.py
    conn = psycopg2.connect("dbname=postgres user=postgres password=crump123")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) #to allow for db creation
    cur = conn.cursor()
    print(sqlQuery)
    try:
        cur.execute(sqlQuery)
    except StandardError as e:
        print("psycopg2 threw: " + str(e))
        print("Database might already exist... Moving on")
    cur.close()
    conn.close()
