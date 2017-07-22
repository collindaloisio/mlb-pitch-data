#!/usr/bin/python
from cassandra.cluster import Cluster
import settings
import scrapeUtils
import re

##################################################################################################################
# Class: Cassandra

# Explained: Run a cassandra instance on your local machine with ./cassandra from cassandra install
# directory at 127.0.0.1
# This class connects to that instance and every instance in its cluster
##################################################################################################################


def fetchCQL(filename):
    with open(filename) as f:
        cqlQuery = f.read()
    return cqlQuery



def createKeyspace(keyspace):
    cluster = Cluster()
    session = cluster.connect()
    session.execute('CREATE KEYSPACE ' + str(keyspace) + " WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")

#
# Input: table (name of table), keyspace (name of keyspace)
# Creates a table and inserts it into a keyspace
#
def createTable(keyspace):
    cluster = Cluster()
    session = cluster.connect(keyspace)

    #---Use this code to make your initial pitch table---
    session.execute(fetchCQL(settings.sqlDir+'CQL_test.cql'))

#inserts data from a filename and into a keyspace: k and a table: table

def insertData(fileName, keyspace, table):
    #---This line will insert pitch data into your table for a given inning file---
    #---Currently, the primary key is the atbat_num, and the game_id---

    #not sure if this is redundant or necessary should look into it
    cluster = Cluster()
    session = cluster.connect(keyspace)

    data = scrapeUtils.parsePitch(settings.localDir+fileName, table)
    for line in data:
        session.execute(line)


def testData(k):
    cluster = Cluster()
    keyspace = k
    session = cluster.connect(keyspace)
    #---this will just select some data and spit it out, currently used in test---
    connection = session.execute('SELECT * FROM pitches LIMIT 5')
    pitchList = []
    for pitch in connection:
        foo = str("Pitcher ID %s - %s" % (pitch.pitcher_id, pitch.pitch_type))
        pitchList.append(foo)
        print(pitchList)
        #print("Pitcher ID %s - %s" % (pitch.pitcher_id, pitch.pitch_type))
    return(pitchList)


def selectPitcher(keyspace, table, pitcher):
    cluster = Cluster()
    session = cluster.connect(keyspace)

    data = session.execute('SELECT * FROM ' + str(table))
    for pitch in data:
        if pitch.pitcher_id == pitcher:
            print(str(pitch))


if __name__ == "__main__":
    main()



