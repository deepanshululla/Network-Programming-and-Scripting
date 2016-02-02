#!/usr/bin/python

import header
import socks
import sys 

def login(sock,host,username,password):

	loginreq = header.get(host,'/accounts/login/?next=/fakebook/')
	socks.sndmsg(loginreq,sock)
	data = socks.recmsg(sock)
	[status,body,head] = header.exthead(data)
	if status == "200":
		[csrf,session] = header.cookie(head)	
	else:
		print "Status "+status+" Found"
		sys.exit()
	
	postdata = 'csrfmiddlewaretoken=%s&username=%s&password=%s&next=' % (csrf, username, password)
	request = 'POST /accounts/login/ HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nContent-Length: %d' \
                  '\r\nContent-Type: application/x-www-form-urlencoded\r\nCookie: csrftoken=%s; sessionid=%s' \
                  '\r\n\r\n%s' % (host, len(postdata), csrf, session, postdata)

	while True:
	
		socks.sndmsg(request,sock)
		data = socks.recmsg(sock)	
		[status,body,head] = header.exthead(data)
		if status == "302":
			[csrf1,session1] = header.cookie(head)
			cookie = [csrf,session1]
			break
		else:
			print "try again"

	return cookie

def href(host,path,cookie,sock,port):
	request = header.crawlget(host,path,cookie)
	socks.sndmsg(request,sock)
	data = socks.recmsg(sock)
	[status,body,head] = header.exthead(data)

	if data == "fail":
		[body,head,sock1] = header.errorhandle(host,path,cookie,sock,port)
		sock = sock1	

	else:
		if status == "200":
			print ""
		else:
			print "500 internal server error"
               		[body,head,sock1] = header.errorhandle(host,path,cookie,sock,port)
			sock = sock1

	links = header.sephref(body)	
	return [links,body,sock]


def printflags(secflags):
	for strn in secflags:
                secret = strn.split(':')[2].split(' ')[1].split('<')[0]
                print secret
                
	
