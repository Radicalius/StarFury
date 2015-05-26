#Script For Modloader
#Imports all Mods into the main program

import os

__all__ = []
blacklist = ["__init__.py","__init__.py~","__init__.pyc"] 	#Mod files in this list will not be loaded
					  			#Leave original entries (__init__.py,__init__.py~) in this list
					 		        #If they are not present, it causes a RecursionError
for i in os.listdir("./Mods/"):
	if i not in blacklist:
		__all__.append(i.split(".")[0])
