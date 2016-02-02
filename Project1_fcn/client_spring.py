
#$ ./client <-p port> [hostname] [NEU ID]
#$ client.py -p 27993 cs5700.ccs.neu.edu 001798574
from __future__ import print_function
import socket
import sys
import str2int2 #self made library for conversion of string to algebraic calculations

clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('socket created')
server=str(sys.argv[1])

nuid=str(sys.argv[2])



port=27993



clientSocket.connect((server,port))
str1="cs5700spring2015 HELLO "+nuid+" \n"
print(str1)
clientSocket.send(str1)
data=clientSocket.recv(1024)
print(data)
# client sends hello msg: cs5700fall2015 HELLO [your NEU ID] \n
if data.find('STATUS')>0 or data.find('BYE')>0:
	while True:
		# print('recieving data')
	
	
		# data=clientSocket.recv(1024)
	
		
		print(data)
		k=data.find('BYE')
		r=data.find('STATUS')
		if k>0:
			f=data.split()
			sec_flag=f[1]
			print('The secret flag is ',sec_flag)
			clientSocket.close()
			break
		elif r>0:
			sol=str(str2int2.calc2(data))
			# print(r+' = '+sol)
			
			sol2="cs5700spring2015 "+sol+' \n'
			print(sol2)
			clientSocket.send(sol2)
			data=clientSocket.recv(1024)
			if data:continue
			
# r=data.find('STATUS')
#--------------
# if data.find('STATUS')>0:
	# while True:
		
		# if data.find('STATUS')<0:break
		
		# sol=str(str2int2.calc2(data))
		
		# print(sol)
		# clientSocket.send("cs5700spring2015 "+sol+' \n')
print('Closing connection')
clientSocket.close()


		
