from __future__ import print_function
import os
import sys
import socket
import socks
import layer2
import layer3
import layer4
import layer5
import netUtils
import performHandshake






source_ip=netUtils.get_source_ip()
source_mac=netUtils.get_source_mac()
source_port=netUtils.getFreePort()
host,path=netUtils.serverNameExtract(sys.argv[1])

destination_ip=socket.gethostbyname(host)
#print(dest_ip)
#129.10.116.81
dest_port=80

def handshake(source_ip,dest_ip,source_port):
	client_seq,client_ack=performHandshake.sendSyn(source_ip,dest_ip,source_port)
	print("syn packet sent")	
	tcph = performHandshake.recPacket(dest_ip)
	
	server_seq=0
	server_ack=tcph[3]
	print (str(client_seq)+ " is our generated seq No.")	
	print(str(server_ack)+ " is ackNo given by server")
	server_seq=tcph[2]
	print(str(server_seq)+ " is server's seqNo generated by server") #seq
	client_seq=server_ack
	client_ack=server_seq+1
	print("synack packet recieved")	
	
	performHandshake.sendAck(source_ip,dest_ip,source_port,client_seq,client_ack)
	print("ack packet sent.Connetion seems to be established")
	
	
	server_seq=client_ack
	server_ack=client_seq+1	
	
	return [client_seq,client_ack,server_seq,server_ack]



	



def pageRequest(url,source_ip,destination_ip,client_seq,client_ack,server_seq,server_ack):
	host,path=netUtils.serverNameExtract(sys.argv[1])
	data_req=layer5.reqGenGet(host,path)
	print(data_req)
	tcp_header = layer4.packTCPHeader(source_ip,destination_ip, source_port, client_seq, client_ack,'PSHACK',data_req)
	ip_header = layer3.packHeader(source_ip,destination_ip)
	
	pck = ip_header + tcp_header + data_req
	soc = socks.createSendSock()
	recsock=socks.createRecvSock()	
	soc.sendto(pck,(destination_ip,80))
	raw=socks.recv(recsock)
	ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw)
	soc.close()
	recsock.close
	#socks.debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
	[server_seq2,server_ack2]=layer4.getServerSeqNo(tcph)
	k=len(data_req)+client_seq
	#print("k="+str(k)) 
	#socks.debugPrintSeqNo(client_seq,client_ack,server_seq2,server_ack2)
	if tcph[5]==0x010 and tcph[1]==source_port and server_ack2==k and server_seq2==server_seq:
		print("ACK packet recieved for get. handshake done")	
		#body=downloadPage(tcph,iph,source_ip,destination_ip,client_seq,client_ack)
		data=socks.recData(destination_ip,source_ip,source_port,client_seq,client_ack,server_seq2,server_ack2)
		header_data,body=layer5.xtractHeaders(data)
	#print(header_data)
	else:
		sys.exit("NO ack recieved for GET.pLease try later")
	return body

def fileWrite(fileName,data):
	f = open(fileName, 'w')
	f.write(data)
	b = os.path.getsize(fileName)
	#print("The size of file is "+ str(b))
	f.close()

def main():
	if len(sys.argv) != 2:

		sys.exit("Wrong number of arguments passed")
	url = sys.argv[1]
	os.system("sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP")
	#print(source_ip)
	client_seq,client_ack,server_seq,server_ack=handshake(source_ip,destination_ip,source_port)
	
	page=pageRequest(url,source_ip,destination_ip,client_seq,client_ack,server_seq,server_ack)
	#print(page)
	fileName=netUtils.get_filename(url)
	print(fileName +"is being created")
	fileWrite(fileName,page)
	#stat,body,header_data=layer5.xtractHeaders(fileName)
	

if __name__ == '__main__':
    main()

#python ph1.py http://www.ccs.neu.edu/home/cbw/4700/2MB.log
