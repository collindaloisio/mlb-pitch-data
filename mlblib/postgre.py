import config
import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import LoggingConnection


#
#Function: fetches SQL from a filename
#
def fetchSQL(filename):
    with open(filename) as f:
        sqlQuery = f.read()
    return sqlQuery


#
#Function: Initiates new postgre DB named mlbdb for the first time
# IF you run twice it should tell you that it already exists...
# This will definitely fail on password for you
def initiateSQLdb():
    filename = settings.sqlInitiate
    sqlQuery = fetchSQL(filename)
    #We should add dbname, user, password to settings.py
    conn = psycopg2.connect("dbname=postgres user=postgres password="+ config.postgrePassword)
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

#
#Function: Inserts whatever sql query you write into DB
#
def insertSQL(filename):
    fetchSQL(filename)


