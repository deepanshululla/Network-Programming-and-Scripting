from __future__ import print_function
import socket

clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server='localhost'
port=8000

clientSocket.connect((server,port))

while 1:
	data=raw_input('>')
	clientSocket.send(data)
	if not data:break
	newdata=clientSocket.recv(1024)
	print(newdata)
clientSocket.close()
