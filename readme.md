#README

https://xkcd.com/327/

SQL Injection is very bad and we should change the way we create sql


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
Install postgreSQL
Install Cassandra

###Dependent Packages
pip install psycopg2 : this is a postgresql Driver

pip install dse-driver : this is a cassandra Driver 


###Standard Ports
Set up Postgresql on Port 5432


###Gitignore Stuff
Add a personalmain.py to mlb/ to do local test. Git will ignore this file
Add a config.py that follows config_template.txt or else project will not work

###Helpful password storage
From stackechange: By the way, check out the ~/.pgpass file to store password securely and not in the source code (http://www.postgresql.org/docs/9.2/static/libpq-pgpass.html). libpq, the postgresql client librairy, check for this file to get proper login information. It's very very handy.
