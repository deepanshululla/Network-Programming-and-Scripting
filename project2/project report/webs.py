#purpose of this is to create a function which can return a socket
#and http page,return cookie,return status code
from __future__ import print_function
import socket
import sys
import re

CRLF = "\r\n"

def xtractLinks(body):
	pattern = re.compile(r'<a href=\"(/fakebook/[a-z0-9/]+)\">')
	links = pattern.findall(body)
	
	return links
		


def headerXtract(header_data):
	
	header_dictionary={}
	header_array=header_data.split(CRLF)
	statusLine=header_array[0]
	statusArray=statusLine.split()
	stat=statusArray[1]
	header_array2=header_array[1:len(header_array)]
	for lines in header_array2:
		hld=lines.split(':')
		# print(hld)
		header_dictionary[hld[0]]=hld[1]
	return header_dictionary

def	getLocation(header_data):
	header_dictionary={}
	header_array=header_data.split(CRLF)
	statusLine=header_array[0]
	statusArray=statusLine.split()
	stat=statusArray[1]
	header_array2=header_array[1:len(header_array)]
	for lines in header_array2:
		if "Location:" in lines:
			location=lines.split('Location:')[1]
			path=location.split('http://fring.ccs.neu.edu')[1]
			
	return path
	
def breakCookie(header_data):
	csrf_pattern = re.compile(r'csrftoken=([a-z0-9]+);')
	session_pattern = re.compile(r'sessionid=([a-z0-9]+);')
	header_dictionary=headerXtract(header_data)
	cookieLine=header_dictionary['Set-Cookie']

	if 'csrftoken' in header_data:
		csrfToken = csrf_pattern.findall(header_data)[0]
		
	else:
		csrfToken=''
	if 'sessionid' in cookieLine:
		sessionId = session_pattern.findall(cookieLine)[0]
		
	else:
		sessionId=''
	
	return [csrfToken,sessionId]

def reqGenGet(server,path):
	k1="GET "+path+" HTTP/1.1"
	reqRtn=[k1,"Host:"+server,"Connection: keep-alive","","",]
	request=CRLF.join(reqRtn)
	return request
	
def reqGenCrawl(server,path,userName,password,cokie):
	
	k1="GET "+path+" HTTP/1.1"
	reqRtn=[k1,"Host: "+server,"Connection: keep-alive","Cookie: csrftoken="+cokie[0]\
			+"; sessionid= "+cokie[1],"",""]
	
	request=CRLF.join(reqRtn)
	return request
	

def reqGenPut(server,userName,password,cokie):
	postdata = 'csrfmiddlewaretoken=%s&username=%s&password=%s&next=' % (cokie[0], userName, password)
	request = 'POST /accounts/login/ HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nContent-Length: %d' \
                  '\r\nContent-Type: application/x-www-form-urlencoded\r\nCookie: csrftoken=%s; sessionid=%s' \
                  '\r\n\r\n%s' % (server, len(postdata), cokie[0], cokie[1], postdata)
	return request	

def findBtw(s,start_char,end_char):
	start = s.find(start_char)
	end= s.find(end_char, start)
	fl=s[start:end]
	return fl
	
	
def serverNameExtract(url):
	
	# l1=url.find('http://')
	# l2=url.find('https://')
	# print(url)
	# if l1!=-1:
		# url1=url.split('http://')[1]
	# if l2!=-1:
		# url1=url.split('https://')[1]
	q=url.find('/')
	# print(url1)
	if q!=-1:
		server=url[0:q]
		
		path=url[q:len(url)]
		if path[len(path)-1]!='/':
			path=path+'/'
	if q==-1:
		server=url
		path='/'
	return [server,path]
	
def findSecretFlag(page):
	

	
	flagShip=findBtw(page,"<h2 class='secret_flag' style=",'</h2>')
	flag=flagShip.split(':')[2]
	return flag
	
	
def xtractInfo(response):
	
	try:

		header_data, _, body = response.partition(CRLF + CRLF)
		#print(header_data)
		header_array=header_data.split(CRLF)
		
		statusLine=header_array[0]
		statusArray=statusLine.split()
		stat=statusArray[1]
		header_dictionary=headerXtract(header_data)
		cokie='not available'
			
		rtn=[stat,body,header_data]
		status=stat	
		if status == '403' or status == '404':
			print('403 or 404 page not found Error')
		elif status == '301':  # redirect to a new url
			print('301 Redirect')
		elif status == '500':  # Internal Server Error
			d=2
		else:
			d=3
	except:
		rtn=['900','','']
		
	
	
			
	return rtn