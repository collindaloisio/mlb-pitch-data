#!/usr/bin/python
import sys, urllib, re, urlparse
import fileinput
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import glob
import os

##################################################################################################################
# Function: downloadGameFiles
# inputs: dateUrl- A string that is the path to a specific date on the MLB site that is the home to all games
#         on that given date
#
# Explained: This function takes the URl for the specific date and downloads all game.xml files for that given
# date. This function introduces the BeautifulSoup module that we had to download. If you don't get this by
# just looking at it, I'll explain in person. It took me a while of going down the internet rabit hole to figure
# this shit out.
##################################################################################################################

def downloadGameFiles(dateUrl):

    # Appended to each file as we download for uniqueness
    counter = 0

    # Establish URL connection
    f = urllib.urlopen(dateUrl)

    # Spin up instance of beautiful soup html parser
    soup = BeautifulSoup(f, 'html.parser')

    # For all links in the html file that have the substring "GID"...
    for link in soup.find_all("a", string=re.compile("gid")):

        # Create fileName for file stored locally,
        dfileName = 'gameFile' + str(counter) + '.xml'
        # Create the URL for the specific file you want
        gameLink = dateUrl + '/' + link.get('href')

        # Open file URL for specific game and download game.xml file
        f = urllib.urlopen(gameLink)
        gameSoup = BeautifulSoup(f, 'html.parser')

        for files in gameSoup.find_all("a", string=re.compile("game.xml")):
            # Download the file and increment counter for uniqueness
            try:
                urllib.urlretrieve(gameLink + 'game.xml', dfileName)
                print(gameLink + 'game.xml')
		counter = counter + 1
            except:
                print("Could not Download File")

def whoPlayed():
    for filename in glob.glob('*.xml'):
        tree = ET.parse(filename)
        root = tree.getroot()
        gameTime = root.attrib.get("game_time_et")
        for team in root.findall('team'):
            if(team.get('type') == 'home'):
                hometeam = team.get('name_full')
            if(team.get('type') == 'away'):
                awayTeam = team.get('name_full')

        print(awayTeam + " played at " + hometeam + " at " + gameTime + " Eastern Time\n")



def main():
    mlbSite = "http://gd2.mlb.com/components/game/mlb/"
    for filez in os.listdir("./"):
        if "gameFile" in filez :
            os.remove(filez)
    date = raw_input('Enter a date YYYYMMDD: ') #prompt for date

    #parse input
    yr= date[0:4]
    mon = date[4:6]
    day = date[6:8]
    
    #build name
    standardName = 'year_'+yr+'/month_'+mon+'/day_'+day

    #this will be the full Url for some Day
    fullUrl = mlbSite+standardName

    # Download the files for a specific date
    downloadGameFiles(fullUrl)

    # Parse the XML files to determine who played
    whoPlayed()

if __name__ == "__main__":
    main()




