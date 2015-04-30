import sys
import os
import random

width = 9
height = 9

sqrs = {}

class Square(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.val = 0
		self.pos = range(1,9)
	def set(self):
		self.val = random.choice(self.pos)
		for x2 in range(width):
			sqrs[(x2,self.y)].limit(self.val)
		for y2 in range(height):
			sqrs[(self.x,y2)].limit(self.val)
		#cx = self.x/3
		#cy = self.y/3
		#for x1 in range(3):
		#	for y1 in range(3):
		#		sqrs[(x1+cx,y1+cy)].limit(self.val)
	def limit(self,val):
		try:
			self.pos.remove(val)
		except:
			pass

for x1 in range(width):
	for y1 in range(height):
		sqrs[(x1,y1)] = Square(x1,y1)

for x1 in range(width):
	for y1 in range(height):
		sqrs[(x1,y1)].set()

f = open("log.txt",'w')
for x1 in range(width):
	for y1 in range(height):
		if sqrs[(x1,y1,z1)].val>9:
			f.write(str(sqrs[(x1,y1,z1)].val)+" ")
		else:
			f.write(str(sqrs[(x1,y1,z1)].val)+"  ")
	f.write("\n")
