#!/usr/bin/python
import sys, urllib, re, urlparse
import fileinput
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import glob
import os
import tests
##################################################################################################################
# Class: scrapeUtils.py

# Explained:
##################################################################################################################

#
# Wrapper function to download a file
# Input: link you are downloading, fileName for local system
# Downloads the file at link in ./local
#

def downloadFile(link,fileName):
    try:
        #It took me way to long to find this explicit reference to .local and change it to ../local
        #How can we refactor accross the whole code base instead of explicit reference
        urllib.urlretrieve(link, "../local/" + fileName)
    except:
        print("Could not Download File")

#
# Function downloads all game files for that day
# Inputs: dateUrl- A string that is the path to a specific date on the MLB site that is the home to all games
#         on that given date
#         counter - Keeps track of how many files we have downloaded thus far. Is appended to end of file names.
# Output: Game files are downloaded to local directory within working directory
#

def downloadGameFiles(dateUrl, counter):

    print("Downloading File " + str(counter))

    # Establish URL connection
    try:
        f = urllib.urlopen(dateUrl)
    except:
        print("Could not establish connection to MLB website. Check internet connectivity")
        exit(-1)

    # Spin up instance of beautiful soup html parser
    soup = BeautifulSoup(f, 'html.parser')

    # For all links in the html file that have the substring "GID"...
    for link in soup.find_all("a", string=re.compile("chnmlb")):

        # Create fileName for file stored locally,
        dfileName = 'gameFile' + str(counter) + '.xml'
        # Create the URL for the specific file you want
        gameLink = dateUrl + '/' + link.get('href')

        # Open file URL for specific game and download game.xml file
        f = urllib.urlopen(gameLink)
        gameSoup = BeautifulSoup(f, 'html.parser')

        for files in gameSoup.find_all("a", string=re.compile("game.xml")):
            # Download the file and increment counter for uniqueness
            downloadFile(gameLink+'game.xml',dfileName)


#
# Function downloadInningFile based on link and user choice of inning or "all"
# Inputs: gameLink - Link to the gid file at the level of YYYYMMDD link
#        eg: http://gd2.mlb.com/components/game/mlb/year_2016/month_07/day_01/gid_2016_07_01_kcamlb_phimlb_1/
#        segment - segment of game you want to download, 1-last inning(9+) or "all" for the whole inning_all file
# Output: Downloads specified inning file determined by gameLink_segment to working directory
#

def downloadInningFile(gameLink, segment):

    segLink = '_'+str(segment)+'.xml'
    inningsLink = gameLink + 'inning/inning' + segLink
    #print(inningsLink)

    downloadFile(inningsLink, 'inning'+str(segment)+'.xml')


#
# Function parsePitch. should this be in a seperate parsing package.
# This function takes a filename as a path on system
# Outputs a CQL/SQL string for db insertion
#

def parsePitch(filename):

    if not(os.path.isfile(os.path.abspath(filename))):
        print("Filename passed to parsePitch is invalid.")
        exit(-1)



    frontSQL = "INSERT INTO PITCHES (spin_rate, pitch_type, start_speed) VALUES ("
    backSQL = ");\n"
    out = ""
    stringList = []

    tree = ET.parse(filename)
    root = tree.getroot()

    top = root.find('top') #get top of the inning

    #iterate through at bats in top of the inning
    for atbat in top.findall('atbat'):
        #iterate through pitches in atbat

        for pitch in atbat.findall('pitch'):
            spin_rate = pitch.get('spin_rate')
            pitch_type = pitch.get('pitch_type')
            start_speed = pitch.get('start_speed')
            catString = str(spin_rate)+','+"'"+str(pitch_type)+"'"+','+str(start_speed)
            stringList.append(catString)


    for stri in stringList:
        #build SQL
        out += frontSQL + stri + backSQL

    #print(out)
    return(out)


#
# Function returns a list of Dates that Jake Arrieta threw pitches in a game. This function was made
# with the intention of expaning it to work with any pitcher. Should be refactored to scrapePitcher in future
# Inputs: refUrl - This is the link to the website baseball-reference.com that
#         shows all of Jake Arrieta's games
# Output: Returns a list object of Dates that Jake Arrieta pitched in YYYYMMDD Format
#


def scrapePitcherDates(refUrl):
    
    try:
        f = urllib.urlopen(refUrl)
    except:
        print("Could not establish connection to MLB reference site. Please check internet connectivity")    
        exit(-1)

    soup = BeautifulSoup(f, 'html.parser')

    allDates = []

    for items in soup.find_all("td", attrs={'data-stat':'date_game'}):
        if len(str(items.contents)) > 6:
            allDates.append(str(items.contents[0])[23:31])

    return allDates



#
# Function iterates through all gameFiles in ./local and prints a sentance about the game.
# Inputs: None (Files in ./local)
# Output: Prints Sentence stating which teams played, where they played and at what time.
#

def whoPlayed():
    nameList = []
    for filename in glob.glob('./local/*.xml'):
        tree = ET.parse(filename)
        root = tree.getroot()
        gameTime = root.attrib.get("game_time_et")
        for team in root.findall('team'):
            teams = ''
            if(team.get('type') == 'home'):
                homeTeam = team.get('name_full')
                teams = teams + homeTeam
            if(team.get('type') == 'away'):
                awayTeam = team.get('name_full')
                teams = teams + awayTeam
            nameList.append(teams)
        print(awayTeam + " played at " + homeTeam + " at " + gameTime + " Eastern Time\n")

    
if __name__ == "__main__":
    main()




