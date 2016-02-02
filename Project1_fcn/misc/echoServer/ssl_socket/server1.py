from __future__ import print_function
import socket
import ssl

serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('localhost',8000))
serverSocket.listen(1)

clientSocket,clientAddress=serverSocket.accept()
sslServer=ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA",keyfile="cert.pem", certfile="cert.pem",server_side=True)

print('connected to',clientAddress)



while 1:
	dataSend=raw_input('Server: ')
	dataRecv=sslServer.recv(1024)
	print('Client: ',dataRecv)
	if not data:break
    	sslServer.send(data)
sslServer.close()
