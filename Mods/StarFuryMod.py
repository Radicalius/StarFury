#This is a base class for a StarFury Mod
#All mods must be child classes of this class

class StarFuryMod(object):
	def __init__(self,name="StarFuryMod",author="Radicalius",version="1.0.0"):
		self.name = name
		self.author = author								#Information to display in modloader menu
		self.version = version
	def mapCreation(self,map,bmap):         						#Function called directly after map creation
		pass									#bmap contains a list of building ids
												#map contains a list of heights
	def serverUpdate(self,map,bmap,players,bullets,bombs,rockets,score,victor):
		pass
	
	def serverComm(self,ss,cmd,g,map,bmap,players,bullets,bombs,rockets,score,victor):
		pass
