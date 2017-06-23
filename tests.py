#!/usr/bin/python
import unittest
import sys
from scrapeUtils import *

##################################################################################################################
# Class: TestDownloads

# Explained: This class instantiates the unittest module. each test should have an argument, often self.
# Tests are determined to be passed or not by a statement like self.assertEqual or self.AssertTrue
##################################################################################################################

class TestDownloads(unittest.TestCase):

#Unit test of listGames.downloadInningFile
#to pass one inning file should be saved to ./local
    def testdownloadInningFile(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
        downloadInningFile(link,1)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
