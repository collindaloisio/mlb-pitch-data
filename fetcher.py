import sys, urllib, re, urlparse
import fileinput
from bs4 import BeautifulSoup

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
        # Printing link for debug purposes, Can remove this
        print(gameLink)
        # Download the file
        try:
            urllib.urlretrieve(gameLink + 'game.xml', dfileName)
        except:
            print("Could not Download File")
        #Increment counter for uniqueness
        counter = counter + 1

def main():
    mlbSite = "http://gd2.mlb.com/components/game/mlb/"

    date = raw_input('Enter a date YYYYMMDD: ') #prompt for date

    #parse input
    yr= date[0:4]
    mon = date[4:6]
    day = date[6:8]

    #build name
    standardName = 'year_'+yr+'/month_'+mon+'/day_'+day

    #this will be the full Url for some Day
    fullUrl = mlbSite+standardName

    downloadGameFiles(fullUrl)

if __name__ == "__main__":
    main()




