#Game module containing the classes

class Game :
	def __init__(self,URL,date,homeTeam,awayTeam,homePitchers,awayPitchers,inningsPlayed,atBats) :
		self.URL = URL
		self.date = date
		self.homeTeam = homeTeam
		self.awayTeam = awayTeam
		self.homePitchers = homePitchers
		self.awayPitchers = awayPitchers
		self.inningsPlayed = inningsPlayed
		self.atBats = atBats

	def emptygame() :
		self.URL = 0
		self.date = 0
		self.homeTeam = 0
		self.awayTeam = 0
		self.homePitchers = 0
		self.awayPitchers = 0
		self.inningsPlayed = 0
		self.atBats = 0


	#def getAtBat(atBatIndex):


class Pitch :
	def __init__(self,x,y) :
		self.x = x
		self.y = y


class AtBat :
	def __init__(self,pitcherId,batterId,outcome,pitches, balls, strikes):
		self.pitcherId = pitcherId
		self.batterId = batterId
		self.outcome = outcome
		self.pitches = pitches
		self.balls = balls


#This is a Batter Class that holds Batter name, ID, and some basic statistics
#We can always add stats other than batting avg
class Batter :
	def __init__(self,playerId,name,avg) :
		self.playerId = playerId
		self.name = name
		self.avg = avg
		

#This is a Pithcer Class that holds pithcer name, ID, and some basic statistics
#We can always add stats other than ERA
class Pitcher :
	def __init__(self,playerId,name,era) :
		self.playerId = playerId
		self.name = name
		self.era = era
