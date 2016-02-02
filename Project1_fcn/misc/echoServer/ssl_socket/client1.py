from __future__ import print_function
import socket
import ssl

clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sslSocket = ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA",keyfile=None, certfile=None, server_side=False)
server='localhost'
port=8000

sslSocket.connect((server,port))


while 1:
	data=raw_input('Client: ')
	sslSocket.send(data)
	if not data:break
	newdata=sslSocket.recv(1024)
	print('Server: ',newdata)
sslSocket.close()
