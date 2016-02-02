#!/usr/bin/python

import socket
import sys
from timeit import default_timer
import netUtils
import layer5
import layer4
##### Create a RAW Send Socket #####
def createSendSock():
	try:
		sendSock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error , mssg:
		print 'Socket could not be created. Error Code : ' + str(mssg[0]) + ' Message ' + msg[1]
		sys.exit()
	return sendSock


##### Create a RAW Receive Packet #####
def createRecvSock():
	try:
		recsock = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.IPPROTO_TCP)
	except socket.error , msg:
		print 'Socket2 could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	return recsock
	
	
def send(msg,sock,dest_ip):
	sock1=createSendSock()
	sock=sock1
	sock.sendto(msg, (dest_ip , 0 ))
	sock1.close()

def recv(sock):
	
	start = default_timer()
	sock1=createRecvSock()
	sock=sock1
	msg=sock.recvfrom(65565)
	
	if not msg and duration>60:
		
			sys.exit("time out occured")
		
	sock1.close()
	return msg
#############################################################################

##So the order after handhskake is 


	
	
def closeConnection(source_ip,destination_ip, source_port,client_seq,client_ack):
	
	
	layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
	layer5.sendFinAck(source_ip,destination_ip, source_port,client_seq,client_ack)
	print "attempting to close connection"

def debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack):
	print "Client sequence no " +str(client_seq)
	print "Client ack no " +str(client_ack)
	print "server sequence " +str(server_seq)
	print "server ack no " +str(server_ack)


#############################################################################
def getImpData(raw1):
	ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
	[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
	[src_port,dest_port]=layer4.getPorts(tcph)
	flag=layer4.getPacType(tcph)
	return [src_ip,server_seq,server_ack,dest_port,payLength,flag,data]


	


def recData(destination_ip,source_ip,source_port,client_seq,client_ack,server_seq,server_ack):

# declaring variables
	data1=''
	recsock=createRecvSock()
	server_seq_dict={}
	server_ack_dict={}
	i=1
	dup_pac_count=0
	ack_dict={}
	
	raw1 = recv(recsock)
	[src_ip,server_seq,server_ack,dest_port,payLength,flag,data]=getImpData(raw1)
	dict_seq=str(server_seq)+"."+str(server_ack)
	serverSeqList=server_seq_dict.keys()
# while loop
	while True:
		if src_ip == destination_ip and dest_port==source_port and (dict_seq not in serverSeqList) and payLength>0 and flag!="FINACK":
	##considering only packets with non duplicate packets with data		
			client_seq=server_ack
			client_ack=payLength+server_seq
			#chkSum=layer4.getTcpCheckSum(source_ip, destination_ip,tcp_header,data)
			dict_seq=str(server_seq)+"."+str(server_ack)
			server_seq_dict[str(server_seq)+"."+str(server_ack)]=data
			server_ack_dict[str(server_seq)+"."+str(server_ack)]=str(client_seq)+'.'+str(client_ack)
			serverSeqList=server_seq_dict.keys()
			
			layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			i+=1
			print flag+ " recieved. Packet " + str(i)+". packet length "+ str(payLength)
			#server_ack=client_seq
			#server_seq=client_ack
			raw1 = recv(recsock)
			[src_ip,server_seq,server_ack,dest_port,payLength,flag,data]=getImpData(raw1)
			dict_seq=str(server_seq)+"."+str(server_ack)
			
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq not in serverSeqList) and payLength==0 and flag!="FINACK" : ##considering only 	packets with acks with no datas
			client_seq=server_ack
			client_ack=server_seq
			
			ack_dict[str(client_seq)+'.'+str(client_ack)]=str(server_seq)+'.'+str(server_ack)
			server_ack_dict[str(server_seq)+"."+str(server_ack)]=str(client_seq)+'.'+str(client_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			#print flag+ " recieved"
			#server_ack=client_seq
			#server_seq=client_ack	
			raw1 = recv(recsock)
			[src_ip,server_seq,server_ack,dest_port,payLength,flag,data]=getImpData(raw1)
			dict_seq=str(server_seq)+"."+str(server_ack)				
		elif dup_pac_count>18:
			break
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq in serverSeqList) and payLength==0 and dup_pac_count<18: ##considering only duplicate packets with acks no data
			dup_pac_count+=1
			
			raw1 = recv(recsock)
			[src_ip,server_seq,server_ack,dest_port,payLength,flag,data]=getImpData(raw1)
			dict_seq=str(server_seq)+"."+str(server_ack)
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq in serverSeqList) and payLength>0 and dup_pac_count<18: ##considering only duplicate packets with data
			dup_pac_count+=1
			#print flag+ " recieved"
			kValue=server_ack_dict[dict_seq]
			clis_seq,clis_ack=kValue.split('.')			
			cli_seq=int(clis_seq)
			cli_ack=int(clis_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,cli_seq,cli_ack)
			#print "ack sent for the packet with seq no. "+str(cli_seq)+" and  ack no. " +str(cli_ack)
			raw1 = recv(recsock)
			[src_ip,server_seq,server_ack,dest_port,payLength,flag,data]=getImpData(raw1)
			dict_seq=str(server_seq)+"."+str(server_ack)

		elif src_ip == destination_ip and dest_port==source_port and (flag=='FINACK' or flag=='FIN'):
			#print "FINACK recieved"			
			#debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			##close connection if fin or finack recieved
			#print flag+ " recieved"
			client_seq=server_ack
			client_ack=1+server_seq
			#closeConnection(source_ip,destination_ip, source_port,client_seq,client_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			layer5.sendFinAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			break
		else:
			#debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			if src_ip == destination_ip and dest_port==source_port:
				sys.exit("No condition met.Unknown problem")
	arrList=server_seq_dict.keys()
	#arrList = [ double(x) for x in arrList ]## converting every sting seq-ack combo into integer
	arrList.sort()
	#print server_seq_dict	
	for i in arrList:
		data1=data1+server_seq_dict[i]
	#print data1
	print "Data end"	
		#continue
	return data1
