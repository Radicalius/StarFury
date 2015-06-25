import socket,os,thread
from socket import *
from urllib import urlopen as get

envars = {}

f = open("lobby.cfg","r")
for i in f.readlines():
	if i[0]!="#" and i!="\n":
		g = i.split(": ")
		envars[g[0]] = g[1].strip()
f.close()

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',int(envars["Port"])))

users = {}
addrs = {}

ready = False
ingame = False
status = "Lobby"

def run_game(pnum):
	global ingame
	ingame = True
	for i in users.keys():
		users[i][3] = "InGame"
	for j in users:
		for k in users:
			sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3]+" "+users[j][4]+" "+str(users[j][5]).replace(" ","~"),users[k][0])
	os.system("python srv.py "+str(pnum))
	print "in"
	ingame = False
	for i in users.keys():
		users[i][3] = "Prep"
	for j in users:
		for k in users:
			sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3]+" "+users[j][4]+" "+str(users[j][5]).replace(" ","~"),users[k][0])
	global status
	status = "Lobby"
	update(status)	

def update(status):
	try:
		get("http://starfury.eu5.org/alter.php?name="+envars["Name"]+"&gamemode="+envars["Gamemode"]+"&map="+envars["Map"]+"&players="+str(len(users))+"/"+envars["Player Limit"]+"&status="+status+"&ip="+envars["IPv4"]+"&port="+envars["Port"])
	except:
		pass

update("Lobby")

while True:
	inp,addr = sock.recvfrom(1024)
	g = inp.split(" ")
	if g[0][0] == "/":
		if g[0] == "/player":
			users[g[1]] = [addr,"fighter","1","Prep","0",["-1"]*14]
			addrs[addr] = g[1]
			for j in users:
				sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3]+" "+users[j][4]+" "+str(users[j][5]).replace(" ","~"),addr)
			update("Lobby")
		if g[0] == "/team":
			users[addrs[addr]][2] = g[1]
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/class":
			users[addrs[addr]][1] = g[1]
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/hull":
			users[addrs[addr]][4] = str(g[1])
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/comp":
			users[addrs[addr]][5][int(g[1])] = str(g[2])
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/ready" and not ingame:
			users[addrs[addr]][3] = g[1]
		ready = True
		for j in users:
			sock.sendto("/player "+addrs[addr]+" "+users[addrs[addr]][1]+" "+users[addrs[addr]][2]+" "+users[addrs[addr]][3]+" "+users[addrs[addr]][4]+" "+str(users[addrs[addr]][5]).replace(" ","~"),users[j][0])
			if users[j][3] == "Prep":
				ready = False
		if ready == True:
			print "Game Starting..."
			status = "In Game"
			update("In Game")
			for j in users:
				sock.sendto("/start 8000",users[j][0])
			thread.start_new(run_game,(len(users),))
			
