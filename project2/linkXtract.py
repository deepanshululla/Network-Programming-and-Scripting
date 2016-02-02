from bs4 import BeautifulSoup

def findBtw(s,start_char,end_char):
	start = s.find(start_char)
	end= s.find(end_char, start)
	return [start,end]
def urlFilter(url,server):
	#extract http:// and htttps://
	l0=url.find('www')
	l1=url.find('http://')
	l2=url.find('https://')
	elem=url
	if l2==-1 and l1==-1 and l0==-1:
			[start,end]=findBtw(url,'/','"')
			fg=url[start:end]
			url=server+fg
		
	if l0!=-1:
			#find all links starting with www
			[start,end]=findBtw(elem,'www','"')
			end=end+1
			url=elem[start:end]
			
	if l1!=-1 and l0==-1:
			#find all links starting with http://
			[start,end]=findBtw(elem,'http://','"')
			start=start+7
			url=elem[start:end]
			
			# print('Check 2:'+url)
			
	l2=elem.find('https://')
	if l2!=-1 and l1==-1 and l0==-1:
		#find all links starting with https://
		[start,end]=findBtw(elem,'https://','"')
		start=start+8
		url=elem[start:end]
		
	return url	
def xtract(body,server):
	body_line1=body.split('>')
	urlList=[]
	
	for elem in body_line1:
		l0=elem.find('www')
		if l0!=-1:
			#find all links starting with www
			[start,end]=findBtw(elem,'www','"')
			url=elem[start:end]
			urlList.append(url)
			
		l1=elem.find('http://')
		if l1!=-1 and l0==-1:
			#find all links starting with http://
			[start,end]=findBtw(elem,'http://','"')
			start=start+7
			url=elem[start:end]
			urlList.append(url)
			# print('Check 2:'+url)
			
		l2=elem.find('https://')
		if l2!=-1 and l1==-1 and l0==-1:
			#find all links starting with https://
			[start,end]=findBtw(elem,'https://','"')
			start=start+8
			url=elem[start:end]
			urlList.append(url)
			# print('Check 3:'+url)
			
		
		l3=elem.find('href')
		if l3!=-1 and l2==-1 and l1==-1 and l0==-1:
			#find all links starting with a path name
			[start,end]=findBtw(elem,'/','"')
			fg=elem[start:end]
			url=server+fg
			urlList.append(url)
			# print('Check 4:'+url)
		
			
	return urlList
	# print('total links scanned:'+str(len(urlList)))
	

		
		
def xtract2(body,server):
	urlList=[]
	soup = BeautifulSoup(body,'html.parser')
	for link in soup.find_all('a'):
		url=str(link.get('href'))
		elem=url
		url=urlFilter(url,server)
		urlList.append(url)
	return urlList