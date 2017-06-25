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
    session = cluster.connect()
    query = 'CREATE TABLE pitches (pitch_id varchar primary key, type int, x int, y int);'
    session.execute(query)


def main():
    createTable()


if __name__ == "__main__":
    main()



