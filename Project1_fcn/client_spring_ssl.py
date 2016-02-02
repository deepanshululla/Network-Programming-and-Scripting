
#$ ./client <-p port> [hostname] [NEU ID]
#$ client.py -p 27994 -s cs5700.ccs.neu.edu 001798574
from __future__ import print_function
import socket
import sys
import ssl
import str2int2 #self made library for conversion of string to algebraic calculations

clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
hostName=str(sys.argv[4])
server=hostName
portS=str(sys.argv[2])
port=int(portS)
nuid=str(sys.argv[5])

try:
	sslSocket = ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_SSLV2,certfile=None,server_side=False)
	sslSocket.connect((server,port))
	print('socket created using sslv2')
except:
	try:
		sslSocket = ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_SSLv23,certfile=None,server_side=False)
		sslSocket.connect((server,port))
		print('socket created using SSLv23')
	except:
		sslSocket = ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_SSLV3,certfile=None,server_side=False)
		sslSocket.connect((server,port))
		print('socket created using sslv2')
	# python client.py -p 27994 -s cs5700.ccs.neu.edu 001798574

str1="Client: cs5700spring2015 HELLO "+nuid+" \n"
print(str1)
sslSocket.send(str1)

data=sslSocket.recv(1024)
print(data)


count=0;
# client sends hello msg: cs5700fall2015 HELLO [your NEU ID] \n
if data.find('STATUS')>0 or data.find('BYE')>0:
	while True:
		# print('recieving data')
	
	
		# data=sslSocket.recv(1024)
	
		
		print(data)
		k=data.find('BYE')
		r=data.find('STATUS')
		if k>0:
			f=data.split()
			sec_flag=f[1]
			print('The secret flag is ',sec_flag)
			sslSocket.close()
			
			break
		elif r>0:
			sol=str(str2int2.calc2(data))
			# print(r+' = '+sol)
			
			sol2="cs5700spring2015 "+sol+' \n'
			print(sol2)
			sslSocket.send(sol2)
			data=sslSocket.recv(1024)
			
			if data:continue
			
			
# r=data.find('STATUS')
#--------------
# if data.find('STATUS')>0:
	# while True:
		
		# if data.find('STATUS')<0:break
		
		# sol=str(str2int2.calc2(data))
		
		# print(sol)
		# sslSocket.send("cs5700spring2015 "+sol+' \n')
print('Closing connection')
sslSocket.close()



		
