#!/usr/bin/python
from dse.cluster import Cluster
import settings
import scrapeUtils
import re

##################################################################################################################
# Class: Cassandra

# Explained: Run a cassandra instance on your local machine with ./cassandra from cassandra install
# directory at 127.0.0.1
# This class connects to that instance and every instance in its cluster
##################################################################################################################


def createKeyspace(keyspaceInput):
    cluster = Cluster()
    keyspace = keyspaceInput
    session = cluster.connect()
    session.execute('CREATE KEYSPACE ' + str(keyspaceInput) + " WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")


#creates a table and insterts it into a keyspace:k

def createTable(table, k):
    cluster = Cluster()
    keyspace = k
    session = cluster.connect(keyspace)

    #---Use this code to make your initial pitch table---
    session.execute('CREATE TABLE ' + str(table) + ' (game_id text, atbat_num int, pitcher_id int, spin_rate float, '
                    'pitch_type text, start_speed float, end_speed float, nasty int, '
                    'outcome_shorthand text, outcome text, inning_num int, p_num int,'
                    'outs_after_bat int, PRIMARY KEY(game_id, inning_num, p_num));')

#inserts data from a filename and into a keyspace: k and a table: table

def insertData(fileName, k, table):
    #---This line will insert pitch data into your table for a given inning file---
    #---Currently, the primary key is the atbat_num, and the game_id---

    #not sure if this is redundant or necessary should look into it
    cluster = Cluster()
    keyspace = k
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


def selectPitcher(k, table, pitcher):
    cluster = Cluster()
    keyspace = k
    session = cluster.connect(keyspace)

    data = session.execute('SELECT * FROM ' + str(table))
    for pitch in data:
        if pitch.pitcher_id == pitcher:
            print(str(pitch))



def main():
    createTable()


if __name__ == "__main__":
    main()



