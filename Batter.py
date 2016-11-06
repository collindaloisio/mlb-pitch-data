#This is a Batter Class that holds Batter name, ID, and some basic statistics
#We can always add stats other than batting avg
class Batter :
	def __init__(self,playerId,name,avg) :
		self.playerId = playerId
		self.name = name
		self.avg = avg
		
