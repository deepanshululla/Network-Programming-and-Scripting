#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import socks
import web
import header


len1 = len(sys.argv)
if len1 == 3:
	username = sys.argv[1]
	password = sys.argv[2]
else:
	print "wrong number of arguments passed"
	sys.exit()

host='fring.ccs.neu.edu'
port=80
unvisited=[]
visited=[]
flags=[]
hrefs=[]

#Create Socket 
sock = socks.create(host,port) 

#login to the server
cookie = web.login(sock,host,username,password)

path = "/fakebook/"
[links,body,sock] = web.href(host,path,cookie,sock,port) 
result = header.search(body,flags)
flags = result
print links

while len(flags)<5:
	unvisited = []
	for x in range(len(links)):

		if links[x] in visited:
			print "Link present"
		else:
			unvisited.append(links[x])

	links = []

	for x in range(len(unvisited)):
		hreflink = unvisited[x]
		[hrefs,body,sock1] = web.href(host,hreflink,cookie,sock,port)
		sock = sock1
		result = header.search(body,flags)
		flags = result
		
		if (len(flags) == 5):
			web.printflags(flags)
			sys.exit()			
		
		visited.append(hreflink)
		links.extend(hrefs)

	links = sorted(set(links))		
	
