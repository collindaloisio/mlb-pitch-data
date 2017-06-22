import unittest
import sys
from listGames import *


#Unit test of listGames.downloadInningFile
#to pass one inning file should be saved to ./local
def testdownloadInningFile():
    link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
    downloadInningFile(link,1)


def main():
    testdownloadInningFile()




if name == '__main__':
    main()
