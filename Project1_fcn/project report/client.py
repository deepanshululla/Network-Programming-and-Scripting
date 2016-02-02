#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import ssl
import socket
import inputchk
import socks
import solution

#Check the input arguments supplied

length = len(sys.argv)
i=0
parms = []
for i in range(0,length):
	parms.append((sys.argv[i]))

if length == 6:
	host, port, ID = inputchk.input_1(parms)
	#python client.py −p <port> −s [hostname] [NEU ID]
	#python client.py −p 27994 −s login.ccs.neu.edu 001798574
	#python client.py −p 27994 −s login.ccs.neu.edu 001901571
	sock = socks.create_ssl_sock(host, port)
elif length == 5:
	host, port, ID = inputchk.input_2(parms)
	#python client.py −p <port> [hostname] [NEU ID]
	#python client.py −p 27993 login.ccs.neu.edu 001798574
	#python client.py −p 27993 login.ccs.neu.edu 001901571
	sock = socks.create_sock(host, port)
elif length == 3:
	host, port, ID = inputchk.input_3(parms)
	#python client.py [hostname] [NEU ID]
	#python client.py login.ccs.neu.edu 001798574
	#python client.py login.ccs.neu.edu 001901571
	sock = socks.create_sock(host, port)
elif length == 4:
	host, port, ID = inputchk.input_4(parms)
	#python client.py -s [hostname] [NEU ID]
	#python client.py −s login.ccs.neu.edu 001798574
	#python client.py −s login.ccs.neu.edu 001901571
	sock = socks.create_ssl_sock(host, port)
else:
	sys.exit("Wrong number of arguments passed")

#create client socket

# sock = socks.create_sock(host, port)

message = "cs5700fall2015 HELLO " + ID + "\n"
print message
stat = socks.sndmsg(message, sock)
print stat

data = socks.recmsg(sock)
print data

msgs = data.split()

while True:
	if msgs[1] == "STATUS":
		num1 = msgs[2]
		num2 = msgs[4]
		op = msgs[3]

		if op == "+":
			sol = solution.sum(num1, num2)
		elif op == "-":
			sol = solution.sub(num1, num2)
		elif op == "*":
			sol = solution.mul(num1, num2)
		elif op == "/":
			sol = solution.div(num1, num2)
		else:
			print "unrecognized operator"

		solmsg = "cs5700fall2015 " + sol + "\n"
		print solmsg
     
		stat = socks.sndmsg(solmsg, sock)
		print stat

	elif msgs[2] == "BYE":
		result = msgs[1]
		break
	elif not msgs:
		print "No data received"
		sys.exit()
	else:
		print "Unexpected data received"
		sys.exit()

	data = socks.recmsg(sock)
	print data
	msgs = data.split()

print result
