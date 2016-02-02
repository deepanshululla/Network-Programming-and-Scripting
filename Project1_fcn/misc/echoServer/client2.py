from __future__ import print_function
import tcpClient

server='localhost'
port=8000

clientSocket=tcpClient.create((server,port))



while 1:
	data=raw_input('>')
	clientSocket.send(data)
	if not data:break
	newdata=clientSocket.recv(1024)
	print(newdata)
clientSocket.close()