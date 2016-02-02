#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import ssl
import time

# Creating a socket

def create_sock(host, port):
	try :
		clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	except socket.error:
		print "Failed to create socket error code"
		sys.exit()    

	clientSocket.connect((host , port))
	print "Socket connected"
	return clientSocket
	
def create_ssl_sock(host, port):
	try :
		clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sslSocket = ssl.wrap_socket(clientSocket,ssl_version=ssl.PROTOCOL_TLSv1,certfile=None,server_side=False)
	except socket.error:
		print "Failed to create socket error code"
		sys.exit()    

	sslSocket.connect((host,port))
	print "Socket connected"
	return sslSocket	


def sndmsg(message, sock):
	print message
	try:
		sock.sendall(message)
		stat = "message successfully sent"
	except :
		stat = "message send failed"
		sys.exit()
	return stat

def recmsg(sock):
	while True:
		data=sock.recv(4096)
		if len(data) == 0:
			print "Continue"
		else:
			break
	return data

