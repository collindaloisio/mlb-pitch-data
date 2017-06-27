#!/usr/bin/python
import unittest
from mlblib import *
import os
import glob
from mlblib import cassandra

##################################################################################################################
# Class: TestDownloads

# Explained: This class instantiates the unittest module. each test should have an argument, often self.
# Tests are determined to be passed or not by a statement like self.assertEqual or self.AssertTrue

# I changed the name of the file to unitTests.py because apparently packages and their files need different nanes.
# Made this a package to properly import lib.scrapeUtils
##################################################################################################################

class TestDownloads(unittest.TestCase):

    global filePath
    filePath = os.path.abspath(settings.localDir)

#Unit test of listGames.downloadInningFile
#to pass one inning file should be saved to local dir
    @unittest.skip("don't want to download file")
    def test_if_file_exists_and_not_size_zero_downloading_InningFile(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
        scrapeUtils.downloadInningFile(link,1)
        self.assertTrue(os.path.isfile(os.path.abspath(settings.localDir + 'inning1.xml')))
        self.assertNotEquals(os.path.getsize(settings.localDir + 'inning1.xml'), 0)
        os.remove(os.path.abspath(filePath + '/inning1.xml'))

    @unittest.skip("don't want to download file")
    def test_download_inning_is_passed_non_existent_inning(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/'
        self.assertEqual(scrapeUtils.downloadInningFile(link,15), -1)
        self.assertFalse(os.path.isfile(filePath + '/inning15.xml'))

    @unittest.skip("don't want to download file")
    def test_download_inning_is_passed_non_existent_game_dir(self):
        link = "NO_DICE_GAME_FILE"
        self.assertEqual(scrapeUtils.downloadInningFile(link,1),-1)
        self.assertFalse(os.path.isfile(filePath + '/inning1.xml'))

    @unittest.skip("don't want to download a bunch of files")
    def test_download_all_inning_files_for_a_given_date(self):
        link = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01'
        scrapeUtils.downloadAllInningFiles(link, 0)
        for file in glob.glob(settings.localDir+'inning*'):
            self.assertNotEquals(os.path.getsize(file), 0)
            os.remove(file)


class TestDatabaseFunctionality(unittest.TestCase):

    @unittest.skip("Don't want to set up a database yet. This is Collin's work. Waiting for completion")
    def test_postgre(self):
        postgre.initiateSQLdb()

    #should improve this test
    @unittest.skip("Don't want to set up a database yet. This is Collin's work. Waiting for completion")
    def test_cassandra(self):
        self.assertTrue(cassandra.testData() is not None)

if __name__ == "__main__":
    unittest.main()
