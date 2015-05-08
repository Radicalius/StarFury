import socket,random,thread,sys
import time as ti
from socket import *
from class_ import *

ss = socket(AF_INET,SOCK_DGRAM)
ss.bind(("",8000))

score = Score()

map = []
bmap = []
players = {}
addrs = {}
bullets = []
rockets = []
turrets = []
bombs = []
uaddrs = {}

score1 = 0
score2 = 0
victor = None

playernum = int(sys.argv[1])
length = 500
playerc = 0
start = False
af1 = 0
af2 = 0
bots = 0

last = random.randint(1,10)
map.append(860/20)
map.append(last)
for i in range(length):
	if random.randint(0,4) == 4:
		last+=random.randint(-1,1)
		if (last == 1):
			last = 2
		if last == 11:
			last = 5
		map.append(last)
	else:
		map.append(last)
map.append(860/20)
bmap.append(-1)
for i in range(length+3):
	if bmap[-1] == 9:
		bmap.append(8)
	else:
		if random.randint(0,4) == 4 and map[i]>0:
			if random.randint(0,3)!=0:
				bmap.append(random.randint(0,3))
			else:
				bmap[-1] = 8
				bmap.append(9)
		else:
			bmap.append(-1)

sx = int(0.0625*length)
mx = int(0.75*length)
afs = []

if playernum%2 == 0:
	ghj = playernum
else:
	ghj = playernum+1

afs = [0]*ghj

for i in range(ghj/2):
	x = i*int(length*0.0625)+sx
	bmap[x] = -3
	bmap[x-9] = 5
	bmap[x-2] = 4
	bmap[x-1] = 7
	bmap[x-3] = 7
	for j in range(1,10):
		bmap[x+j] = -2
		map[x+j] = map[x]	
	map[x-1] = map[x]	
	map[x-2] = map[x]
	map[x-3] = map[x]
	bmap[-x] = -3
	bmap[-x+9] = 5
	bmap[-x+2] = 4
	bmap[-x+1] = 7
	bmap[-x+3] = 7
	for j in range(1,10):
		bmap[-x-j] = -2
		map[-x-j] = map[-x]	
	map[-x+1] = map[-x]	
	map[-x+2] = map[-x]
	map[-x+3] = map[-x]
	afs[i] = x
	afs[ghj/2-i] = length-x

afs = sorted(afs)
print afs
map[1] = 4
for i in range(2,10):
	map[i] = 4
	map[-i] = 4

bmap[10] = 11
bmap[9] = 4
bmap[11] = 4
bmap[4] = 5
bmap[2] = 5

bmap[200] = 7
bmap[199] = 4
bmap[192] = 5

bmap[175] = 7
bmap[174] = 4
bmap[167] = 5

bmap[-175] = 7
bmap[-174] = 4
bmap[-167] = 5

bmap[-200] = 7
bmap[-199] = 4
bmap[-192] = 5


bmap[-11] = 10
bmap[-10] = 4
bmap[-12] = 4
bmap[-5] = 5
bmap[-3] = 5

mapstring = ""
bmapstring = ""
for i in map:
	mapstring+=" "+str(i)
for i in bmap:
	bmapstring+=" "+str(i)

scount = 0
tcount = 0
lasttime = 0
count = 0
lastshot = 0
victor = None

te = 1
af = 0
for i in range(bots):
	if te == 1:
		af = af1	
		af1+=1
	else:		
		af = af2+playernum/2
		af2+=1
	players["Bot"+str(i)] = Bot("Bot"+str(i),"fighter",str(te),af)
	if te == 1:
		te = 2
	else:
		te = 1
	playerc+=1

def update(id):
	global count,lastshot,bmap,victor
	for i in players.keys():
		if not players[i].ai:
			players[i].run(map,bmap,bullets,bombs,rockets,score,ss,players)
	for i in bullets:
		if i.alive:
			i.run(map,bmap)
	for i in bombs:
		bmap = i.run(bmap,map,score,players)
	for i in rockets:
		i.run(map,bmap)	
	for i in turrets:
		i.run(players,bullets)
	j = 0
	shot = False
	for i in bmap:
		if i == 7:
				x = j*20+10
				y = 680-map[j]*20+10
				tar = None
				for i in players.keys():
					dist = sqrt(pow(x-players[i].x,2)+pow(y-players[i].y,2))
					if players[i].alive and sqrt(pow(x-players[i].x,2)+pow(y-players[i].y,2))<860 and not players[i].stealth:
						if (players[i].team == "1" and j>250) or (players[i].team == "2" and j<250) and not players[i].stealth:
							tar = players[i]
				if tar!=None:
					rt = -atan2(y-(tar.y-sin(tar.rt*pi/180.)*tar.speed*dist/(100)),x-(tar.x+430+cos(tar.rt*pi/180)*tar.speed*dist/(100)))*180./pi+90+random.randint(-10,10)
				else:
					rt = 0
				if ti.time()>lastshot+0.15 and tar!=None:
					shot = True
					bullets.append(Bullet(x-430-sin(rt*pi/180.)*40,y-cos(rt*pi/180.)*40,rt+90,Team(1)))
					for i in players.keys():
						if not players[i].ai:
							ss.sendto("14 "+str(int(bullets[-1].x))+" "+str(int(bullets[-1].y))+" "+str(int(bullets[-1].rt)),addrs[i])
		j+=1
	count+=1
	if shot:
		lastshot = ti.time()
	if score.s1>=10000 or score.s2<=-10000:
		victor = 0
	if score.s2>=10000 or score.s1<=-10000:
		victor = 1
	if victor==0:
		for i in players.keys():
			if not players[i].ai:
				if players[i].team == 0:
					ss.sendto("17 1",players[i].addr)
				else:
					ss.sendto("17 0",players[i].addr)
		sys.exit(0)
	if victor==1:
		for i in players.keys():
			if not players[i].ai:
				if players[i].team == 1:
					ss.sendto("17 1",players[i].addr)
				else:
					ss.sendto("17 0",players[i].addr)
		sys.exit(0)
	if random.randint(1,500) == 1:
		while True:
			index = random.randint(0,500)
			if bmap[index] == -1:
				bmap[index] = random.choice([0,1,2,3,8,9])
				for k in players.keys():
					if not players[k].ai:
						ss.sendto("20 "+str(index)+" "+str(bmap[index]),players[k].addr)
				break		

def sync(id):
	try:
		global count
		for i in players.keys():
			for j in players.keys():
				if not players[j].ai:
					ss.sendto("6 "+i+" "+str(int(players[i].x))+" "+str(int(players[i].y))+" "+str(int(players[i].rt)),addrs[j]) 	
		for i in range(len(bullets)):
			if bullets[i].alive:
				for j in players.keys():
					if not players[j].ai:
						ss.sendto("8 "+str(i)+" "+str(int(bullets[i].x))+" "+str(int(bullets[i].y)),addrs[j])
		for i in range(len(bombs)):
			if bombs[i].alive:
				for j in players.keys():
					if not players[j].ai:
						ss.sendto("10 "+str(i)+" "+str(int(bombs[i].x))+" "+str(int(bombs[i].y)),addrs[j])  
		if score.update:
			for j in players.keys():
				if not players[j].ai:
					print score.s1,score.s2
					ss.sendto("13 "+str(score.s1)+" "+str(score.s2),addrs[j])
			score.update = False
	except:
		print sys.exc_info()
def run(id):
	global scount,lasttime,tcount
	while True:
		scount+=(ti.time()-lasttime)
		tcount+=(ti.time()-lasttime)
		lasttime = ti.time()
		if scount>1/280. and start:
			thread.start_new(update,(1,))
			scount = 0
		if tcount>1/10. and start:
			thread.start_new(sync,(1,))
			tcount = 0

thread.start_new(run,(1,))

#lusers = {}
#sock = socket(AF_INET,SOCK_STREAM)
#sock.bind(('',8001))

#def lobby_accept(id):
#	global lusers
#	while True:
#		sock.listen(1)
#		sock1,addr = sock.accept()
#		ti.sleep(1)
#		len = sock.recv(2)
#		call = sock.recv(int(len))
#		lusers[call] = [sock1,"fighter","0"]
#		print lusers

#thread.start_new(lobby_accept,(1,))

af = 0
af1 = 0
af2 = -1
while True:
	inp = ss.recvfrom(4048)
	g = inp[0].split(" ")
	addr = inp[1]
	cmd = int(g[0])
	if cmd == 0:
		if not g[1] in players.keys() and playerc<playernum:
			addrs[g[1]] = addr
			uaddrs[addr] = g[1]
			print g[1]+" joined..."
			ss.sendto("0"+mapstring,addr)
			ss.sendto("1"+bmapstring,addr)
			print afs[af],af
			if g[3] == "1":
				players[g[1]] = Player(g[1],addr,g[2],g[3],afs[af1])
				af+=1
			else:		
				players[g[1]] = Player(g[1],addr,g[2],g[3],afs[af2])
				af2-=1
			for i in players.keys():
				ss.sendto("2 "+i+" "+players[i].class_+" "+players[i].team+" "+str(af),addr)
				print i
			for i in players.keys():
				if not players[i].ai:
					ss.sendto("2 "+g[1]+" "+players[g[1]].class_+" "+players[g[1]].team+" "+str(players[g[1]].airfield),addrs[i])
			score.update = True
			playerc+=1
			if playerc == playernum:
				start = True
				print "Game Starting..."
				for i in players.keys():
					if not players[i].ai:
						ss.sendto("111",addrs[i])
			count = 0
	if cmd == 2:
		players[uaddrs[addr]].rth = int(g[1])
		for i in players.keys():
			if not players[i].ai:
				ss.sendto("4 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 3:
		if g[1] == "2":
			if players[uaddrs[addr]].class_ == "fighter":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)+2*pow(1.25,players[uaddrs[addr]].amp)
			if players[uaddrs[addr]].class_ == "bomber":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)
				players[uaddrs[addr]].stealth = True
			if players[uaddrs[addr]].class_ == "interceptor":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)
				players[uaddrs[addr]].mark = True
		else:
			if players[uaddrs[addr]].class_ == "fighter":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)
			if players[uaddrs[addr]].class_ == "bomber":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)
				players[uaddrs[addr]].stealth = False
			if players[uaddrs[addr]].class_ == "interceptor":
				players[uaddrs[addr]].speed = pow(1.25,players[uaddrs[addr]].sstat)
				players[uaddrs[addr]].mark = False
		for i in players.keys():
			if not players[i].ai:
				ss.sendto("5 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 4:
		players[uaddrs[addr]].gun = int(g[1])
		for i in players.keys():
			if not players[i].ai:
				ss.sendto("7 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 5:
		players[uaddrs[addr]].bomb = int(g[1])
		for i in players.keys():
			if not players[i].ai:
				ss.sendto("9 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 6:
		players[uaddrs[addr]].rocket = int(g[1])
		for i in players.keys():
			if not players[i].ai:
				ss.sendto("11 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 7:
		try:
			players[uaddrs[addr]].mx = int(g[1])
			players[uaddrs[addr]].my = int(g[2])
			for i in players.keys():
				if not players[i].ai:
					ss.sendto("12 "+uaddrs[addr]+" "+g[1]+" "+g[2],addrs[i])
		except:
			pass
	if cmd == 8:
		user = players[uaddrs[addr]]
		if g[1]!="":
			if user.gold>=100 and user.landed:
				user.gold-=100
				if g[1] == "Ammo":	
					user.ammo+=1
				if g[1] == "RoF":	
					user.rof+=1
				if g[1] == "Range":	
					user.range+=1
				if g[1] == "Caliber":	
					user.cal+=1
				if g[1] == "Bullet Speed":	
					user.bs+=1
				if g[1] == "Power":	
					user.amp+=1
				if g[1] == "Duration":	
					user.powstat+=1
				if g[1] == "Cooldown":	
					user.cooldown+=1
				if g[1] == "AOE":	
					user.aoe+=1
				if g[1] == "Speed":	
					user.sstat+=1
				if g[1] == "Handling":	
					user.mstat+=1
				if g[1] == "Heat Signature":	
					user.hs+=1
				if g[1] == "Hit Box":	
					user.hb+=1
				if g[1] == "Respawn Rate":	
					user.rr+=1
				for i in players.keys():
					if not players[i].ai:
						ss.sendto("15 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 9:
		user = players[uaddrs[addr]]
		if g[1]!="":
			if user.gold>=100 and user.landed:
				user.comps[int(g[1])].upgrade(user)
				user.gold-=100
				for i in players.keys():
					if not players[i].ai:
						ss.sendto("18 "+uaddrs[addr]+" "+g[1],addrs[i])
	if cmd == 10:
		user = players[uaddrs[addr]]
		for i in players.keys():
			if not players[i].ai:
				s = ""
				for j in g[1:]:
					s+=j+" "
				ss.sendto("21 "+user.call+" "+s,addrs[i])	
				
