from __future__ import print_function
import webs
import sys
import linkXtract
#[socket,status,cookie,http body]=webs.anlyze((url2analyze,port),path)
# server="en.wikipedia.org/wiki/Reverse_DNS_lookup"
url2analyze=sys.argv[1]
#url2analyze="www.northeastern.edu"
port=80


r=webs.anlyze((url2analyze,port),'/')
body=str(r[3])
header_data=str(r[4])
header_dictionary=webs.headerXtract(header_data)
urlList=linkXtract.xtract2(body,url2analyze)
print(urlList)
# print(header_data)
print("the status code is " +str(r[1]))
print('the cookie is '+str(r[2]))

