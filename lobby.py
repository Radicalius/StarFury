import socket,os,thread
from socket import *

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('',8001))

users = {}
addrs = {}

ready = False
ingame = False

def run_game(pnum):
	global ingame
	ingame = True
	for i in users.keys():
		users[i][3] = "InGame"
	for j in users:
		for k in users:
			sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3],users[k][0])
	os.system("python srv.py "+str(pnum))
	print "in"
	ingame = False
	for i in users.keys():
		users[i][3] = "Prep"
	for j in users:
		for k in users:
			sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3],users[k][0])

while True:
	inp,addr = sock.recvfrom(1024)
	g = inp.split(" ")
	if g[0][0] == "/":
		if g[0] == "/player":
			users[g[1]] = [addr,"fighter","1","Prep"]
			addrs[addr] = g[1]
			for j in users:
				sock.sendto("/player "+j+" "+users[j][1]+" "+users[j][2]+" "+users[j][3],addr)
		if g[0] == "/team":
			users[addrs[addr]][2] = g[1]
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/class":
			users[addrs[addr]][1] = g[1]
			users[addrs[addr]][3] = "Prep"
		if g[0] == "/ready" and not ingame:
			users[addrs[addr]][3] = g[1]
			print g[1]
		ready = True
		for j in users:
			sock.sendto("/player "+addrs[addr]+" "+users[addrs[addr]][1]+" "+users[addrs[addr]][2]+" "+users[addrs[addr]][3],users[j][0])
			if users[j][3] == "Prep":
				ready = False
		if ready == True:
			print "Game Starting..."
			for j in users:
				sock.sendto("/start 8000",users[j][0])
			thread.start_new(run_game,(len(users),))
			
