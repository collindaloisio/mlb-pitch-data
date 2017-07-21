#!/usr/bin/python

from mlblib import scrapeUtils,settings,cassandra
import os


def main():
    #postgre.insertPitchTable()
    #link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01'
    #postgre.downloadAndInsertPitchData(link,1)
    #postgre.checkDataExists()
    #scrapeUtils.downloadInningFile('http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/',1,2)
    #scrapeUtils.downloadAllInningFiles(link,0)
    #scrapeUtils.parsePitch(settings.localDir+"inningFile0.xml")
    for files in os.listdir(settings.localDir):
        if files.endswith('.xml'):
            cassandra.insertData(files)
        else:
            continue


if __name__ == "__main__":
    main()



