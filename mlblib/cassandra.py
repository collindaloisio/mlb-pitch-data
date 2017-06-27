#!/usr/bin/python
from dse.cluster import Cluster
from mlblib import *

##################################################################################################################
# Class: Cassandra

# Explained: Run a cassandra instance on your local machine with ./cassandra from cassandra install
# directory at 127.0.0.1
# This class connects to that instance and every instance in its cluster
##################################################################################################################


def createTable(fileName):
    cluster = Cluster()
    keyspace = "pitch_test"
    session = cluster.connect(keyspace)

    #session.execute('DROP TABLE PITCHES')
    #---Use this code to make your initial pitch table---
    #make_table = session.execute('CREATE TABLE PITCHES (game_id text, atbat_num int, pitcher_id int, spin_rate float, '
    #                             'pitch_type text, start_speed float, end_speed float, nasty int, '
    #                             'outcome_shorthand text, outcome text, inning_num int, p_num int,'
    #                             'outs_after_bat int, PRIMARY KEY(game_id, inning_num, p_num));')


    #---This line will insert pitch data into your table for a given inning file---
    #---Currently, the primary key is the atbat_num, and the game_id---
    data = scrapeUtils.parsePitch(settings.localDir+fileName)

    for line in data:
        session.execute(line)

    #---this will just select some data and spit it out---
    connection = session.execute('SELECT * FROM pitches LIMIT 5')

    pitchList = []
    for pitch in connection:
        foo = str("Pitcher ID %s - %s" % (pitch.pitcher_id, pitch.pitch_type))
        pitchList.append(foo)
        print(pitchList)
        #print("Pitcher ID %s - %s" % (pitch.pitcher_id, pitch.pitch_type))
    return(pitchList)

def main():
    createTable()


if __name__ == "__main__":
    main()



