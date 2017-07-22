from mlblib import cassandra
import sklearn
import logging
from dse import query
import pandas as pd
from dse.cluster import Cluster
from dse.protocol import NumpyProtocolHandler
from dse.query import tuple_factory

log = logging.getLogger()
log.setLevel('DEBUG')
#handler = logging.StreamHandler()
#handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
#log.addHandler(handler)

def doSomething():
    cluster = Cluster()
    keyspace = 'pitch_test'
    session = cluster.connect(keyspace)

    session.row_factory = tuple_factory

    data = session.execute('Select pitcher_id, start_speed, end_speed from pitches where pitcher_id = 543699 '
                                 'LIMIT 100 ALLOW FILTERING')
    print(type(data[1]))


    #for pitch in data:
    #    if pitch.pitcher_id == 543699:
    #        pitch.end_speed


def doIt():
    cluster = Cluster()
    session = cluster.connect('pitch_test')
    session.row_factory = tuple_factory
    session.client_protocol_handler = NumpyProtocolHandler

    prepared_stmt = session.prepare('SELECT pitcher_id FROM pitches WHERE pitcher_id = 543699'
                                    ' LIMIT 100 ALLOW FILTERING;')

    bound_stmt = prepared_stmt.bind([])
    rslt = session.execute(bound_stmt)
    df = pd.DataFrame(rslt[0])
    print(df)
