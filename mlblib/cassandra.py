#!/usr/bin/python
from dse.cluster import Cluster

##################################################################################################################
# Class: Cassandra

# Explained: Run a cassandra instance on your local machine with ./cassandra from cassandra install
# directory at 127.0.0.1
# This class connects to that instance and every instance in its cluster
##################################################################################################################


def createTable():
    cluster = Cluster()
    keyspace = "pitch_test"
    session = cluster.connect(keyspace)
    connection = connection.execute('SELECT * FROM pitches LIMIT 5')
    for pitch in pitches:
        print("Pitcher ID %d - %s" % (pitch.pitcher_id, pitch.pitch_type))


def main():
    createTable()


if __name__ == "__main__":
    main()



