import sys, urllib, re, urlparse
import fileinput
import Game
import Pitcher
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import glob
import numpy as np
import pandas as pd
import matplotlib as plt

mlbSite = "http://gd2.mlb.com/components/game/mlb/"

##################################################################################################################
# Function: downloadGameFiles                                                                                    #
# inputs: dateUrl- A string that is the path to a specific date on the MLB site that is the home to all games    #
#         on that given date                                                                                     #
#                                                                                                                #
# Explained: This function takes the URl for the specific date and downloads all game.xml files for that given   #
# date. This function introduces the BeautifulSoup module that we had to download. If you don't get this by      #
# just looking at it, I'll explain in person. It took me a while of going down the internet rabit hole to figure #
# this shit out.                                                                                                 #
##################################################################################################################


def getGameLinks(dateUrl):
    counter = 0

    # Establish URL connection
    f = urllib.urlopen(dateUrl)

    # Spin up instance of beautiful soup html parser
    soup = BeautifulSoup(f, 'html.parser')
    linkList = []

    # For all links in the html file that have the substring "GID"...
    for link in soup.find_all("a", string=re.compile("gid")):

        # Create fileName for file stored locally,
        
        # Create the URL for the specific file you want
        gameLink = dateUrl + '/' + link.get('href')
        linkList.append(gameLink)
    for link in linkList:
        print(link)
    return(linkList)

# This is a wrapper function will instantiate a game class object given a
# game URL. For each game it will create the Pitcher Objects and
def gameBuilder(gameDirectory):

    homePitchers = list()
    awayPitchers = list()

    f = urllib.urlopen(gameDirectory)
    gameSoup = BeautifulSoup(f, 'html.parser')
    for files in gameSoup.find_all("a", string=re.compile("bis_boxscore.xml")):
        try:
            gameFile = 'boxScore.xml'
            urllib.urlretrieve(gameDirectory + "bis_boxscore.xml", gameFile)
        except:
            print("Could not download boxscore file.")

    tree = ET.parse('bis_boxscore.xml')
    root = tree.getroot()
    for pitching in root.findall('pitching'):
        if pitching.attrib.get("team_flag") in 'away':
            for pitcherData in pitching.findall('pitcher'):
                # Build Pitcher
                currentPitcher = Pitcher(pitcherData.attrib.get('id'), pitcherData.attrib.get('name'), pitcherData.attrib.get('era'))
                # Add to awayPitchers
                awayPitchers.append(currentPitcher)
        else:
            for pitcher in pitching.findall('pitcher'):
                # Build Pitcher
                currentPitcher = Pitcher(pitcherData.attrib.get('id'), pitcherData.attrib.get('name'), pitcherData.attrib.get('era'))
                # Add to awayPitchers
                homePitchers.append(currentPitcher)

    # Find all Pitches for the given game,
    # Create List of Home Pitchers and Away Pitchers

    # For each at Bat in the game,
    # Compile a List of pitches for that at bat and create AtBat instance
    # Compile list of ALL at bats in game

    # Create game instance and reutrn
    currentGame = Game()
    return currentGame

def downloadGameDescriptionFiles(dateUrl):

    # Appended to each file as we download for uniqueness
    counter = 0
    linkList = getGameLinks(dateUrl)

    # For all links in the html file that have the substring "GID"...
    for gameLink in linkList:
        f = urllib.urlopen(gameLink)
        gameSoup = BeautifulSoup(f, 'html.parser')
        for files in gameSoup.find_all("a", string=re.compile("game.xml")):
            # Download the file and increment counter for uniqueness
            try:
                dfileName = 'gameFile' + str(counter) + '.xml'
                urllib.urlretrieve(gameLink + 'game.xml', dfileName)
                counter = counter + 1
            except:
                print("Could not Download File")

#Given an atBat instnace, plot all pitches on x,y grid
def plotPitches(atBat) :
    pitches = atBat.getPitches()
    pitchx = []
    pitchy = []
    for pitch in pitches :
        pitchx.append(pitch.x)
        pitchy.append(pitch.y)

    dat = {'x': pitchx, 'y': pitchy}
    toPlot = pd.DataFrame(data =dat, index=index)
    toPlot.plot()




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
    print("Downloading game files. Standby...")
    getGameLinks(fullUrl)
    #downloadGameDescriptionFiles(fullUrl)

    # Parse the XML files to determine who played
    #print("Games Played on " + date + ":")
    #whoPlayed()
    #getGameLinks(fullUrl)

    gameSelected = raw_input('From List above pick a game (First Three Letters of Away Team: ') # Prompt for game

if __name__ == "__main__":
    main()
