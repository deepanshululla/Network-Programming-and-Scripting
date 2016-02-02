
#the purpose of ph4 is to invoke URL lists
#work on status code management, not visiting root page again or already visited pages,
#BFS/DFS to search among urls

#stat manage has to be done in main code 
from __future__ import print_function
import webs
import sys
import linkXtract
#[socket,status,cookie,http body]=webs.anlyze((url2analyze,port),path)

url2analyze=str(sys.argv[1])



port=80


r=webs.anlyze((url2analyze,port),'/')
body=str(r[3])
header_data=str(r[4])
header_dictionary=webs.headerXtract(header_data)
[server,path]=webs.serverNameExtract(url2analyze)
urlList=linkXtract.xtract2(body,server)

# print(header_data)
print("the status code is " +str(r[1]))
print('the cookie is '+str(r[2]))

for url in urlList:
	[server,path]=webs.serverNameExtract(url)
	
	w=webs.anlyze((server,port),path)
	responseCode=int(w[1])
	responseCheck=responseCode/100
	if responseCheck==2:
		print(url+' is checked and it is okay')
	elif responseCode==3:
		print(url+' is checked and it is asking us to redirect')
	elif responseCode==4:
		print(url+' is checked and we need to abort this html')
	else: 
		print(url+ ' is invalid')
print('total links scanned:'+str(len(urlList)))
