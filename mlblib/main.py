#!/usr/bin/python

from mlblib import scrapeUtils,settings,database
import os
from cassandra.cluster import Cluster
import settings
import scrapeUtils



def main():
    #Below is the usage of the new single row
    #This requires that you have inning files in your local dir
    #If not, call downloadAllInningFiles with a good YYYYMMDD string first

    cluster = Cluster()
    session = cluster.connect('pitch_test')

    #ONLY NEEDS TO HAPPEN ONCE, generates table with allcolumnssss
    database.generateTableFromDoc(session,settings.docDir+"all_db_columns.txt","pitches_all")

    for file in os.listdir(settings.localDir):
        if file.endswith('.xml'):
            data = scrapeUtils.parsePitchRewrite(settings.localDir + file, settings.docDir+"all_db_columns.txt")
            #Batch Insert takes a session so we do not have to open and close cassandra sessions
            #The reason to do multiple batch inserts is so that batches do not get too large
            for row in data:
                database.singleRowInsert(session, row, 'pitches_all')




if __name__ == "__main__":
    main()



