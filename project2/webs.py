#purpose of this is to create a function which can return a socket
#and http page,return cookie,return status code
from __future__ import print_function
import socket
import sys
CRLF = "\r\n"


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


	

def reqGen(server,path):
	k1="GET "+path+" HTTP/1.1"
	reqRtn=[k1,"Host:"+server,"Connection: Close","","",]
	return reqRtn
	
def findBtw(s,start_char,end_char):
	start = s.find(start_char)
	end= s.find(end_char, start)
	return [start,end]
	
	
def serverNameExtract(url):
	q=url.find('/')
	if q!=-1:
		server=url[0:q]
		path=url[q:len(url)]
	
	if q==-1:
		server=url
		path='/'
	return [server,path]
	
def anlyze((url2analyze,port),path):
	
	#[socket,status,cookie,http body,header_data]=anlyze((url2analyze,port),path)
	
	
	try:
		clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		[server,path]=serverNameExtract(url2analyze)
		serverIp=str(socket.gethostbyname(server))
		clientSocket.connect((serverIp,port))
		request=reqGen(server,path)
		clientSocket.send(CRLF.join(request))
		response = ''
		buffer = clientSocket.recv(4096)
		while buffer:
			response += buffer
			buffer = clientSocket.recv(4096)
		# print(buffer)

	# HTTP headers are separated from the body by an empty line
		header_data, _, body = response.partition(CRLF + CRLF)
		#print(header_data)
		header_array=header_data.split(CRLF)
		
		statusLine=header_array[0]
		statusArray=statusLine.split()
		stat=statusArray[1]
		header_dictionary=headerXtract(header_data)
		cokie='not available'
		if stat=='200':
			try:
				cookieLine=header_dictionary['Set-Cookie']
				[start,end]=findBtw(cookieLine,'=',';')
				start=start+1
				cokie=cookieLine[start:end]
			except:
				cokie='not available'
		
		rtn=[clientSocket,stat,cokie,body,header_data]
		
		# print(stat)
		# print(cokie)
		# print(rtn[3])
		
		

	except:
		print(url2analyze+" DNS records not found")
		rtn=['','900','','','']
			
	return rtn	
	
	