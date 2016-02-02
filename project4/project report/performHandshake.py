import socks
import socket
import netUtils
import layer3
import layer4
from random import randint
#source_ip=netUtils.get_source_ip()

def sendSyn(source_ip,destination_ip, source_port):
	
	soc = socks.createSendSock()
	ip_header = layer3.packHeader(source_ip,destination_ip)
	seq = randint(0,42949)
	
	ack =0 
	tcp_header = layer4.packTCPHeader(source_ip,destination_ip, source_port, seq, ack,'SYN','')
	pck = ip_header + tcp_header
	soc.sendto(pck,(destination_ip,80))
	#print "SYN packet sent with seq:"+str(seq)
	#msg=socks.recv(soc)
	soc.close()
	
	return [seq,ack]
	
	
def recPacket(destn_ip):
	
	recsock=socks.createRecvSock()
	while True:
		raw = socks.recv(recsock)
		
		ihl,tcph,source_ip,dest_ip,iph,data,payL = netUtils.xtractPacket(raw) 
		#server_ack=tcph[3]
		
		if source_ip == destn_ip and tcph[0]==80 and tcph[5]==18:
			#print "SYNACK recieved"
			#print tcph
			break
		
			
	
	return tcph
def sendAck(source_ip,destination_ip, source_port,seqNo,ackNo):
	soc = socks.createSendSock()
	ip_header = layer3.packHeader(source_ip,destination_ip)
	seq = seqNo
	
	ack =ackNo
	tcp_header = layer4.packTCPHeader(source_ip,destination_ip, source_port, seq, ack,'ACK','')
	pck = ip_header + tcp_header
	soc.sendto(pck,(destination_ip,80))
	#print "Ack packet sent"
	#msg=socks.recv(soc)
	soc.close()
	return seq	


