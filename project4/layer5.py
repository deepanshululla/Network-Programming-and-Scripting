import layer3
import layer4
import socket
import socks
CRLF = "\r\n"

def reqGenGet(server,path):
	k1="GET "+path+" HTTP/1.1"
	reqRtn=[k1,"Host:"+server,"Connection: keep-alive","","",]
	request=CRLF.join(reqRtn)
	return request

def sendAck(source_ip,destination_ip, source_port,seqNo,ackNo):
	soc = socks.createSendSock()
	ip_header = layer3.packHeader(source_ip,destination_ip)
	
	tcp_header = layer4.packTCPHeader(source_ip,destination_ip, source_port, seqNo, ackNo,'ACK','')
	pck = ip_header + tcp_header
	soc.sendto(pck,(destination_ip,80))
	#print "Ack packet sent"
	#msg=socks.recv(soc)
	soc.close()
		
def sendFinAck(source_ip,destination_ip, source_port,seqNo,ackNo):
	soc = socks.createSendSock()
	ip_header = layer3.packHeader(source_ip,destination_ip)
	
	tcp_header = layer4.packTCPHeader(source_ip,destination_ip, source_port, seqNo, ackNo,'FINACK','')
	pck = ip_header + tcp_header
	soc.sendto(pck,(destination_ip,80))
	#print "Ack packet sent"
	#msg=socks.recv(soc)
	soc.close()
		
def xtractHeaders(response):
	
	try:
		
		header_data,gar,body = response.partition(CRLF+CRLF)
		#header_data=l[0]
		
		#print(header_data)
		#body=l[2]
		#print body
		
		#header_array=header_data.split(CRLF)
		
		#statusLine=header_array[0]
		#statusArray=statusLine.split()
		#stat=statusArray[1]
		#header_dictionary=headerXtract(header_data)
		#cokie='not available'
			
		rtn=[header_data,body]
		
		
	except:
		sys.exit("Failed to seperate html page from header")
	return rtn
	
#GET / HTTP/1.0
