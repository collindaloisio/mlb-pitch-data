import urllib
from ftplib import FTP
import os.path
import xml
import fileinput



ftpSite = "http://gd2.mlb.com/components/game/mlb/"

ftp = FTP()


date = raw_input('Enter a date YYYYMMDD: ') #prompt for date

#parse input
yr= date[0:4]
mon = date[4:6]
day = date[6:8]

#build name
standardName = 'year_'+yr+'/month_'+mon+'/day_'+day




#date = Get some date from the user


#Dylan feel free to add this back in. I don't understand the FTP stuff in here and it 
#was breaking so I commented it out.
#Explain what it's trying to do. 

#fileNames = ftp.nlist('/year_2015/month_03/day_21/')

#this will be the full Url for some game
fullUrl = ftpSite+standardName




try:
    urllib.urlretrieve('http://gd2.mlb.com/components/game/mlb/year_2015/month_03/day_21/gid_2015_03_21_kcamlb_chamlb_1/game.xml', 'currentGame.xml')
except:
    print("Could not Download File")



try:
    fileHandle=urllib.urlopen(fullUrl)
except:
    print("Could not Download File")


print fileHandle.geturl()



