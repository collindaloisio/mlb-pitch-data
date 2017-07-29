#README

https://xkcd.com/327/

https://fastballs.wordpress.com/2010/04/18/a-pitchfx-primer/

Introduction to Statistical Learning

http://www-bcf.usc.edu/~gareth/ISL/ISLR%20First%20Printing.pdf


###Overall Objectives of the Application:

This application will be able to predict what Jake Arrieta will pitch next. The user will need
to provide a specific scenario variables such as count, home VS away, pitch count, base runners, batter, etc...
In the backend we will have created a database of all pitch data for pitches thrown by Jake Arrieta.
This data will have been gathered and parced from the MLB website. Then with applied machine learning
algorithms, the algorithm should be able to predict the location and type of pitch to be thrown next.


Below is something Collin wrote a long time ago before we discussed this project.

###Design Plans

A web application for baaseball data analysis is clearly the thing that I have been
meaning to write this whole time. I hadn't seen it yet. But now... Now I do. 

A user pops in. She sees a strikezone -- with a draggable baseball. First though,
she must enter the names of the pitcher or batter she wants to analyze. But we wouldn't want 
to restrict her on that.

Indeed, we could have her look at some type of statistic, and where that happened in the zone.

Point being, dynamic fun scaling tools to analyze interpretivley. 

##Project set up

Create config.py as per config_template.txt

###Installations

Install Cassandra

###Dependent Packages
pip install psycopg2 : this is a postgresql Driver

cassandra, cql, pandas, numpy, scikit-learn, matplotlib
    If this doesn't work follow these steps:
    
    1. git clone https://github.com/datastax/python-dse-driver
    2. Go into the repository and run: 
         sudo python setup.py build
         sudo python setup.py install
    3. You should now have a dse-driver v2.1.0
    3. If you are still having issues related to importing a "loading" module from django,
    uninstall dse package. dse-driver package and dse package are different. 
  

###Standard Ports
Set up Postgresql on Port 5432

###Cassandra Setup
Setup cassandra:

     1. Run ./cassandra
     2. Run ./cqlsh in the cassandra bin
     3. In cqlsh say: 
        CREATE KEYSPACE pitch_test with replication = {'class': 'SimpleStrategy', 'replication_factor' :1};
     4. Run database.createTable()
     5. Download inning files using downloadAllInningFiles
     6. Run cassandra.insertData either use the code below for all files or choose one that you'd like to use

If you want to iterate across all files in local use this code in main:

     for files in os.listdir(settings.localDir):
     if files.endswith('.xml'):
         database.insertData(files)
     else:
         continue

###Gitignore Stuff
Add a personalmain.py to mlb/ to do local test. Git will ignore this file

Add a config.py that follows config_template.txt or else project will not work

###Helpful password storage
From stackechange: By the way, check out the ~/.pgpass file to store password securely and not
in the source code (http://www.postgresql.org/docs/9.2/static/libpq-pgpass.html). libpq, the postgresql client librairy,
check for this file to get proper login information. It's very very handy.

##Current Overview
We have decided to break the project up into modules. This will allow us to import the libraries that we
have created and cleanly use them in the higher level iteration of our project. The Package has been named
mlblib. Inside mlblib, we have the following modules:
   __postgre__ - This is a module that contains functions used for creating/updating our database.
   
   __database__ - This is a module that contains functions for creating/updating a cassandra db. Need to discuss which 
   DB implementation we are using.
   
   __scrapeUtils__ - This is a module that contains functions used in scraping, and parsing data from our various data sources.

The mlblib is interpreted as a package by python because it contains the __init__.py file. Within this file we have the line
' __all__ = ["scrapeUtils", "settings","postgre","config"] '
This line indicates which modules will be included when someone uses the line 
'from mlblib import *' 

In addition to these modules, the mlblib package directory contains a settings.py file and a config.py file. The settings.py
file currently contains global variables such that they don't need to be referenced everywhere throughout the code. I believe
we are unhappy with this implementation right now. The config.py file is an environmental config file. Since everyone's
environment will be different, this file contains environmental specific varriables that each user of this code base must fill out.
It contains the postgrePassword and logFile variables. The postgrePassword is whatever password that connects you to your local
postgres database. The logFile is to specify where you would like the program to write a log to (not implemented currently).
Note: The config.py solution is probably fine long term but settings.py could change.