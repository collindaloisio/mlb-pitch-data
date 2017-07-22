#!/usr/bin/python
import sys, urllib, re, urlparse
import fileinput
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import glob
import os
import settings
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
        urllib.urlretrieve(link, settings.localDir + fileName)
    except:
        print("Could not Download File " + fileName)
        return -1

    with open(settings.localDir + fileName) as f: fileString = f.read()
    if fileString == 'GameDay - 404 Not Found':
        print("File Not found! 404")
        os.remove(settings.localDir + fileName)
        return -1

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
#        segment - Inning of game you want to download, 1-last inning(9+) or "all" for the whole inning_all file
# Output: Downloads specified inning file determined by gameLink_segment to working directory
#

def downloadInningFile(gameLink, segment):

    segLink = '_'+str(segment)+'.xml'
    inningsLink = gameLink + 'inning/inning' + segLink

    return downloadFile(inningsLink, 'inning'+str(segment)+'.xml')


# Pardo's version of downloding inning files
# this function downloads all inning_all.xml files for all games on a given day

def downloadAllInningFiles(dateUrl, counter):

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
    # This is for handling double headers
    for link in soup.find_all("a", string=re.compile("gid")):
        print(type(link.get('href')))
        print(str(link.get('href')[0:28]))
        # Create fileName for file stored locally,
        dfileName = 'inningFile_' + str(link.get('href')[0:29]) + str(counter) + '.xml'
        # Create the URL for the specific file you want
        gameLink = dateUrl + '/' + link.get('href')
        # Open file URL for specific game and download game.xml file
        # Currently only downlods the inning_all.xml
        downloadFile(gameLink+'inning/inning_all.xml', dfileName)
        counter += 1

#
# Function parsePitch. should this be in a seperate parsing package.
# This function takes a filename as a path on system
# Outputs a CQL/SQL string for db insertion
# The file must be an inning_all.xml file
# It also requires a tablename for which you want to insert the data

def parsePitch(filename, table):

    if (os.path.isfile(os.path.abspath(filename))):
        try:
            tree = ET.parse(filename)
        except:
            "Not a valid XML file or string"
            exit(-1)
    else:
        tree = ET.fromstring(filename)


    frontSQL = "INSERT INTO " + str(table) + " (pitcher_id, spin_rate, pitch_type, start_speed, end_speed, nasty, " \
               "outcome_shorthand, atbat_num, outcome, game_id, p_num, inning_num, outs_after_bat) VALUES ("
    backSQL = ");"
    stringList = []
    outList = []

    tree = ET.parse(filename)
    root = tree.getroot()

    #keeps a game id to be used in primary key
    game_id = str(filename)[20:48]


    for inning in root.findall('inning'):

        inning_num = inning.get('num') # get inning number

        # iterate through at bats in top of the inning
        for atbat in inning.iter('atbat'):
            pitcher_id = atbat.get('pitcher')
            atbat_num = atbat.get('num')
            outs_after_bat = atbat.get('o') # how many outs after the batter bats


            # iterate through pitches in atbat
            for pitch in atbat.findall('pitch'):
                spin_rate = pitch.get('spin_rate')
                pitch_type = pitch.get('pitch_type')
                start_speed = pitch.get('start_speed')
                end_speed = pitch.get('end_speed')
                outcome = pitch.get('des')
                nasty = pitch.get('nasty')
                outcome_shorthand = pitch.get('type')
                p_num = pitch.get('id') # these increment weird, can't really discern the pattern

                catString = str(pitcher_id)+','+str(spin_rate)+','+"'"+str(pitch_type)+"'"+','+str(start_speed)+',' + \
                            str(end_speed)+','+str(nasty)+','+"'"+str(outcome_shorthand)+"'"+','+str(atbat_num)+','\
                            +"'"+str(outcome)+"'"+','+"'"+game_id+"'"+','+str(p_num)+','+str(inning_num)+','+ \
                            str(outs_after_bat)
                stringList.append(catString)



    for stri in stringList:
        # build SQL
        out = frontSQL + stri + backSQL
        outList.append(out)
    return(outList)


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




