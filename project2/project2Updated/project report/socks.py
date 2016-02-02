#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys


host='fring.ccs.neu.edu'
port=80
# Creating a socket

def create_sock(host,port):
	try :
		clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
		# print "Socket Created"
	except socket.error as e:
		 
		print e
		sys.exit("Failed to create socket error code")    
	try:
		clientSocket.connect((host,port))
		# print "Socket connected"
	except socket.error as e:
		print e
		
		sys.exit("problem in connecting to a socket")
	return clientSocket



def sndmsg(message,sock):
	# print message
	try:
		sock.sendall(message)
		stat = "message successfully sent"
	except :
		stat = "message send failed"
		sys.exit()
	return stat

def recmsg(sock,request):
	i=0;
	while 1:
		i=i+1
		data=sock.recv(4096)
		
		if len(data)==0 and i<5:
			# print('continue')
			sndmsg(request,sock)
			# print(request)
			continue
			
		elif i>=5:
			sys.exit("no data read")
			
		else:
			break
	return data
	
def handle_req(request,sock):
	sock1=create_sock(host,port)
	sock=sock1
	sndmsg(request,sock)
	# print request
	
	reply=recmsg(sock,request)
	# print reply
	return reply
	

