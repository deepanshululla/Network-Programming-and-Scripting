#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import socks
import webs
import re
import socket
import linkXtract

#Host: fring.ccs.neu.edu/fakebook/

#declaring global variables
CRLF = "\r\n"
host='fring.ccs.neu.edu'

port=80
# password='CQA2F4BJ'
# userName='001798574'
password=sys.argv[2]
userName=sys.argv[1]
cokie=[]
url_unvisited=['/fakebook/']
url_visited=[]
flag_list=[]




def login(sockObject):
	request1=webs.reqGenGet(host,'/accounts/login/?next=/fakebook/')
	#print(request1)
	response1=socks.handle_req(request1,sockObject)
	
	# print(response1)
	[stat,body,header_data]=webs.xtractInfo(response1)
	
	#print(header_data)
	
	
	if stat=='200':
		try:
			cokie=webs.breakCookie(header_data)		
		except Exception as e:
			cokie=[]
			print(e)
			sys.exit("Cookie not available for login")
			
		request2=webs.reqGenPut(host,userName,password,cokie)
		response2=socks.handle_req(request2,sockObject)
		[stat,body,header_data]=webs.xtractInfo(response2)
		
		[csrf2,sessionId2]=webs.breakCookie(header_data)
		csrf1=cokie[0]
		cokie=[csrf1,sessionId2]
		path='/fakebook/'
		request21=webs.reqGenCrawl(host,path,userName,password,cokie)
		response21=socks.handle_req(request21,sockObject)
		[stat,body,header_data]=webs.xtractInfo(response21)
		header_dictionary=webs.headerXtract(header_data)
	# print(response3)
	else:
		sys.exit("Not able to login")
	
	return [response21,cokie] 
	
def profileLinkCrawl(profileLink,cokie,sockObject):
		
	requestN=webs.reqGenCrawl(host,profileLink,userName,password,cokie)
	responseN=socks.handle_req(requestN,sockObject)
	[status,body,header_data]=webs.xtractInfo(responseN)
	while 1:
		if status=='500':
		
			sock1=socks.create_sock(host,port)
			requestN=webs.reqGenCrawl(host,profileLink,userName,password,cokie)
			responseN=socks.handle_req(requestN,sock1)
			[status2,body,header_data]=webs.xtractInfo(responseN)
			
			if status2=='200':
				sockObject=sock1
				break
			else:
				status=status2
				continue
				
		else:
			break	
		
	try:
		urlList=linkXtract.xtract3(body)
		if "<h2 class='secret_flag' style=" in body:
			flagCheck=webs.findSecretFlag(body)
			flag_list.append(flagCheck)
		for profileLink2 in urlList:
			if profileLink2 not in url_unvisited and profileLink not in url_visited:
				url_unvisited.append(profileLink2)	
		
	except:
		sys.exit("Problem in profileLinkCrawl")
	
		
	
	return [status,body,header_data]
	

	
		
		
def crawl(cokie,sockObject,response):
	
	[stat,body,header_data]=webs.xtractInfo(response)
	urlCheck=linkXtract.xtract3(body)
	i=0;
	
	for profileLink in urlCheck:
		url_unvisited.append(profileLink)
		if profileLink not in url_visited:
			profileLinkCrawl(profileLink,cokie,sockObject)
			url_visited.append(profileLink)
			i=i+1
		
			try:
				url_unvisited.remove(profileLink)
				
			except:
				print("item not in list")
		else:
			continue
	
	while len(flag_list)<5:
		urlCheck=url_unvisited
		for profileLink in urlCheck:
			if profileLink in url_visited:
				continue
			else:
				profileLinkCrawl(profileLink,cokie,sockObject)
				url_visited.append(profileLink)
				i=i+1
			
				try:
					url_unvisited.remove(profileLink)
				
				except:
					print("item not in list")
		urlCheck=url_unvisited
		sock2=socks.create_sock(host,port)
		sockObject=sock2	

	
	# print("The number of itiretions are "+str(i))
		
	# print(url_unvisited)
	# print(url_visited)
	# print(flag_list)
	for flag in flag_list:
		print(flag)

	
	
	
	

	
				



def main():
	#creating socket connection
	crawlerSocket=socks.create_sock(host,port)
	if (len(sys.argv) != 3):
		sys.exit('Please pass correct number of arguments')
    #python webcrawler.py 001798574 CQA2F4BJ
	#python webcrawler.py 001901571 EKAOJN77
	response,cokie=login(crawlerSocket)
	crawl(cokie,crawlerSocket,response)

if __name__ == '__main__':
    main()
