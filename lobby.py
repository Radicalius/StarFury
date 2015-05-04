import socket
from socket import *

def lobby_accept():
	sock = socket(AF_INET,SOCK_STREAM)
	sock.bind(('',8001))
	while True:
		sock.listen(1)
		sock,addr = sock.accept()
		len = sock.recv(2)
		call = sock.recv(int(len))
