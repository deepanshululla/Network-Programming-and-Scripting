from __future__ import print_function
import socket

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('localhost',8000))
serverSocket.listen(1)
clientSocket,clientAddress=serverSocket.accept()
print('connected to',clientAddress)
while 1:
	data=clientSocket.recv(1024)
	print(data)
	if not data:break
    	clientSocket.send(data)
serverSocket.close()