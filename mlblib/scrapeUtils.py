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
# Function downloadAllInningFiles
# Inputs: date - A date in the format YYYYMMDD
#        eg: 20170520 = May 20 2017
# Output: Downloads ALL inning files when
#

def downloadAllInningFiles(date):

    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    dateUrl = "http://gd2.mlb.com/components/game/mlb/year_" + year + "/month_" + month + "/day_" + day
    counter = 0

    print("Downloading Files:")
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
        print(str(link.get('href')[0:28]))
        # Create fileName for file stored locally,
        dfileName = 'inningFile_' + str(link.get('href')[0:29]) + str(counter) + '.xml'
        # Create the URL for the specific file you want
        gameLink = dateUrl + '/' + link.get('href')
        # Open file URL for specific game and download game.xml file
        # Currently only downlods the inning_all.xml
        downloadFile(gameLink+'inning/inning_all.xml', dfileName)
        counter += 1


#Function floatwrapper returns -1 when there is nothing in the field
#we should almost certainly deal with this differently
def floatwrapper(str):
    if (str is None) | (str == ''):
        return 'valueNotFound'
    else:
        return float(str)

#Function intwrapper returns -1 when there is nothing in the field
#we should almost certainly deal with this differently
def intwrapper(str):
    if (str is None) | (str == ''):
        return 'valueNotFound'
    else:
        return int(str)

def strwrapper(st):
    if (st is None) | (st == ''):
        return 'valueNotFound'
    else:
        return str(st)



#takes a filename and column number
#file should be newline seperated and look like: all_db_columns.txt
#returns a list of tuples representing the dbColumn, xmlColumn, and type
def parseColumns(filename):
    out = []
    with open(filename) as f:
        read_data = f.read().splitlines()
    for line in read_data:
        if line.startswith('--'):
            continue
        lineList = line.split()
        tup = (lineList[0], lineList[1], lineList[2])
        out.append(tup)
    return(out)










#Function parsePitchRewrite is a refactoring of parsepitch that is more scalable and mutable
#Instead of returning a complicated string that we in turn insert into the database, we return a
#list of tuples. Effectively we are returning a mock table for one day's game data.
#Each tuple in the list represents one row of data to insert.
#To insert the whole list of tuples, we iterate through the list and insert each tuple into database one at
#a time.
#In DB package, we will actually batch insert the tuple list as it is fairly simple to do.
#Then, we can open ONE session, call parsePitchRewrite on as many files as we like to insert data for all files
#filename parameter needs to be like: settings.localDir + file
def parsePitchRewrite(filename,columnReference):
    tree = ET.parse(filename)
    root = tree.getroot()
    game_id = str(filename)[20:48]

    dictList = []

    for inning in root.findall('inning'):
        # We always get the inning number
        inning_num = intwrapper(inning.get('num'))

        # iterate through atbats in top of the inning
        for atbat in inning.iter('atbat'):
            #We always get the pitcher_id, atbat_num, and outs_after_bat
            pitcher_id = intwrapper(atbat.get('pitcher'))
            atbat_num = intwrapper(atbat.get('num'))
            outs_after_bat = intwrapper(atbat.get('o'))

            # iterate through pitches in atbat
            for pitch in atbat.findall('pitch'):
                dataDict = {'game_id': game_id, 'inning_num' : inning_num, 'pitcher_id' : pitcher_id,
                            'atbat_num' : atbat_num, 'outs_after_bat' : outs_after_bat}
                # iterate thru second column of table mapping (xml field names)
                for (dbCol,xmlCol,typ) in parseColumns(columnReference):
                    # Mock switch statement to choose wrapper based on field type
                    switchDict = {
                        'int' : intwrapper,
                        'float' : floatwrapper,
                        'text' : strwrapper
                    }
                    field = switchDict[typ](pitch.get(xmlCol))
                    if field == 'valueNotFound':
                        continue
                    dataDict.update({dbCol : field})
                dictList.append(dataDict)
    return(dictList)





#
# Function parsePitch. should this be in a seperate parsing package.
# This function takes a filename as a path on system
# Outputs a CQL/SQL string for db insertion
# The file must be an inning_all.xml file
# It also requires a tablename for which you want to insert the data
#

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

    print(type(spin_rate))

    for stri in stringList:
        # build SQL
        out = frontSQL + stri + backSQL
        outList.append(out)
    return(outList)

#def parseNew(filename, table):
