#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import time

host='fring.ccs.neu.edu'
port=80
# Creating a socket

def create(host,port):
	try :
		clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print "Socket Created"

	except socket.error as e:
		
		print e
		sys.exit("Failed to create socket error code")    

	try:
		clientSocket.connect((host,port))
		print "Socket Connected"

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

def recmsg(sock):

	data=sock.recv(4096)
		
	if len(data) == 0:
		print('data not recieved')
		data = "fail"			
			
	return data

