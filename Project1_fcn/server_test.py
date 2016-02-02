from __future__ import print_function
import socket
import rnd4Server
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('localhost',27993))
serverSocket.listen(1)
clientSocket,clientAddress=serverSocket.accept()
print('connected to',clientAddress)
data=clientSocket.recv(1024)
k=data.find('HELLO')
if k>=1:
	while 1:
		for x in range(1,10):
			d0=rnd4Server.oper()
			d1=('cs5700fall2015 STATUS '+d0+' \n')
			clientSocket.send(d1)
			data=clientSocket.recv(1024)
			m=data.split()
			print(d0 +'='+str(m[1]))
			
		d2='cs5700fall2015 321123 BYE \n'
		clientSocket.send(d2)
		serverSocket.close()
		break
				
			
serverSocket.close()
