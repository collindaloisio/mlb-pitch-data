from mlblib import database
import logging
import matplotlib.pyplot as plt
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.protocol import NumpyProtocolHandler
from cassandra.query import tuple_factory
import time




def tableToPandas():
    cluster = Cluster()
    session = cluster.connect('pitch_test')
    session.row_factory = tuple_factory
    session.client_protocol_handler = NumpyProtocolHandler

    # prepared_stmt = session.prepare('SELECT pitcher_id,spin_rate, start_speed, end_speed FROM pitches WHERE pitcher_id = 543699'
    #                                 ' LIMIT 100 ALLOW FILTERING;')

    prepared_stmt = session.prepare('SELECT * FROM pitches_all LIMIT 1000 ALLOW FILTERING;')


    print(prepared_stmt)
    rslt = session.execute(prepared_stmt)
    df = pd.DataFrame(rslt[0])
    #print("Means of data shown... Returning data frame object:")
    #print(df['outcome_shorthand'])
    return(df)

def plotUp(df):
    #plt.style.use('ggplot')
    mapping = {'S':0.001, 'X':.5,'B':.999}
    #df.replace('outcome_shorthand',mapping)
    print(df['outcome_shorthand'])

    bsmap = df['outcome_shorthand'].replace(mapping)
    x=df['x']
    y=df['y']
    #ball_strike_map = df.replace('outcome_shorthand',mapping)['outcome_shorthand']
    plt.scatter(x=x, y=y, c=bsmap)
    plt.gray()


if __name__ ==  "__main__":
    df = tableToPandas()
    plotUp(df)
    plt.show()