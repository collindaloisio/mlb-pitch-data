#This is a Pithcer Class that holds pithcer name, ID, and some basic statistics
#We can always add stats other than ERA
class Pitcher :
	def __init__(self,playerId,name,era) :
		self.playerId = playerId
		self.name = name
		self.era = era
