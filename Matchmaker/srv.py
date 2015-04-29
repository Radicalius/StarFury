import socket,thread,os,sys
from socket import *

class User(object):
	def __init__(self,sock,addr):
		self.addr = addr
		self.sock = sock
		self.call = None
		self.chatmode = True
		self.to_write = []
		self.atlock = ""
		self.friends = []
		self.pending = []
		thread.start_new(self.read,(1,))
		thread.start_new(self.write,(1,))
	def read(self,id):
		while True:
			try:
				length = self.sock.recv(2)
				inp = self.sock.recv(int(length))
				if inp[0]!="/" and self.atlock!="":
					inp = "@"+self.atlock+" "+inp
				g = inp.split(" ")
				if g[0] == "/login":
					if open("Accounts/"+g[1]+".act","r").readline().strip() == g[2]:
						self.call = g[1]
						users[self.call] = self
						self.sock.send("[server]: Welcome "+g[1]+"!\n")
					else:
						sock.send("[server]: Authentication Failure\n")
					v = open("Accounts/"+g[1]+".act","r")
					v.readline()
					for n in v.readline().strip().split(";"):
						self.friends.append(n)
						if n in users.keys():
							self.to_write.append("/user "+n+" Online\n")
						else:
							self.to_write.append("/user "+n+" Away\n")
					for i in users.keys():
						if self.call in users[i].friends:
							users[i].to_write.append("/user "+self.call+" Online\n")
				elif g[0] == "/register":
					if not g[1] in os.listdir("Accounts/"):
						open("Accounts/"+g[1]+".act","w").write(g[2]+"\n")
						self.sock.send("[server]: Account Created\n")
					else:
						self.sock.send("[server]: Name Already in Use\n")
				elif g[0][0] == "@":
					l = g[0][1:].split(";")
					l.append(self.call)
					h = ""
					for j in g[1:]:
						h+=j
					for i in l:
						users[i].to_write.append(self.call+"("+g[0]+"): "+h+"\n")
				elif g[0] == "/private":
					self.chatmode = False
				elif g[0] == "/public":
					self.chatmode = True
				elif g[0] == "/@lock":
					self.atlock = g[1]
				elif g[0] == "/@unlock":
					self.atlock = ""
				elif g[0] == "/logout":
					del users[self.call]
					for i in users.keys():
						if self.call in users[i].friends:
								users[i].to_write.append("/user "+self.call+" Away\n")
				elif g[0] == "/friend":
					users[g[1]].to_write.append("/friend "+self.call+"\n")
					users[g[1]].pending.append("f"+g[1])
				elif g[0] == "/y":
					print "I2"
					if self.pending[-1][0] == "f":
						print "In1"
						self.friends.append(self.pending[-1][1:])
						lines = open("Accounts/"+self.call+".act","r").readlines()
						lines[1]+=(";"+self.friends[-1])
						f = open("Accounts/"+self.call+".act","w")
						for i in lines:
							f.write(i+"\n")
						f.close()
						lines = open("Accounts/"+self.friends[-1]+".act","r").readlines()
						lines[1]+=(";"+self.call)
						f = open("Accounts/"+self.friends[-1]+".act","w")
						for i in lines:
							f.write(i+"\n")
						f.close()
					self.pending = self.pending[:-1]
				elif g[0] == "/n":
					print "In3"
					self.pending = self.pending[:-1]
				else:
					if self.call!=None:
						for i in users.keys():
							if users[i].chatmode:
								users[i].to_write.append(self.call+": "+inp+"\n")
			except:
				print sys.exc_info()
				
	def write(self,id):
		while True:
			if len(self.to_write)>0:
				self.sock.send(self.to_write[0])
				self.to_write = self.to_write[1:]

users = {}
connecting = []

ss = socket(AF_INET,SOCK_STREAM)
ss.bind(('',8006))

while True:
	ss.listen(1)
	sock,addr = ss.accept()
	connecting.append(User(sock,addr))
	print "User Joined..."
