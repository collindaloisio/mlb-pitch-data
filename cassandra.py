from dse.cluster import Cluster





##################################################################################################################
# Class: Cassandra

# Explained: Run a cassandra instance on your local machine with ./cassandra from cassandra install
# directory at 127.0.0.1
# This class connects to that instance and every instance in its cluster
##################################################################################################################


def connectToLocal():
    cluster = Cluster()
    session = cluster.connect()

