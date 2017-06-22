#!/usr/bin/python
import unittest
import sys
from listGames import *

class TestDownloads(unittest.TestCase):

#Unit test of listGames.downloadInningFile
#to pass one inning file should be saved to ./local
    def testdownloadInningFile(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
        downloadInningFile(link,1)
        self.assertTrue(True)


# def main():
#     testdownloadInningFile()




if __name__ == "__main__":
    unittest.main()
