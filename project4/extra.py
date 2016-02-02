def recData(destination_ip,source_ip,source_port,client_seq,client_ack,server_seq,server_ack):
	
	print "Data started"
	
	data1=''
	recsock=createRecvSock()
	server_seq_dict={}
	server_ack_dict={}
	server_seq_dict[str(server_seq)+"."+str(server_ack)]=data1
	server_ack_dict[str(server_seq)+"."+str(server_ack)]=str(client_seq)+'.'+str(client_ack)
	i=1
	dup_pac_count=0
	raw1 = recv(recsock)
	ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
	[src_port,dest_port]=layer4.getPorts(tcph)
	
	#stat,body,header_data=layer5.xtractHeaders(data)
	#data1=data1+data
	print "Compare %s our destination ip with source ip of packet %s" %(str(src_ip),str(destination_ip))
	print "Compare %s our source port with deatination port of packet %s" %(str(source_port),str(dest_port))
	while True:
		ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
		[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
		dict_seq=str(server_seq)+"."+str(server_ack)
		[src_port,dest_port]=layer4.getPorts(tcph)
		flag=layer4.getPacType(tcph)
		print flag +" recieved"		
		#server_seq_dict[str(server_seq)+"."+str(server_ack)]=data
		
		serverSeqList=server_seq_dict.keys()
		
	
		
		if dup_pac_count>=7:
			sys.exit("too many duplicate packets")
			break
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq not in serverSeqList) and payLength>0: 
##considering only packets with non duplicate packets with data
			debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			server_seq,server_ack=dict_seq.split('.')
			print "Packet "+str(i)+ " recieved with seq no. %s and ack no. % s" %(server_seq,server_ack)
			cli_seq=int(server_ack)
			#cli_ack=int(server_seq)
			client_ack=payLength+int(server_seq)
			server_seq_dict[str(server_seq)+"."+str(server_ack)]=data
			server_ack_dict[str(server_seq)+"."+str(server_ack)]=str(client_seq)+'.'+str(client_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			print "ack sent for the packet with seq no. " +str(client_seq)+" and ack no. "+str(client_ack)
			serverSeqList=server_seq_dict.keys()
			dict_seq=str(server_seq)+"."+str(server_ack)
			print serverSeqList
			#print server_ack_dict	
			i+=1
			raw1 = recv(recsock)
			
			ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
		
			continue
		
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq not in serverSeqList) and payLength==0 and flag!="FINACK" : ##considering only packets with acks with no data
			debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			client_seq=server_ack
			client_ack=1+client_ack
			print "Ack recived with seq no %d and ack no. %d recieved" %(client_seq,client_ack)
			raw1 = recv(recsock)
			ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
			[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
			dict_seq=str(server_seq)+"."+str(server_ack)
			[src_port,dest_port]=layer4.getPorts(tcph)
			flag=layer4.getPacType(tcph)			
			continue
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq in serverSeqList) and payLength<=0 and dup_pac_count<7: ##considering only duplicate packets with acks with no data
			server_seq,server_ack=dict_seq.split('.')
			print "Duplicate ACK packet detected with sequence no. "+str(server_seq)+" and  ack no. " +str(server_ack)
			print "the duplicate packet count is " +str(dup_pac_count)
			raw1 = recv(recsock)

			ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
			dup_pac_count+=1
			[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
			dict_seq=str(server_seq)+"."+str(server_ack)
			[src_port,dest_port]=layer4.getPorts(tcph)
			flag=layer4.getPacType(tcph)
			continue
		elif src_ip == destination_ip and dest_port==source_port and (dict_seq in serverSeqList) and payLength>0 and dup_pac_count<7: ##considering only duplicate packets with acks with data
			server_seq,server_ack=dict_seq.split('.')
			debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			print "Duplicate data packet detected with sequence no. "+str(server_seq)+" and  ack no. " +str(server_ack)
			print "the duplicate packet count is " +str(dup_pac_count)
			kValue=server_ack_dict[dict_seq]
			clis_seq,clis_ack=kValue.split('.')			
			cli_seq=int(clis_seq)
			cli_ack=int(clis_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,cli_seq,cli_ack)
			print "ack sent for the packet with seq no. "+str(cli_seq)+" and  ack no. " +str(cli_ack)
			dup_pac_count+=1
			raw1 = recv(recsock)
			ihl,tcph,src_ip,dest_ip,iph,data,payLength = netUtils.xtractPacket(raw1)
			[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
			dict_seq=str(server_seq)+"."+str(server_ack)
			[src_port,dest_port]=layer4.getPorts(tcph)
			flag=layer4.getPacType(tcph)
			continue

		elif src_ip == destination_ip and dest_port==source_port and (flag=='FINACK' or flag=='FIN'):
			#print "FINACK recieved"			
			debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
			##close connection if fin or finack recieved
			[server_seq,server_ack]=layer4.getServerSeqNo(tcph)
			dict_seq=str(server_seq)+"."+str(server_ack)
			[src_port,dest_port]=layer4.getPorts(tcph)
			flag=layer4.getPacType(tcph)
			client_seq=server_ack
			client_ack=1+client_ack
			#closeConnection(source_ip,destination_ip, source_port,client_seq,client_ack)
			layer5.sendAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			layer5.sendFinAck(source_ip,destination_ip, source_port,client_seq,client_ack)
			break
		else:
			debugPrintSeqNo(client_seq,client_ack,server_seq,server_ack)
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
	return [data1,tcph,iph]

