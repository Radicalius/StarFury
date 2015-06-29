import pygame,random,sys
from pygame import *
import time as ti
from math import *
pygame.init()

bs = {0:10,1:-10,2:-30,3:-20,-2:10,-3:200,5:50,6:50,7:100,8:10,9:25,10:10000,11:10000}

class Score(object):
	def __init__(self):
		self.s1 = 0
		self.s2 = 0
		self.update = False

class Team(object):
	def __init__(self,team):
		self.team = team
		self.bs = 2
		self.gold = 0
		self.range = 2
		self.hb = 0
class Lock(object):
	def __init__(self):
		self.lock = False
	def lock(self):
		self.lock = True
	def get(self):
		return self.lock
	
font = pygame.font.Font("font.ttf",12)

stats = {"Ammo":0,"Speed":1,"Handling":2,"Cal":12,"RoF":3,"BS":4,"Range":5,"Amp":6,"Cooldown":7,"Duration":8,"AoE":9,"HS":10,"HB":11,"Caliber":12,"RR":13,"Slot":14,"SAP":15,"RAP":16,"BAP":17}

class Component(object):
	def __init__(self,name,char,image,stats,modified,active,semiactive,passive,fname=""):
		self.ammo = stats[0]
		self.sstat = stats[1]
		self.mstat = stats[2]
		self.rof = stats[3]
		self.bs = stats[4]
		self.range = stats[5]
		self.amp = stats[6]
		self.cooldown = stats[7]
		self.powstat = stats[8]
		self.aoe = stats[9]
		self.hs = stats[10]
		self.hb = stats[11]
		self.cal = stats[12]
		self.rr = stats[13]
		self.img = image
		self.name = name
		self.char = char
		self.slot = stats[14]
		self.modified = modified
		self.fname = fname
		self.sap = stats[15]
		self.rap = stats[16]
		self.bap = stats[17]
		self.active = active
		self.semiactive = semiactive
		self.passive = passive
	@staticmethod
	def load(fname):
		f = open("Components/"+fname,"r")
		cont = f.readlines()
		name = "Comp"
		char = ""
		image = "blank.png"
		a = None
		sa = None
		p = None
		modified = []
		s = [0]*18
		for l in cont:
			h = l.split(" ")
			g = l.split("=")
			if len(g)>1:
				if g[0].strip() == "Name":
					name = g[1]
				if g[0].strip() == "Char":
					char = g[1]
				if g[0].strip() == "Image":
					image = g[1]
				if g[0].strip() == "Active":
					a = g[1].strip()
				if g[0].strip() == "SemiActive":
					sa = g[1].strip()
				if g[0].strip() == "Passive":
					p = g[1].strip()
			elif len(h)>1:
				mult = h[0]
				stat = h[1].strip()
				modified.append([stat,mult])
				if mult[0] == "+":
					mult = mult[1:]
				mult = float(mult)
				s[stats[stat]]+=mult
		return Component(name,char,image,s,modified,a,sa,p,fname=fname) 
	def add(self,i):
		i.ammo+=self.ammo
		i.sstat+=self.sstat
		i.mstat+=self.mstat
		i.rof+=self.rof
		i.bs+=self.bs
		i.range+=self.range
		i.amp+=self.amp
		i.cooldown+=self.cooldown
		i.powstat+=self.powstat
		i.aoe+=self.aoe
		i.hs+=self.hs
		i.hb+=self.hb
		i.cal+=self.cal
		i.rr+=self.rr
		i.sap+=self.sap
		i.bap+=self.bap
		i.rap+=self.rap
		if self.passive!=None: 
			i.passives.append(self.passive)
		if self.semiactive!=None:
			i.actives.append([self.semiactive,"semi",False])
		if self.active!=None:
			i.actives.append([self.active,"full",False])
	def upgrade(self,i):
		i.ammo-=self.ammo
		i.sstat-=self.sstat
		i.mstat-=self.mstat
		i.rof-=self.rof
		i.bs-=self.bs
		i.range-=self.range
		i.amp-=self.amp
		i.cooldown-=self.cooldown
		i.powstat-=self.powstat
		i.aoe-=self.aoe
		i.hs-=self.hs
		i.hb-=self.hb
		i.cal-=self.cal
		i.rr-=self.rr
		self.ammo*=1.25
		self.sstat*=1.25
		self.mstat*=1.25
		self.rof*=1.25
		self.bs*=1.25
		self.range*=1.25
		self.amp*=1.25
		self.cooldown*=1.25
		self.powstat*=1.25
		self.aoe*=1.25
		self.hs*=1.25
		self.hb*=1.25
		self.cal*=1.25
		self.rr*=1.25
		i.ammo+=self.ammo
		i.sstat+=self.sstat
		i.mstat+=self.mstat
		i.rof+=self.rof
		i.bs+=self.bs
		i.range+=self.range
		i.amp+=self.amp
		i.cooldown+=self.cooldown
		i.powstat+=self.powstat
		i.aoe+=self.aoe
		i.hs+=self.hs
		i.hb+=self.hb
		i.cal+=self.cal
		i.rr+=self.rr
	def render(self,screen,x,mx,my,mp,s,host):
		screen.blit(pygame.image.load("Images/"+self.img.strip()).convert_alpha(),(x*75+430-556/2+50,322/2+340-50))
		g = 0
		if mx>x*75+430-556/2+50 and mx<x*75+430-556/2+50+25 and my>322/2+340-50 and my<322/2+340-25:
			for i in self.modified:
				d = font.render(i[0]+" "+i[1],True,(255,255,255))
				screen.blit(d,(x*75+430-556/2+62.5-d.get_width()/2,322/2+340-25+g*12))
				g+=1
		print mp
		if mx>x*75+430-556/2+50 and mx<x*75+430-556/2+50+25 and my>322/2+340-50 and my<322/2+340-25 and mp:
			s.sendto("9 "+str(x),host)
			mp = False
		

comps = [[Component.load("wasp.hull"),Component.load("iondrive.cmp"),Component.load("largetail.cmp"),Component.load("ammobox.cmp"),Component.load("autocannon.cmp")],[Component.load("osprey.hull"),Component.load("irscanner.cmp"),Component.load("rockettubes.cmp"),Component.load("powercore.cmp"),Component.load("flakcannon.cmp"),Component.load("thrusters.cmp")],[Component.load("raptor.hull"),Component.load("thrusters.cmp"),Component.load("largetail.cmp"),Component.load("bombclip.cmp"),Component.load("bombbay.cmp"),Component.load("cloakingdevice.cmp"),Component.load("heatsink.cmp")]]

class Player(object):
	def __init__(self,call,addr,comps,team,af,hull):
		self.ai = False
		self.x = 0
		self.sx = 0
		self.falling = False
		self.ftime = 0
		self.sy = 0
		self.ax = 0
		self.addr = addr
		self.y = 340
		print team
		if team == 1:
			self.rt = 180
		else:
			self.rt = 0
		self.gold = 1000
		self.alive = False
		self.airfield = af
		self.landed = False
		self.call = call
		#self.class_ = clas
		self.team = team
		self.rth = 0
		self.stealth = False
		self.speed = 0
		self.slock = Lock()
		self.expd = True
		self.mark = False
		self.gun = 0
		self.bomb = 0
		self.mx = 0
		self.my = 0
		self.comps = comps
		self.hull = hull
	#################################
		self.ammo = 0
		self.sstat = 0
		self.mstat = 0
		self.rof = 0
		self.bs = 0
		self.range = 0
		self.amp = 0
		self.cooldown = 0
		self.powstat = 0
		self.aoe = 0
		self.hs = 0
		self.hb = 0
		self.cal = 0
		self.rr = 0
		self.rap = 0
		self.bap = 0
		self.sap = 0
	#################################
		self.dtime = ti.time()-20
		self.powmax = 250.*pow(1.25,self.powstat)
		self.powdur = self.powmax
		self.rocket = 0
		self.lastmissle = 0
		self.lastshot = 0
		self.lastbomb = 0
		self.bombs = 0
		self.shots = 0
		self.rockets = 0
		self.light = None
		self.actives = []
		self.semiactives = []
		self.passives = []
		#if self.class_ == "fighter":
		#	self.sstat+=0.5
		#	self.comps = comps[0]
		#	self.shots = pow(1.25,self.ammo)*20
		#	self.bombs = 0
		#	self.rockets = 0
		#	for i in comps[0]:
		#		i.add(self)
		#if self.class_ == "interceptor":
		#	self.comps = comps[1]
		#	self.shots = pow(1.25,self.ammo)*10
		#	self.speed = pow(1.25,self.sstat)
		#	self.rockets = pow(1.25,self.ammo)*5
		#	self.bombs = 0
		#	for i in comps[1]:
		#		i.add(self)
		#if self.class_ == "bomber":
		#	self.sstat-=0.5
		#	self.hb-=0.5
		#	self.comps = comps[2]
		#	self.shots = pow(1.25,self.ammo)*10
		#	self.speed = pow(1.25,self.sstat)
		#	self.bombs = pow(1.25,self.ammo)*15
		#	self.rockets = 0
		#	for i in comps[2]:
		#		i.add(self)
		for i in self.comps:
			i.add(self)
		total = self.sap+self.bap+self.rap
		if total!=0:
			self.shots = pow(1.25,self.ammo)*20*(self.sap/total)
			self.bombs = pow(1.25,self.ammo)*20*(self.bap/total)
			self.rockets = pow(1.25,self.ammo)*20*(self.rap/total)
		else:
			self.shots = 0
			self.bombs = 0
			self.rockets = 0
		self.speed = 0
	def lock(self,a):
		self.slock.lock()
		print self.slock.lock
	def render(self,screen,call,scrollx,map,exp,bmap,bullets,bombs,rockets,players,score,lighting,mods):
		global score1,score2
		if self.light == None:
			self.light = Light(0,0,(0,0,255),0.3,100)
		if self.alive:
			if self.stealth or self.mark or self.speed>pow(1.25,self.sstat):
				self.powdur-=1
			else:
				if self.powdur<250.*pow(1.25,self.powstat):
					self.powdur+=0.5*pow(1.25,self.cooldown)
			if self.powdur<=0:
				self.stealth = False
				self.mark = False
				self.speed = pow(1.25,self.sstat)
			if self.y<0 and not self.falling:
				self.falling = True
				self.ftime = 0
			if self.x<0:
				rtw = -atan2(self.y-(self.my),-(self.mx-(430+self.x)))*180./pi+180
			elif self.x>500*20-800:
				print "IN"
				rtw = -atan2(self.y-(self.my),-(self.mx-(430+self.x-scrollx)))*180./pi+180
			else:
				rtw = -atan2(self.y-(self.my),-(self.mx-430))*180./pi+180
			rts = atan2(cos(self.rt*pi/180),-sin(self.rt*pi/180))*180./pi
			if (rtw-rts+90)%360 == 0:
				self.rth = 0
			elif (rtw-rts+90)%360<180:
				self.rth = 1
			else:
				self.rth = -1
			print self.mx,self.my
			if not self.falling:
				self.rt+=self.rth*pow(1.25,self.mstat)*2
				#self.rt = -atan2((self.my)-340,self.mx-430)*180./pi
				self.x+=cos(self.rt*pi/180)*self.speed*2
				self.y-=sin(self.rt*pi/180)*self.speed*2
			else:
				self.x+=cos(self.rt*pi/180)*self.speed*2
				if self.y<75:
					self.y+=pow(self.ftime,2)/1000.
				else:
					self.y+=pow(140-self.ftime,2)/1000
				self.ftime+=1
				if self.y>150:
					self.falling = False
			if (call == self.call) and self.x<500*20-800 and self.x>0:
				if not self.stealth:
					fighter = pygame.image.load("Images/"+self.hull.img.split(".")[0]+str(self.team)+".png").convert_alpha()
				else:
					fighter = pygame.image.load("Images/"+"bombers.png").convert_alpha()
				if (self.rt%360>90 and self.rt%360<270):
					fighter = pygame.transform.flip(fighter,False,True)
				f2 = pygame.transform.rotate(fighter,self.rt)
				screen.blit(f2,(430-f2.get_width()/2,self.y-f2.get_height()/2))
				self.light.x = 430
				self.light.y = self.y
				self.light.render(lighting)
			else:
				label = font.render(self.call,True,(155,155,155))
				fighter = pygame.image.load("Images/"+self.hull.img.split(".")[0]+str(self.team)+".png").convert_alpha()
				if (self.rt%360>90 and self.rt%360<270):
					fighter = pygame.transform.flip(fighter,False,True)
				f2 = pygame.transform.rotate(fighter,self.rt)
				if not self.stealth:
					if self.call!=call:
						screen.blit(label,(430+self.x-label.get_width()/2-scrollx,self.y-label.get_height()/2-25))
					screen.blit(f2,(430+self.x-f2.get_width()/2-scrollx,self.y-f2.get_height()/2))
					if self.call == "zac1":
						print (430+self.x-f2.get_width()/2-scrollx,self.y-f2.get_height()/2)
				if players[call].mark == True:
					try:
						screen.blit(pygame.image.load("Images/"+"mark.png").convert_alpha(),(430+random.randint(-30*pow(1.25,self.amp-players[call].hb),30*pow(1.25,self.amp-players[call].hb))+self.x-20-scrollx,self.y+random.randint(-30*pow(1.25,self.amp-players[call].hb),30*pow(1.25,self.amp-players[call].hb))-20))
					except:
						pass
			if (self.y>680-map[int(self.x+430)/20]*20+20):
				self.alive = False
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				if bmap[int(self.x+430)/20]!=-2 and bmap[int(self.x+430)/20]!=-3:
					self.alive = False
					bmap[int(self.x+430)/20] = -1
				else:
					if bmap[int(self.x+430)/20]==-2: 
						if not self.landed:
							if self.x<500*10:
								self.speed = 0.5
								self.y = 680-map[int(self.x+430)/20]*20+10
								self.rt = 180
							else:
								self.speed = 0.5
								self.y = 680-map[int(self.x+430)/20]*20+10
								self.rt = 0
					if bmap[int(self.x+430)/20]==-3 and not self.landed:
						self.speed = 0
						if self.x<5000:
							self.rt = 180
						else:
							self.rt = 0
						self.y = 680-map[int(self.x+430)/20]*20+10
						self.landed = True
						total = self.sap+self.bap+self.rap
						if total!=0:
							self.shots = pow(1.25,self.ammo)*20*(self.sap/total)
							self.bombs = pow(1.25,self.ammo)*20*(self.bap/total)
							self.rockets = pow(1.25,self.ammo)*20*(self.rap/total)
						else:
							self.shots = 0
							self.bombs = 0
							self.rockets = 0
						#if self.class_ == "fighter":
						#	self.shots = pow(1.25,self.ammo)*20
						#	self.bombs = 0
						#	self.rockets = 0
						#if self.class_ == "interceptor":
						#	self.shots = pow(1.25,self.ammo)*10
						#	self.speed = pow(1.25,self.sstat)
						#	self.rockets = pow(1.25,self.ammo)*5
						#	self.bombs = 0
						#if self.class_ == "bomber":
						#	self.shots = pow(1.25,self.ammo)*10
						#	self.speed = pow(1.25,self.sstat)
						#	self.bombs = pow(1.25,self.ammo)*15
						#	self.rockets = 0
							self.speed = 0
			else:
				self.landed =  False
			for i in self.passives:
				if i == "Coin":
					self.gold+=0.01
			for i in self.actives:
				if self.powdur>0:
					if i[0] == "Thrust":	
						if i[2]:
							self.speed = pow(1.25,self.sstat)*2
						if not i[2] and self.speed == pow(1.25,self.sstat)*2:
							self.speed = pow(1.25,self.sstat)
					if i[0] == "Blink" and i[2] and self.powdur>=250:
						self.x+=cos(self.rt*pi/180)*self.speed*400
						self.y-=sin(self.rt*pi/180)*self.speed*400
						self.powdur-=250				
				
			if self.gun == 1 and ti.time()-self.lastshot>1/5.*pow(1.25,-self.rof) and self.shots>0:
				self.lastshot = ti.time()
				self.shots-=1
				#if self.class_ != "bomber":
				bullets.append(Bullet(self.x+cos(self.rt*pi/180)*15,self.y-sin(self.rt*pi/180)*15,self.rt,self))
				#else:
				#	bullets.append(Bullet(self.x+cos(self.rt*pi/180)*-15,self.y-sin(self.rt*pi/180)*-15,180+self.rt,self))
			if self.bomb == 1 and ti.time()-self.lastbomb>1/5.*pow(1.25,-self.rof) and self.bombs>0:
				self.lastbomb = ti.time()
				self.bombs-=1
				bombs.append(Bomb(self,self.x,self.y,-sin(self.rt*pi/180)*self.speed,cos(self.rt*pi/180)*self.speed))
			if self.rocket == 1 and ti.time()-self.lastmissle>1/5.*pow(1.25,-self.rof) and self.rockets>0:
				self.lastmissle = ti.time()
				self.rockets-=1
				rockets.append(Rocket(self.x+cos(self.rt*pi/180)*15,self.y-sin(self.rt*pi/180)*15,self.rt,self,self))
			for i in bullets:
				if i.alive:
					if (sqrt(pow(self.x-i.x,2)+pow(self.y-i.y,2)<100*pow(1.25,self.hb)+5*pow(1.25,i.hb))):
						#self.alive = False
						i.alive = False
						if i.master.team!=self.team:
							i.master.gold+=100
							if i.master.team == "1":
								score.s1+=100
							else:
								score.s2+=100
						else:
							i.master.gold-=100
							if i.master.team == "1":
								score.s1-=100
							else:
								score.s2-=100
			for i in rockets:
				if i.alive:
					if (sqrt(pow(self.x-i.x,2)+pow(self.y-i.y,2)<100*pow(1.25,self.hb)+5*pow(1.25,i.hb))):
						#self.alive = False
						i.alive = False
						if i.master.team!=self.team:
							i.master.gold+=100
							if i.master.team == "1":
								score.s1+=100
							else:
								score.s2+=100
						else:
							i.master.gold-=100						
							if i.master.team == "1":
								score.s1-=100
							else:
								score.s2-=100
			#if self.x>self.sx:
			#	self.x-=0.1
			#if self.x<self.sx:
			#	self.x+=0.1
			#if self.y>self.sy:
		#		self.y-=0.3
			#if self.y<self.sy:
			#	self.y+=0.3
			#print self.x-self.sx
			#if self.slock.get():
			#	print "in"
			#	self.speed = pow(1.25,self.sstat)
			
		else:
			print True
			if not self.expd:
				self.dtime = ti.time()
				exp.append(Explosion(self.x,self.y,4))
				self.gold-=25
				if self.team == "1":
					score.s1-=25
				else:
					score.s2-=25
				self.expd = True
			if ti.time()-self.dtime>10*pow(1.25,-self.rr) and self.airfield!=-1 and bmap[self.airfield]!=-1:
				#self.x = self.airfield*20+810
				#self.y = 680-map[self.airfield]*20+10
				self.expd = False
				self.alive = True
				self.speed = 0
				if self.x<5000:
					self.rt = 180
				else:
					self.rt = 180
				self.landed = True	
		for i in mods:
			i.playerRender(self,screen,call,scrollx,map,exp,bmap,bullets,bombs,rockets,players,score,lighting)	
			i.playerRun(self,call,map,exp,bmap,bullets,bombs,rockets,players,score)

	def run(self,map,bmap,bullets,bombs,rockets,score,ss,players,mods):
		if self.alive:
			if self.stealth or self.mark or self.speed>pow(1.25,self.sstat):
				self.powdur-=1
			else:
				if self.powdur<250*pow(1.25,self.powstat):
					self.powdur+=0.5*pow(1.25,self.cooldown)
			if self.powdur<=0:
				self.stealth = False
				self.mark = False
				self.speed = pow(1.25,self.sstat)
			if self.y<0 and not self.falling:
				self.falling = True
				self.ftime = 0
			if self.x<0:
				rtw = -atan2(self.y-(self.my),-(self.mx-(430+self.x)))*180./pi+180
			elif self.x>500*20-800:
				rtw = -atan2(self.y-(self.my),-(self.mx-(430+self.x-(500*20-800))))*180./pi+180
			else:
				rtw = -atan2(self.y-(self.my),-(self.mx-430))*180./pi+180
			rts = atan2(cos(self.rt*pi/180),-sin(self.rt*pi/180))*180./pi
			if (rtw-rts+90)%360 == 0:
				self.rth = 0
			elif (rtw-rts+90)%360<180:
				self.rth = 1
			else:
				self.rth = -1
			if not self.falling:
				self.rt+=self.rth*pow(1.25,self.mstat)
				self.x+=cos(self.rt*pi/180)*self.speed
				self.y-=sin(self.rt*pi/180)*self.speed
			else:
				self.x+=cos(self.rt*pi/180)*self.speed
				if self.y<75:
					self.y+=pow(self.ftime,2)/1000.
				else:
					self.y+=pow(140-self.ftime,2)/1000
				self.ftime+=1
				if self.y>150:
					self.falling = False
			if (self.y>680-map[int(self.x+430)/20]*20+20):
					self.alive = False
					print "It was the ground",self.x
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				if bmap[int(self.x+430)/20]!=-2 and bmap[int(self.x+430)/20]!=-3:
					self.alive = False
					bmap[int(self.x+430)/20] = -1
				else:
					if bmap[int(self.x+430)/20]==-2: 
						if not self.landed:
							self.speed = 0.5
							if self.x<5000:
								self.rt = 180
							else:
								self.rt = 0
							self.y = 680-map[int(self.x+430)/20]*20+10
					if bmap[int(self.x+430)/20]==-3 and not self.landed:
						self.speed = 0
						if self.x<5000:
							self.rt = 0
						else:
							self.rt = 180
						self.y = 680-map[int(self.x+430)/20]*20+10
						self.landed = True
						total = self.sap+self.bap+self.rap
						if total!=0:
							self.shots = pow(1.25,self.ammo)*20*(self.sap/total)
							self.bombs = pow(1.25,self.ammo)*20*(self.bap/total)
							self.rockets = pow(1.25,self.ammo)*20*(self.rap/total)
						else:
							self.shots = 0
							self.bombs = 0
							self.rockets = 0
						#if self.class_ == "fighter":
						#	self.shots = pow(1.25,self.ammo)*20
						#	self.bombs = 0
						#	self.rockets = 0
						#if self.class_ == "interceptor":
						#	self.shots = pow(1.25,self.ammo)*10
						#	self.speed = pow(1.25,self.sstat)
						#	self.rockets = pow(1.25,self.ammo)*5
						#	self.bombs = 0
						#if self.class_ == "bomber":
						#	self.shots = pow(1.25,self.ammo)*10
						#	self.speed = pow(1.25,self.sstat)
						#	self.bombs = pow(1.25,self.ammo)*15
						#	self.rockets = 0
						self.speed = 0
			else:
				self.landed =  False
			for i in self.passives:
				if i == "Coin":
					self.gold+=0.1
			for i in self.actives:
				if self.powdur>0:
					if i[0] == "Thrust":	
						if i[2]:
							self.speed = pow(1.25,self.sstat)*2
						if not i[2] and self.speed == pow(1.25,self.sstat)*2:
							self.speed = pow(1.25,self.sstat)
					if i[0] == "Blink" and i[2] and self.powdur>=250:
						self.x+=cos(self.rt*pi/180)*self.speed*400
						self.y-=sin(self.rt*pi/180)*self.speed*400
						self.powdur-=250			
				
			if self.gun == 1 and ti.time()-self.lastshot>1/5.*pow(1.25,self.cooldown) and self.shots>0:
				self.lastshot = ti.time()
				self.shots-=1
				#if self.class_ != "bomber":
				bullets.append(Bullet(self.x+cos(self.rt*pi/180)*15,self.y-sin(self.rt*pi/180)*15,self.rt,self))
				#else:
				#bullets.append(Bullet(self.x+cos(self.rt*pi/180)*-15,self.y-sin(self.rt*pi/180)*-15,180+self.rt,self))
			if self.bomb == 1 and ti.time()-self.lastbomb>1/5.*pow(1.25,self.cooldown) and self.bombs>0:
				self.lastbomb = ti.time()
				self.bombs-=1
				bombs.append(Bomb(self,self.x,self.y,-sin(self.rt*pi/180)*self.speed,cos(self.rt*pi/180)*self.speed))
			if self.rocket == 1 and ti.time()-self.lastmissle>1/5.*pow(1.25,self.cooldown) and self.rockets>0:
				self.lastmissle = ti.time()
				self.rockets-=1
				rockets.append(Rocket(self.x+cos(self.rt*pi/180.)*15.,self.y-sin(self.rt*pi/180.)*15,self.rt,self,self))
			for i in bullets:
				if (sqrt(pow(self.x-i.x,2)+pow(self.y-i.y,2)<100*pow(1.25,self.hb)+5*pow(1.25,i.hb))) and i.master!=self and i.alive:
					self.alive = False
					i.alive = False
					if i.master.team!=self.team:
						i.master.gold+=100
						if i.master.team == "1":
							score.s1+=100
						else:
							score.s2+=100
					else:
						i.master.gold-=100
						if i.master.team == "1":
							score.s1-=100
						else:
							score.s2-=100
					score.update = True
			for i in rockets:
				if i.alive:
					if (sqrt(pow(self.x-i.x,2)+pow(self.y-i.y,2)<100*pow(1.25,self.hb)+5*pow(1.25,i.hb))) and i.master!=self:
						self.alive = False
						i.alive = False
						if i.master.team!=self.team:
							i.master.gold+=1
							if i.master.team == "1":
								score.s1+=100
							else:
								score.s2+=100
						else:
							if i.master.team == "1":
								score.s1-=100
							else:
								score.s2-=100
						score.update = True
		else:
			if not self.expd:
				for i in players.keys():
					if not players[i].ai:
						ss.sendto("16 "+self.call,players[i].addr)
				self.dtime = ti.time()
				self.gold-=25
				if self.team == "1":
					score.s1-=25
				else:
					score.s2-=25
				score.update = True
				self.expd = True
			if ti.time()-self.dtime>10*pow(1.25,-self.rr) and bmap[self.airfield]!=-1:
				if self.team == "1":
					if len(players)<3:
						self.x = self.airfield*20-420
					else:
						self.x = self.airfield*20+420-10*20
				else:
					self.x = self.airfield*20-340
				self.y = 680-map[(self.x+430)/20]*20+10
				self.expd = False
				self.alive = True
				self.speed = 0
				if self.x<5000:
					self.rt = 0
				else:
					self.rt = 180	
				self.landed = True
		for i in mods:	
			i.playerRun(self,None,map,exp,bmap,bullets,bombs,rockets,players,score)

class Bot(Player):
	def __init__(self,call,clas,team,af):
		super(Bot,self).__init__(call,None,clas,team,af)
		self.ai = True
		self.mode = 0
		self.lrth = 0
		self.lspeed = 0
	def run(self,map,bmap,bullets,bombs,rockets,score,ss,players):
		super(Bot,self).run(map,bmap,bullets,bombs,rockets,score,ss,players)
		if self.landed:
			self.speed = pow(1.25,(self.amp+self.sstat))
			self.mode = 0
		if self.mode == 0:
			if self.y>300:
				if abs(cos((self.rt-90)*pi/180))<0.707:
					if self.team == "1":
						self.rth=1
					else:
						self.rth=-1
				else:
					self.rth = 0
			else:
				self.mode = 1
		if self.mode == 1:
			if abs(cos((self.rt-90)*pi/180))>0.01:
					if self.team == "1":
						self.rth=-1
					else:
						self.rth=1
			else:
				self.mode = 2	
				self.rth = 0			
		if self.lrth!=self.rth:
			for i in players.keys():
				if not players[i].ai:
					ss.sendto("4 "+self.call+" "+str(self.rth),players[i].addr)
			self.lrth = self.rth
		if self.lspeed!=self.speed:
			for i in players.keys():
				if not players[i].ai:
					#ss.sendto("19 "+self.call+" "+str(self.speed),players[i].addr)
					ss.sendto("19 "+self.call+" "+str(self.speed),players[i].addr)
			#self.lspeed = self.speed
		

class Bullet(object):
	def __init__(self,x,y,rt,master,id=random.randint(0,1000)):
		self.x = x
		self.y = y
		self.rt = rt
		self.id = id
		self.master = master
		self.speed = 5*pow(1.25,self.master.bs)
		self.range = 500*pow(1.25,self.master.range)
		self.hb = 5*pow(1.25,self.master.hb)
		self.alive = True
		self.played = False
	def render(self,screen,scrollx,map,bmap):
		if self.alive:
			if not self.played:
				self.sound = pygame.mixer.Sound("Sounds/"+"laser.wav")
				dist = scrollx-self.x
				right = (0.5+dist/10000.*0.5)/(1+dist/10000.)
				left = (1-right)/(1+dist/10000.)
				print left,right
				try:
					self.sound.play().set_volume(left,right)
					self.played = True
				except:	
					self.played = True
			global score1,score2
			self.x+=cos(self.rt*pi/180)*self.speed*2
			self.y-=sin(self.rt*pi/180)*self.speed*2
			self.range-=self.speed
			if self.range<0:
				self.alive = False
			b = pygame.image.load("Images/"+"bullet.png").convert_alpha()
			screen.blit(b,(self.x+430-scrollx,self.y))
			try:
				if (self.y>680-map[int(self.x+430)/20]*20+20):
					self.alive = False
				if (bmap[int(self.x+430)/20]!=-1 and bmap[int(self.x+430)/20]!=-2 and bmap[int(self.x+430)/20]!=-3 and self.y>680-map[int(self.x+430)/20]*20):
					self.alive = False
			except:
				self.alive=False
			if self.y<0:
				self.alive = False
	def run(self,map,bmap):
		if self.alive:
			self.x+=cos(self.rt*pi/180)*self.speed
			self.y-=sin(self.rt*pi/180)*self.speed
			self.range-=self.speed
			if self.range<0:
				self.alive = False
			try:
				if (self.y>680-map[int(self.x+430)/20]*20+20 or self.y<0):
					self.alive = False
				if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
						self.alive = False
			except:
				self.alive = False

class Bomb(object):
	def __init__(self,master,x,y,vu,vx):
		self.x = x
		self.y = y
		self.rt = 0
		self.vu = -vu
		self.a = 10
		self.vx = vx
		self.vd = 0
		self.alive = True
		self.expd = False
		self.lock = False
		self.master = master
		self.played = False
	def run(self,bmap,map,score,players):
		if self.alive:
			self.x+=self.vx
			self.y-=self.vu
			self.y+=self.vd
			self.vd+=self.a/140.
			if (self.y>680-map[int(self.x+430)/20]*20+20):
				self.alive = False
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				self.alive = False	
				if self.master.team == "1":
					score.s1+=bs[bmap[int(self.x+430)/20]]
					self.master.gold+=bs[bmap[int(self.x+430)/20]]
				if self.master.team == "2":
					score.s2+=bs[bmap[int(self.x+430)/20]]
					self.master.gold+=bs[bmap[int(self.x+430)/20]]
				if bmap[int(self.x+430)/20] == 5:
					if self.x<5000:
						bmap[int(self.x+430)/20+7] = 6
					else:
						bmap[int(self.x+430)/20-7] = 6
				if bmap[int(self.x+430)/20] == -3:
					for i in players.keys():
						if int(self.x+430)/20 == players[i].ax:
							if players[i].team == "1":
								if players[i].airfield>0:
									players[i].airfield-=1
								elif players[i].airfield!=2:
									players[i].airfield+=1
								else:
									players[i].airfield = -1
							else:
								if players[i].airfield<5:
									players[i].airfield+=1
								elif players[i].airfield!=3:
									players[i].airfield-=1
								else:
									players[i].airfield = -1
				bmap[int(self.x+430)/20] = -1
				score.update = True
			x = 0
			for i in bmap:
				if i == 4:
					if (sqrt(pow(self.x+430-x,2)+pow(self.y-(680-map[int(self.x+430)/20]*20),2))<100):
						self.alive = False
				x+=20			
			if self.y<0:
				self.alive = False
		return bmap
	def render(self,screen,scrollx,map,bmap,exp,score,players):
		if not self.played:
			self.sound = pygame.mixer.Sound("Sounds/"+"bombfall.wav")
			dist = scrollx-self.x
			right = (0.5+dist/10000.*0.5)/(1+dist/10000.)
			left = (1-right)/(1+dist/10000.)
			print left,right
			try:
				self.sound.play().set_volume(left,right)
				self.played = True
			except:	
				self.played = True
		if self.alive:
			self.x+=self.vx*2
			self.y-=self.vu*2
			self.y+=self.vd*2
			self.vd+=self.a/140.*2
			img = pygame.image.load("Images/"+"bomb.png").convert_alpha()
			screen.blit(img,(self.x+430-scrollx,self.y))
			if (self.y>680-map[int(self.x+430)/20]*20+20):
				self.alive = False
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				self.alive = False
				if self.master.team == "1":
					score.s1+=bs[bmap[int(self.x+430)/20]]
					self.master.gold+=bs[bmap[int(self.x+430)/20]]
				if self.master.team == "2":
					score.s2+=bs[bmap[int(self.x+430)/20]]
					self.master.gold+=bs[bmap[int(self.x+430)/20]]
				if bmap[int(self.x+430)/20] == 5:
					if self.x<5000:
						bmap[int(self.x+430)/20+7] = 6
					else:
						bmap[int(self.x+430)/20-7] = 6
				if bmap[int(self.x+430)/20] == -3:
					for i in players.keys():
						if int(self.x+430)/20 == players[i].ax:
							if players[i].team == "1":
								if players[i].airfield>0:
									players[i].airfield-=1
								elif players[i].airfield!=2:
									players[i].airfield+=1
								else:
									players[i].airfield = -1
							else:
								if players[i].airfield<5:
									players[i].airfield+=1
								elif players[i].airfield!=3:
									players[i].airfield-=1
								else:
									players[i].airfield = -1
				bmap[int(self.x+430)/20] = -1
		else:
			self.sound.stop()
			if not self.expd:
				self.sound = pygame.mixer.Sound("Sounds/"+"explosion.wav")
				dist = scrollx-self.x
				right = (0.5+dist/10000.*0.5)/(1+dist/10000.)
				left = (1-right)/(1+dist/10000.)
				print left,right
				try:
					self.sound.play().set_volume(left,right)
					self.played = True
				except:	
					self.played = True
				self.expd = True
				if self.lock:
					exp.append(Explosion(self.x,self.y,2))
				else:
					exp.append(Explosion(self.x,680-20*(map[int(self.x+430)/20]-1),2))

class Rocket(object):
	def __init__(self,x,y,rt,target,master):
		self.x = x
		self.y = y
		self.master = master
		self.speed = 5*pow(1.25,self.master.bs)
		self.range = 500*pow(1.25,self.master.range)
		self.hb = 5*pow(1.25,self.master.hb)
		self.rt = rt
		self.alive = True
		self.expd = False
		self.target = target
		try:
			self.sound = pygame.mixer.Sound("Sounds/"+"rocket.wav")
			self.sound.play()
		except:
			pass
	def render(self,screen,scrollx,map,bmap,mx,my,exp):
		if self.alive:
			self.x+=cos(self.rt*pi/180)*self.speed*2
			self.y-=sin(self.rt*pi/180)*self.speed*2
			self.range-=self.speed
			if self.range<0:
				self.alive = False
			self.rt = -atan2(self.y-(self.target.my),self.x-(self.target.mx-430+scrollx))*180./pi+180
			if (self.y>680-map[int(self.x+430)/20]*20+20):
				self.alive = False
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				self.alive = False
			img = pygame.transform.rotate(pygame.image.load("Images/"+"missle.png").convert_alpha(),self.rt)
			screen.blit(img,(self.x+430-scrollx-img.get_width()/2,self.y-img.get_height()/2))
		else:
			self.sound.stop()
			if not self.expd:
				self.expd = True
				exp.append(Explosion(self.x,self.y,1))
	def run(self,map,bmap):
		if self.alive:
			self.x+=cos(self.rt*pi/180)*5
			self.y-=sin(self.rt*pi/180)*5
			self.range-=5
			if self.range<0:
				self.alive = False
			self.rt = -atan2(self.y-(self.target.my),self.x-(self.target.mx-430))*180./pi+180
			if (self.y>680-map[int(self.x+430)/20]*20+20):
				self.alive = False
			if (bmap[int(self.x+430)/20]!=-1 and self.y>680-map[int(self.x+430)/20]*20):
				self.alive = False

class Explosion(object):
	def __init__(self,x,y,rad):
		self.x = x
		self.y = y
		self.count = 0.1
		#self.light = Light(self.x,self.y,(255,255,255),0.3,1)
		self.radius = rad
		self.flip = False
		try:
			self.sound = pygame.mixer.Sound("Sounds/"+"exp.wav")
			self.sound.play()
		except:
			pass
	def render(self,screen,scrollx,lighting):
		if self.count>0:
			self.img = pygame.image.load("Images/"+"explosion.png").convert_alpha()
			img = pygame.transform.scale(self.img,(int(self.count*20),int(self.count*20)))
			screen.blit(img,(self.x+430-scrollx-img.get_width()/2,self.y-img.get_width()/2))
			if not self.flip:
				self.count+=0.4
				if self.count>self.radius:
					self.flip = True
			else:
				self.count-=0.4
			if self.count>0:
				pass
				#self.light.x = self.x+430-scrollx
				#self.light.radius = int(self.count*300)
				#self.light.render(lighting)

class Turret(object):
	def __init__(self,x,y,team):
		self.x = x
		self.y = y
		self.team = team
		self.rt = 0
		self.alive = True
		self.target = None
		self.count = 0
		self.lastshot = 0
	def render(self,players,exp,scrollx,screen,bullets):
		if self.target == None:
			for i in players:
				if sqrt(pow(players[i].x-self.x,2)+pow(players[i].y-self.y,2))<750 and players[i].alive and players[i].stealth == False:
					self.target = players[i]
					break
		else:
			if sqrt(pow((self.target.x)-self.x,2)+pow(self.target.y-self.y,2))>750 or self.target.alive == False or self.target.stealth == True:
				self.target = None
		if self.target != None:
			self.rt = -atan2(self.y-(self.target.y),self.x-(self.target.x+430))*180./pi+90
			if ti.time()-self.lastshot>0.1:
				self.lastshot = ti.time()
				bullets.append(Bullet(self.x-430,self.y+10,self.rt+90+sin(self.count)*5,self))
				self.count+=1
		img = pygame.image.load("Images/"+"turret.png").convert_alpha()
		img2 = pygame.image.load("Images/"+"gun.png").convert_alpha()
		img3 = pygame.transform.rotate(img2,self.rt)
		screen.blit(img,(self.x-scrollx,self.y))
		screen.blit(img3,(self.x+10-scrollx-img3.get_width()/2,self.y+10-img3.get_height()/2))				
	def run(self,players,bullets):
		if self.target == None:
			for i in players:
				if sqrt(pow(players[i].x-self.x,2)+pow(players[i].y-self.y,2))<750 and players[i].alive and players[i].stealth == False:
					self.target = players[i]
					break
		else:
			if sqrt(pow((self.target.x)-self.x,2)+pow(self.target.y-self.y,2))>750 or self.target.alive == False or self.target.stealth == True:
				self.target = None
		if self.target != None:
			self.rt = -atan2(self.y-(self.target.y-sin(self.target.rt*pi/180)*self.target.speed*5),self.x-(self.target.x+cos(self.target.rt*pi/180)*self.target.speed*5+430))*180./pi+90
			if ti.time()-self.lastshot>0.1:
				self.lastshot = ti.time()
				bullets.append(Bullet(self.x-430,self.y+10,self.rt+90+sin(self.count)*5,self))
				self.count+=1

class Light(object):
	def __init__(self,x,y,color,intensity,radius):
		self.x = x
		self.y = y
		self.color = color
		self.intensity = intensity
		self.radius = radius
		self.image = None
		try:
			self.master_image = pygame.image.load("Images/light.png")
			self.rendered = False
			self.pix_array = None
			if not self.rendered:
				self.pix_array = pygame.surfarray.pixels3d(self.master_image)
				c = 0
				d = 0
				for i in self.pix_array:
					d = 0
					for j in i:
						k = [0,0,0]
						k[0] = j[0]/255.*self.color[0]
						k[1] = j[1]/255.*self.color[1]	
						k[2] = j[2]/255.*self.color[2]
						self.pix_array[c][d] = k
						d+=1
					c+=1
				self.master_image = pygame.surfarray.make_surface(self.pix_array)
				self.rendered = True
		except:
			print sys.exc_info()
	def render(self,screen):
		self.image = pygame.transform.scale(self.master_image,(self.radius,self.radius))
		self.image.set_alpha(255.*self.intensity)
		screen.blit(self.image,(self.x-self.radius/2,self.y-self.radius/2))
		
		
