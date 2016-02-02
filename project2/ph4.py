
#the purpose of ph4 is to invoke URL lists
#work on status code management, not visiting root page again or already visited pages,
#BFS/DFS to search among urls


#what ph4 already did
#-status code management done
#-not visiting root page again 
#what's left
#-create a dynamic list of urls
#use bfs/dfs

#stat manage has to be done in main code 
from __future__ import print_function
import webs
import sys
import linkXtract
#[socket,status,cookie,http body,header_data]=webs.anlyze((url2analyze,port),path)
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output 
	
	
url2analyze=str(sys.argv[1])
url=url2analyze
[server,path]=webs.serverNameExtract(url2analyze)
url2analyze=linkXtract.urlFilter(url,server)



port=80


r=webs.anlyze((url2analyze,port),'/')
body=str(r[3])
header_data=str(r[4])

header_dictionary=webs.headerXtract(header_data)

urlList=linkXtract.xtract(body,server)

# print(header_data)
print("the status code is " +str(r[1]))
print('the cookie is '+str(r[2]))

for url in urlList:
	[server,path]=webs.serverNameExtract(url)
	if server in url2analyze:
		w=webs.anlyze((server,port),path)
		
		
			
		
print('total links scanned:'+str(len(urlList)))
print(urlList)