#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def input_1(parm):
	#python client.py −p <port> −s [hostname] [NEU ID]
	if parm[1] == "-p":
		if parm[2] == "27994":
			port = 27994
			if parm[3] == "-s":
				if parm[4] == "login.ccs.neu.edu":
					host = parm[4]
					if parm[5].isdigit():
						ID = parm[5]
					else:
						sys.exit("Enter numeric NEU ID")   
				else:
					sys.exit("Wrong hostname entered, use host 'login.ccs.neu.edu'")
			else:
				sys.exit("Err1: Enter the command in format: client <−p port> <−s (optional)> [hostname] [NEU ID]")  
		else:
			sys.exit("Wrong port supplied, use 27994")
	else:
		sys.exit("Err2: Enter the command in format: client <−p port> <−s (optional)> [hostname] [NEU ID]")              
	return (host, port, ID)


def input_2(parm):
	if parm[1] == "-p":
	#python client.py −p <port> [hostname] [NEU ID]
		if parm[2] == "27993":
			port = 27993
			if parm[3] == "login.ccs.neu.edu":
				host = parm[3]
				if parm[4].isdigit():
					ID = parm[4]
					
				else:
					sys.exit("Enter numeric NEU ID")
			else:
				sys.exit("Wrong hostname entered, use host 'login.ccs.neu.edu'")
		else:
			sys.exit("Wrong port supplied, use 27993")
	else:
		sys.exit("Enter the command in format: client <−p port> <−s (optional)> [hostname] [NEU ID]")
	return (host, port, ID)


def input_3(parm):
	#python client.py [hostname] [NEU ID]
	if parm[1] == "login.ccs.neu.edu":
		host = parm[1]
		if parm[2].isdigit():
			ID = parm[2]
		else:
			sys.exit("Enter numeric NEU ID")
	else:
		sys.exit("Wrong hostname entered, use host 'login.ccs.neu.edu'")
	port = 27993
	return (host, port, ID) 


def input_4(parm):
	#python client.py -s [hostname] [NEU ID]
	if parm[1] == "-s":
		if parm[2] == "login.ccs.neu.edu":
			host = parm[2]
			if parm[3].isdigit():
				ID = parm[3]
			else:
				sys.exit("Enter numeric NEU ID")
		else:
			sys.exit("Wrong hostname entered, use host 'login.ccs.neu.edu'")
	else:
		sys.exit("Enter the command in format: client <−p port> <−s (optional)>[hostname] [NEU ID]")
	port = 27994
	return (host, port, ID)

