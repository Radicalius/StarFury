import socket,sys,pygame,thread
from socket import *
from class_ import *
from math import *
import time as ti
pygame.init()

#call = sys.argv[1]#raw_input("Callsign: ")
#team = sys.argv[3] #raw_input("Team [1,2]: ")
#class_ = sys.argv[2] #raw_input("Class[Fighter,Interceptor,Bomber]: ")
s = socket(AF_INET,SOCK_DGRAM)

start = "lobby"

#host = ((raw_input("Server IP: "),int(raw_input("Port: "))))
#host = (sys.argv[4],int(sys.argv[5]))
host = ("localhost",8001)

log = open("log.txt",'w')
#sys.stdout = log

map = []
bmap = []
exp = []
bombs = []
bullets = []
rockets = []
turrets = []
shields = []
players = {}
call = ""

lscrollx = 0
fudge = 1.
fdata = [1.]*25
fpos = 0

score = Score()

scrollx = 0

upgrades = [["Ammo", "Range","Caliber","RoF","Bullet Speed"],["Power","Duration","Cooldown","AOE",""],["Speed","Handling","Heat Signature","Hit Box","Respawn Rate"]]

screen = pygame.display.set_mode((860,680),0,32)
pygame.display.set_caption("StarFury")

text = pygame.image.load("Images/"+"text.png").convert()
bg = pygame.image.load("Images/"+"bg.png").convert()
shade = pygame.image.load("Images/"+"shade.png").convert_alpha()
fighter = pygame.image.load("Images/"+"fighter.png").convert_alpha()
target = pygame.image.load("Images/"+"target.png").convert_alpha()
font = pygame.font.Font("font.ttf",20)
victory = None
vcount = 0

cats = []

imgs = {}

for i in range(-3,12):
	imgs[i] = pygame.image.load("Images/"+str(i)+".png").convert_alpha()

def read(id):
	global vcount,victory,start,host
	while True:
		try:
			inp = s.recvfrom(12000)
			if inp[0] == "111":
				global start
				start = "running"
			g = inp[0].split(" ")
			if g[0] == "/player":
				lobby[g[1]] = [g[2],g[3],g[4]]
				print lobby
			if g[0] == "/start":
				host = (inp[1][0],int(g[1]))
				ti.sleep(1)
				start = "waiting"
				call = callsign
				s.sendto("0 "+call+" "+lobby[call][0]+" "+lobby[call][1],host)
				print "in"
			cmd = int(g[0])
			if cmd == 0:
				for i in g[1:]:
					try:
						map.append(int(i))
					except:
						print i	
			if cmd == 1:
				x = 0
				for i in g[1:]:
					try:
						if i == "-4":
							turrets.append(Turret(x*20-20,680-map[x]*20,2))
						else:
							bmap.append(int(i))
					except:
						print i,sys.exc_info()
					x+=1
			if cmd == 2:
				players[g[1]] = Player(g[1],None,g[2],g[3],int(g[4]))
			if cmd == 4:
				players[g[1]].rth = int(g[2])
			if cmd == 5:
				if g[2] == "2":
					if players[g[1]].class_ == "fighter":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)+2*pow(1.25,players[g[1]].amp)
					if players[g[1]].class_ == "bomber":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)
						players[g[1]].stealth = True
					if players[g[1]].class_ == "interceptor":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)
						players[g[1]].mark = True
				else:
					if players[g[1]].class_ == "fighter":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)
					if players[g[1]].class_ == "bomber":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)
						players[g[1]].stealth = False
					if players[g[1]].class_ == "interceptor":
						players[g[1]].speed = pow(1.25,players[g[1]].sstat)
						players[g[1]].mark = False
			if cmd == 6:
				global fpos,lscrollx
				#players[g[1]].sx = int(g[2])
				#players[g[1]].sy = int(g[3])
				#diff = sqrt(players[g[1]].sx*players[g[1]].sx+players[g[1]].sy*players[g[1]].sy)-sqrt(players[g[1]].x*players[g[1]].x+players[g[1]].y*players[g[1]].y)
				##if diff>self.speed*14:
				#	players[g[1]].x = int(g[2])
				#	players[g[1]].y = int(g[3])
				#else:
				#	players[g[1]].speed = diff/14.
				try:
					dp = abs((players[g[1]].x-lscrollx)/(int(g[2])-lscrollx))
				except ZeroDivisionError:
					dp = 1.
				fdata[fpos] = dp
				fpos+=1
				if fpos == 25:
					fpos = 0
				fudge = sum(fdata)/len(fdata)
				players[g[1]].x = int(g[2])
				players[g[1]].y = int(g[3])
				players[g[1]].rt = int(g[4])
				lscrollx = int(g[2])
			if cmd == 7:
				players[g[1]].gun = int(g[2])
			if cmd == 8:
				#bullets[int(g[1])].x = int(g[2])
				#bullets[int(g[1])].y = int(g[3])
				#if g[1] == call:
				#	sys.exit(0)
				pass
			if cmd == 9:
				players[g[1]].bomb = int(g[2])
			if cmd == 10:
				bombs[int(g[1])].x = int(g[2])
				bombs[int(g[1])].y = int(g[3])
			if cmd == 11:
				players[g[1]].rocket = int(g[2])
			if cmd == 12:
				players[g[1]].mx = int(g[2])
				players[g[1]].my = int(g[3])
			if cmd == 13:
				score.s1 = int(g[1])
				score.s2 = int(g[2])
			if cmd == 14:
				bullets.append(Bullet(int(g[1]),int(g[2]),int(g[3]),Team(1)))
			if cmd == 15:
				user = players[g[1]]
				user.gold-=100
				if g[2] == "Ammo":	
					user.ammo+=1
				if g[2] == "RoF":	
					user.rof+=1
				if g[2] == "Range":	
					user.range+=1
				if g[2] == "Caliber":	
					user.cal+=1
				if g[2] == "Bullet Speed":	
					user.bs+=1
				if g[2] == "Power":	
					user.amp+=1
				if g[2] == "Duration":	
					user.powstat+=1
				if g[2] == "Cooldown":	
					user.cooldown+=1
				if g[2] == "AOE":	
					user.aoe+=1
				if g[2] == "Speed":	
					user.sstat+=1
				if g[2] == "Handling":	
					user.mstat+=1
				if g[2] == "Heat Signature":	
					user.hs+=1
				if g[2] == "Hit Box":	
					user.hb+=1
				if g[2] == "Respawn Rate":	
					user.rr+=1
			if cmd == 16:
				players[g[1]].alive = False
			if cmd == 17:
				if int(g[1])==1:
					victory = True
				else:
					victory = False
			if cmd == 18:
				players[g[1]].gold-=100
				players[g[1]].comps[int(g[2])].upgrade(players[g[1]])
			if cmd == 19:
				players[g[1]].slock.lock(True)
			if cmd == 20:
				bmap[int(g[1])] = int(g[2])
				#players[g[1]].speed = int(g[2])
			if cmd == 21:
				s1 = ""
				for i in g[2:]:
					s1+=i+" "
				cats.append("["+g[1]+"] "+s1)
		except:
			try:
				print sys.exc_info()
			except:
				pass

thread.start_new(read,(1,))

pygame.mouse.set_visible(False)

hx = 0
clock = pygame.time.Clock()
count = 0
lastshot = 0
upgrade = False
u = pygame.image.load("Images/"+"upgrade.png").convert_alpha()

mp = False
chat = False
text1 = ""

f2 = pygame.font.Font("font.ttf",40)
f3 = pygame.font.Font("font.ttf",30)
callsign = ""
class_ = "Fighter"
server = "localhost"
port = "8001"
selected = 0
classn = 0
team = 0
teamn = 0

lobby = {}
state = 0
team = 0
class_2 = 0
rdy1 = False

while True:
	if start == "running":
		#print players["Bot0"].speed
		mx,my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise SystemExit
			if event.type == pygame.KEYDOWN:
				if not chat:
					if event.key == K_ESCAPE:
						raise SystemExit
					if event.key == pygame.K_LEFT:
						s.sendto("2 1",host)
					if event.key == pygame.K_RIGHT:
						s.sendto("2 -1",host)
					if event.key == pygame.K_UP:
						s.sendto("3 2",host)
					if event.key == pygame.K_RETURN:
						s.sendto("4 1",host)
					if event.key == pygame.K_DOWN:
						s.sendto("5 1",host)
					if event.key == pygame.K_SPACE:
						s.sendto("6 1",host)
					if event.key == pygame.K_TAB:
						upgrade = True
				else:
					if event.key == pygame.K_RETURN:
						chat = False
						s.sendto("10 "+text1,host)
						text1 = ""
					elif event.key == pygame.K_BACKSPACE:
						text1 = text1[:-1]
					elif event.key == pygame.K_SPACE:
						text1+=" "
					else:
						text1+=pygame.key.name(event.key)
				if event.key == pygame.K_t:
					chat = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					s.sendto("2 0",host)
				if event.key == pygame.K_LEFT:
					s.sendto("2 0",host)
				if event.key == pygame.K_UP:
					s.sendto("3 0",host)
				if event.key == pygame.K_RETURN:
					s.sendto("4 0",host)
				if event.key == pygame.K_DOWN:
					s.sendto("5 0",host)
				if event.key == pygame.K_SPACE:
					s.sendto("6 0",host)
				if event.key == pygame.K_TAB:
					upgrade = False
			if event.type == pygame.MOUSEMOTION:
				s.sendto("7 "+str(int(mx+scrollx))+" "+str(int(my)),host)		
			if event.type == MOUSEBUTTONDOWN:
				mp = True
				if upgrade:
					col = -1
					row = -1
					x,y = 430-568/2,340-422/2
					mrx = mx-x
					mry = my-y
					if mrx>50 and mrx<75:
						col = 0
					if mrx>210 and mrx<235:
						col = 1
					if mrx>375 and mrx<400:
						col = 2
					for i in range(5):
						if mry>100+i*45 and mry<100+i*45+25:
							row = i
					if col>-1 and row>-1:
						s.sendto("8 "+upgrades[col][row],host)
			if event.type == MOUSEBUTTONUP:
				mp = False
						

		clock.tick(70)#+140*fudge)
		scrollx+=hx
		j = 0
		screen.fill((255,255,255))
		screen.blit(bg,(0,0))

		for i in bullets:
			i.render(screen,scrollx,map,bmap)
		for i in bombs:
			i.render(screen,scrollx,map,bmap,exp,score,players)
		for i in rockets:
			i.render(screen,scrollx,map,bmap,mx,my,exp)
		for i in exp:
			i.render(screen,scrollx)
		for i in map:
			for k in range(i):
				screen.blit(text,(j*20-scrollx,680-k*20))
			screen.blit(shade,(j*20-scrollx,680-(i-1)*20))
			j+=1
			pass
		for i in turrets:
			i.render(players,exp,scrollx,screen,bullets)
		j = 0
		for i in players.keys():
			players[i].render(screen,call,scrollx,map,exp,bmap,bullets,bombs,rockets,players,score)
			x = 0
			if i == call and upgrade and players[i].landed:
				for h in players[i].comps:
					h.render(screen,x,mx,my,mp,s,host)
					x+=1
		shot = False
		for i in bmap:
			if i!=-1 and i!=-4:
				try:
					screen.blit(imgs[i],(j*20-scrollx,680-((map[j])*20)))
				except:
					pass
			if i == 4:
				for k in bombs:
					if sqrt(pow(k.x+430-j*20,2)+pow(k.y-(680-map[int(j+430)/20]*20),2))<100 and  k.alive:
						k.alive = False
						k.lock = True
			if i == 7:
				x = j*20+10
				y = 680-map[j]*20+10
				tar = None
				for i in players.keys():
					dist = sqrt(pow(x-players[i].x,2)+pow(y-players[i].y,2))
					if players[i].alive and sqrt(pow(x-players[i].x,2)+pow(y-players[i].y,2))<860:
						if (players[i].team == "1" and x>250*20) or (players[i].team == "2" and x<250*20) and not players[i].stealth:
							tar = players[i]
				if tar!=None:
					rt = -atan2(y-(tar.y-sin(tar.rt*pi/180.)*tar.speed*dist/100),x-(tar.x+430+cos(tar.rt*pi/180)*tar.speed*dist/100))*180./pi+90
				else:
					rt = 0
				img2 = pygame.image.load("Images/"+"gun.png").convert_alpha()
				img3 = pygame.transform.rotate(img2,rt)
				screen.blit(img3,(x-scrollx-img3.get_width()/2,y-img3.get_height()/2))
			j+=1
		if shot:
			lastshot = ti.time()
		try:
			screen.blit(target,(mx-10,my-10))
			screen.blit(pygame.image.load("Images/"+"bullet.png").convert_alpha(),(5,15))
			screen.blit(font.render(str(int(players[call].shots)),True,(255,255,255)),(20,10))
			screen.blit(pygame.image.load("Images/"+"bomb.png").convert_alpha(),(5,40))
			screen.blit(font.render(str(int(players[call].bombs)),True,(255,255,255)),(20,35))
			screen.blit(pygame.image.load("Images/"+"missle.png").convert_alpha(),(5,65))
			screen.blit(font.render(str(int(players[call].rockets)),True,(255,255,255)),(20,60))
			screen.blit(font.render(str(int(players[call].powdur)),True,(255,255,255)),(20,85))
			a = font.render(str(score.s1)+" vs "+str(score.s2),True,(255,255,255))
			b = font.render("Credits: "+str(players[call].gold),True,(255,255,255))
			screen.blit(a,(430-a.get_width()/2,0))
			screen.blit(b,(430+430*3/4-a.get_width()/2,0))
			scrollx = players[call].x
			if scrollx>500*20-800:
				scrollx = 500*20-800
			if scrollx<0:
				scrollx = 0
			players[call].mx = mx
			players[call].my = my
			for i in range(1,5):
				try:
					screen.blit(font.render(cats[-i],True,(255,255,255)),(0,640-i*20))
				except:	
					pass	
			if chat:			
				screen.blit(font.render(text1,True,(255,255,255)),(0,640))
		except:
			print sys.exc_info()
		if upgrade and players[call].landed:
			#568,422
			screen.blit(u,(430-568/2,340-422/2))
		if victory!=None and vcount<140*2:
			if victory:
				screen.blit(pygame.image.load("Images/"+"victory.png").convert_alpha(),(0,0))
			else:
				screen.blit(pygame.image.load("Images/"+"defeat.png").convert_alpha(),(0,0))
			vcount+=1
			if vcount>140:
				global start
				start = "lobby"
				host = ("localhost",8001)
		pygame.display.update()
		count+=1
	elif start == "waiting":
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit()
		screen.fill((0,0,0))
		t = font.render("Waiting for Players...",True,(255,255,255))
		screen.blit(t,(430-t.get_width()/2,340-t.get_height()/2))
		pygame.display.update()
	else:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.display.quit()
			if event.type == KEYDOWN:
				#s.sendto("0 "+call+" "+class_+" "+team,host)
				if state == 0:
					if event.key == K_UP:
						if selected>0:
							selected-=1
					elif event.key == K_DOWN:
						if selected<5:
							selected+=1
					elif event.key == K_RIGHT and selected == 1:
						classn+=1
					elif event.key == K_LEFT and selected == 1:
						classn-=1
					elif event.key == K_RIGHT and selected == 2:
						teamn+=1
					elif event.key == K_LEFT and selected == 2:
						teamn-=1
					elif event.key == K_RETURN:
						host = (server,int(port))
						call = callsign
						#s.sendto("0 "+callsign+" "+class_.lower()+" "+str(team),host)
						#start = "waiting"
						s.sendto("/player "+call,host)
						state = 1
						selected = 0
					else:
						if selected == 0:
							if event.key == K_BACKSPACE:
								callsign = callsign[:-1]
							elif event.key == KMOD_LSHIFT or event.key == KMOD_RSHIFT:
								pass
							else:
								if pygame.key.name(event.key) in string.lowercase or pygame.key.name(event.key) in ["1","2","3","4","5","6","7","8","9","0"]:
									if  KMOD_LSHIFT & pygame.key.get_mods() or KMOD_RSHIFT & pygame.key.get_mods(): 										
										callsign+=pygame.key.name(event.key).upper()
									else:
										callsign+=pygame.key.name(event.key)
						if selected == 3:
							if event.key == K_BACKSPACE:
								server = server[:-1]
							else:
								server+=pygame.key.name(event.key)
						if selected == 4:
							if event.key == K_BACKSPACE:
								port = port[:-1]
							else:
								port+=pygame.key.name(event.key)
					c = ["Fighter","Interceptor","Bomber"]
					class_ = c[classn%3]	
					team = teamn%2+1			
				else:
					if event.key == K_RETURN:
						if selected == 0:
							team+=1
							c = ["fighter","interceptor","bomber"]
							s.sendto("/class "+str(c[team%3]),host)
						if selected == 1:
							if rdy1:
								s.sendto("/ready Prep",host)
								rdy1 = False
							else:
								s.sendto("/ready Ready",host)
								rdy1 = True
						if selected == 2:
							class_2+=1
							s.sendto("/team "+str(class_2%2+1),host)
					if event.key == K_RIGHT:
						if selected<3:
							selected+=1
					if event.key == K_LEFT:
						if selected>0:					
							selected-=1
		screen.fill((0,0,0))
		t = f2.render("STARFURY",True,(255,255,255))
		if state == 0:
			if selected == 0:
				t2 = font.render("CALLSIGN: "+callsign,True,(155,155,255))
			else:
				t2 = font.render("CALLSIGN: "+callsign,True,(255,255,255))
			if selected == 1:
				t3 = font.render("CLASS: "+class_,True,(155,155,255))
			else:
				t3 = font.render("CLASS: "+class_,True,(255,255,255))
			if selected == 2:
				t45 = font.render("TEAM: "+str(team),True,(155,155,255))
			else:
				t45 = font.render("TEAM: "+str(team),True,(255,255,255))
			if selected == 3:
				t4 = font.render("SERVER: "+server,True,(155,155,255))
			else:
				t4 = font.render("SERVER: "+server,True,(255,255,255))
			if selected == 4:
				t5 = font.render("PORT: "+port,True,(155,155,255))
			else:
				t5 = font.render("PORT: "+port,True,(255,255,255))
			if selected == 5:
				t6 = font.render("CONNECT",True,(155,155,255))
			else:
				t6 = font.render("CONNECT",True,(255,255,255))
			screen.blit(t2,(430-t.get_width()/2-200,290-t2.get_height()/2))
			screen.blit(t3,(430-t.get_width()/2-200,340-t3.get_height()/2))
			screen.blit(t45,(430-t.get_width()/2-200,390-t4.get_height()/2))
			screen.blit(t4,(430-t.get_width()/2-200,440-t4.get_height()/2))
			screen.blit(t5,(430-t.get_width()/2-200,490-t5.get_height()/2))
			screen.blit(t6,(430-t6.get_width()/2,590-t6.get_height()/2))
		else:
			h = f3.render("BLUE",True,(100,100,155))
			screen.blit(h,(860/4.-h.get_width()/2-30,240))
			h2 = f3.render("RED",True,(155,100,100))
			screen.blit(h2,(860/4.*3.-h2.get_width()/2-30,240))
			by = 0
			ry = 0
			for i in lobby.keys():
				if lobby[i][1] == "1":
					screen.blit(pygame.image.load("Images/"+lobby[i][0]+".png").convert_alpha(),(0,290+by)) 
					cname = font.render(i,True,(100,100,155))
					screen.blit(cname,(50,290-cname.get_height()/2+by))
					rdy = font.render(lobby[i][-1],True,(100,100,155))
					screen.blit(rdy,(250,290-cname.get_height()/2+by))
					by+=50	
				if lobby[i][1] == "2":
					screen.blit(pygame.image.load("Images/"+lobby[i][0]+".png").convert_alpha(),(430,290+ry)) 
					cname = font.render(i,True,(155,100,100))
					screen.blit(cname,(50+430,290-cname.get_height()/2+ry))
					rdy = font.render(lobby[i][-1],True,(155,100,100))
					screen.blit(rdy,(250+430,290-cname.get_height()/2+ry))
					ry+=50	
			if selected == 0:
				t2 = font.render("SWITCH CLASS",True,(155,155,255))
			else:
				t2 = font.render("SWITCH CLASS",True,(255,255,255))
			if selected == 1:
				t3 = font.render("READY",True,(155,155,255))
			else:
				t3 = font.render("READY",True,(255,255,255))
			if selected == 2:
				t45 = font.render("SWITCH TEAM",True,(155,155,255))
			else:
				t45 = font.render("SWITCH TEAM",True,(255,255,255))
			screen.blit(t2,(430-t.get_width()/2-300,600-t2.get_height()/2))
			screen.blit(t3,(430-t.get_width()/2+50,600-t3.get_height()/2))
			screen.blit(t45,(430-t.get_width()/2+300,600-t4.get_height()/2))	
		screen.blit(t,(430-t.get_width()/2,140-t.get_height()/2))
		pygame.display.update()
