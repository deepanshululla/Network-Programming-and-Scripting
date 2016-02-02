from __future__ import print_function
import socket

def create((server,port))

	clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clientSocket.connect((server,port))
	return clientSocket

def read(clientSocket,x)
		d=clientSocket.recv(x)
		return d
		
def send(clientSocket,d)
		clientSocket.send(d)
		
def close(clientSocket)
	clientSocket.close()

