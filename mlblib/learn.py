from mlblib import database
import logging
from dse import query
import pandas as pd

from cassandra.cluster import Cluster
from cassandra.protocol import NumpyProtocolHandler
from cassandra.query import tuple_factory


def tableToPandas():
    cluster = Cluster()
    session = cluster.connect('pitch_test')
    session.row_factory = tuple_factory
    session.client_protocol_handler = NumpyProtocolHandler

    prepared_stmt = session.prepare('SELECT pitcher_id,spin_rate, start_speed, end_speed FROM pitches WHERE pitcher_id = 543699'
                                    ' LIMIT 100 ALLOW FILTERING;')


    print(prepared_stmt)
    rslt = session.execute(prepared_stmt)
    df = pd.DataFrame(rslt[0])
    print(df.mean())
    #print(df)
