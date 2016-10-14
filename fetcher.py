import urllib
from ftplib import FTP
import os.path
import xml

ftpSite = "http://gd2.mlb.com/components/game/mlb/"

ftp = FTP()

print('Enter a Date')

#date = Get some date from the user

fileNames = ftp.nlist('/year_2015/month_03/day_21/')


try:
    urllib.urlretrieve('http://gd2.mlb.com/components/game/mlb/year_2015/month_03/day_21/gid_2015_03_21_kcamlb_chamlb_1/game.xml', 'currentGame.xml')
except:
    print("Could not Download File")