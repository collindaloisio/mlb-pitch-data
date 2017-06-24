#!/usr/bin/python
import unittest
from lib import *
import os

##################################################################################################################
# Class: TestDownloads

# Explained: This class instantiates the unittest module. each test should have an argument, often self.
# Tests are determined to be passed or not by a statement like self.assertEqual or self.AssertTrue

# I changed the name of the file to unitTests.py because apparently packages and their files need different nanes.
# Made this a package to properly import lib.scrapeUtils
##################################################################################################################

class TestDownloads(unittest.TestCase):

#Unit test of listGames.downloadInningFile
#to pass one inning file should be saved to local dir
    def test_if_file_exists_downloading_InningFile(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
        scrapeUtils.downloadInningFile(link,1)
        self.assertTrue(os.path.isfile(os.path.abspath(settings.localDir + 'inning1.xml')))
        os.remove(os.path.abspath(settings.localDir + 'inning1.xml'))


if __name__ == "__main__":
    unittest.main()
