from __future__ import print_function
import webs
import linkXtract
#[socket,status,cookie,http body,http header]=webs.anlyze((server,port),path)
# server="en.wikipedia.org/wiki/Reverse_DNS_lookup"
server="www.yellowpages.com"
port=80

r=webs.anlyze((server,port),'/')
body=str(r[3])
header_data=str(r[4])
urlList=linkXtract.xtract(body,server)

for url in urlList:
	[host,path]=webs.hostXtract(url)
	if host in server:
		w=webs.anlyze((server,port),path)
		if w[1]=='200':
			print(url+' is checked and it is okay')
print('total links scanned:'+str(len(urlList)))



