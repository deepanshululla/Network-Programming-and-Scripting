#!/usr/bin/python
import re
import socks

CRLF = "\r\n"

def get(host,path):
	line1 = "GET "+path+" HTTP/1.1"
	getreq = [line1,"Host:"+host,"Connection: keep-alive","",""]
	request=CRLF.join(getreq)
	return request

def crawlget(host,path,cookie):
	line1="GET "+path+" HTTP/1.1"
	request=[line1,"Host: "+host,"Connection: keep-alive","Cookie: csrftoken="+cookie[0]\
			+"; sessionid= "+cookie[1],"",""]	
	request=CRLF.join(request)
	print request
	return request
	
def exthead(data): 
	headarray, _,body = data.partition(CRLF + CRLF)
	header = headarray.split(CRLF)
	stat = header[0].split(' ')
	if len(stat) == 1:
		status = "500"
	else:
		status = stat[1]

	rtn = [status, body, headarray]
	return rtn

def cookie(header):
	cookies = []
	csrf = re.compile(r'csrftoken=([a-z0-9]+);')
	session = re.compile(r'sessionid=([a-z0-9]+);')
	
	if 'csrftoken' in header:
		csrf = csrf.findall(header)[0]
	else:
		csrf = ''
	if 'sessionid' in header:
                session = session.findall(header)[0]
	else:
		session = ''

	cookies.append(csrf)
	cookies.append(session)
	return cookies

def sephref(data):
	pattern = re.compile(r'<a href=\"(/fakebook/[a-z0-9/]+)\">')
	links = pattern.findall(data)
	return links

def search(data,secflag):

	sec=re.findall(r'<h2 class=\'secret_flag\' style="color:red">FLAG: [0-9a-z]{64}</h2>',data,flags=re.I)
        for a in sec:
                if (a not in secflag):
                        secflag.append(a)
	return secflag
		
def errorhandle(host,path,cookie,sock,port):
	while True:
		sock1 = socks.create(host,port)
		request = crawlget(host,path,cookie)
		socks.sndmsg(request,sock1)
		data = socks.recmsg(sock1)
		[status,body,head] = exthead(data)

		if status == "200":
			rtn = [body,head,sock1]
			break	
		else:
			print status
		
	return rtn
