

def packetCount(traceLines):
	pacCountDict={}
	pacEnq,pacDeq,pacRecv,pacDrop,pacCong,udpPac,tcpPac,ackPac=0,0,0,0,0,0,0,0
	#344 r 1.010032 1 2 tcp 40 ------- 1 1.0 4.0 0 113
	
	for x in range(0,len(traceLines)):
		
		line=traceLines[x].split(" ")
		
			
		if line[0]=='+' and line[4]=='tcp':
			pacEnq+=1
			tcpPac+=1
			
		elif line[0]=='+' and line[4]=='cbr':
			pacEnq+=1
			udpPac+=1
		elif line[0]=='+' and line[4]=='ack':
			pacDeq+=1
			ackPac+=1	
		elif line[0]=='-' and line[4]=='tcp':
			pacDeq+=1
			tcpPac+=1
		elif line[0]=='-' and line[4]=='cbr':
			pacDeq+=1
			udpPac+=1
		elif line[0]=='-' and line[4]=='ack':
			pacDeq+=1
			ackPac+=1
		elif line[0]=='r' and line[4]=='tcp':
			pacRecv+=1
			tcpPac+=1
		elif line[0]=='r' and line[4]=='cbr':
			pacRecv+=1
			udpPac+=1
		elif line[0]=='r' and line[4]=='ack':
			pacRecv+=1
			ackPac+=1
		elif line[0]=='c' and line[4]=='tcp':
			pacCong+=1
			tcpPac+=1
		elif line[0]=='c' and line[4]=='cbr':
			pacCong+=1
			udpPac+=1
		elif line[0]=='c' and line[4]=='ack':
			pacCong+=1
			ackPac+=1
		elif line[0]=='d' and line[4]=='tcp':
			pacDrop+=1
			tcpPac+=1
		elif line[0]=='d' and line[4]=='cbr':
			pacDrop+=1
			udpPac+=1
		elif line[0]=='d' and line[4]=='ack':
			pacDrop+=1
			ackPac+=1
		# pacType=line[4]
		# print(pacType)
		
		
	pacCountDict['inQue']=pacEnq
	pacCountDict['deQue']=pacDeq
	pacCountDict['recieved']=pacRecv
	pacCountDict['dropped']=pacDrop
	pacCountDict['congested']=pacCong
	pacCountDict['total']=len(traceLines)
	pacCountDict['tcp']=tcpPac
	pacCountDict['cbr']=udpPac
	pacCountDict['ack']=ackPac
	
	#print(pacCountDict)
	return pacCountDict

def tcpPacketCount(traceLines,nodeStart,nodeEnd):
	pacCountDict={}
	tcpPacEnq,tcpPacDeq,tcpPacRecv,ackPacRecv,tcpPacDrop,ackPacDrop=0,0,0,0,0,0
	tcpPacCong,ackPacCong,ackPacEnq,ackPacDeq,tcpPac,ackPac=0,0,0,0,0,0
	#344 r 1.010032 1 2 tcp 40 ------- 1 1.0 4.0 0 113
	node1=str(float(nodeStart))
	node2=str(float(nodeEnd))
	for x in range(0,len(traceLines)):
		
		line=traceLines[x].split(" ")
		
			
		if line[0]=='+' and line[4]=='tcp' and line[8]==node1 and line[9]==node2:
			tcpPacEnq+=1
			tcpPac+=1
			
		elif line[0]=='+' and line[4]=='ack' and line[8]==node2 and line[9]==node1:

			ackPacDeq+=1
			ackPac+=1	
		elif line[0]=='-' and line[4]=='tcp' and line[8]==node1 and line[9]==node2:
			tcpPacDeq+=1
			tcpPac+=1
		
		elif line[0]=='-' and line[4]=='ack' and line[8]==node2 and line[9]==node1:
			ackPacDeq+=1
			ackPac+=1
		elif line[0]=='r' and line[4]=='tcp' and line[8]==node1 and line[9]==node2:
			tcpPacRecv+=1
			tcpPac+=1
		elif line[0]=='r' and line[4]=='ack' and line[8]==node2 and line[9]==node1:

			ackPacRecv+=1
			ackPac+=1
		elif line[0]=='c' and line[4]=='tcp' and line[8]==node1 and line[9]==node2:
			tcpPacCong+=1
			tcpPac+=1
		
		elif line[0]=='c' and line[4]=='ack' and line[8]==node2 and line[9]==node1:
			ackPacCong+=1
			ackPac+=1
		elif line[0]=='d' and line[4]=='tcp' and line[8]==node1 and line[9]==node2:
			tcpPacDrop+=1
			tcpPac+=1
		
		elif line[0]=='d' and line[4]=='ack' and line[8]==node2 and line[9]==node1:
			ackPacDrop+=1
			ackPac+=1
		# pacType=line[4]
		# print(pacType)
		
		
	pacCountDict['tcpinQue']=tcpPacEnq
	pacCountDict['ackinQue']=ackPacEnq
	pacCountDict['tcpdeQue']=tcpPacDeq
	pacCountDict['ackdeQue']=ackPacDeq
	pacCountDict['TCPrecieved']=tcpPacRecv
	pacCountDict['ACKrecieved']=ackPacRecv

	pacCountDict['TCPdropped']=tcpPacDrop
	pacCountDict['ACKdropped']=ackPacDrop
	pacCountDict['TCPcongested']=tcpPacCong
	pacCountDict['ACKcongested']=ackPacCong
	
	pacCountDict['tcp']=tcpPac
	
	pacCountDict['ack']=ackPac
	
	#print(pacCountDict)
	return pacCountDict

def tcpCalcThroughput(traceLines,timeStart,timeFinal,node1,node2,nodeStart,nodeEnd):
	startNode=str(float(nodeStart))
	endNode=str(float(nodeEnd))
	
	throughSum=0
	for x in range(0,len(traceLines)):
		
		line=traceLines[x].split(" ")
		#r 1.144448 2 3 tcp 1040 ------- 1 1.0 4.0 3 134
		if line[0]=='r' and line[4]=='tcp' and float(line[1])>float(timeStart) and float(line[1])<float(timeFinal) and line[8]==str(startNode) and line[9]==str(endNode) and line[2]==str(node1) and line[3]==str(node2) :
			throughSum=throughSum+int(line[5])*8
		elif line[0]=='r' and line[4]=='ack' and float(line[1])>float(timeStart) and float(line[1])<float(timeFinal) and line[9]==str(startNode) and line[8]==str(endNode) and line[3]==str(node1) and line[2]==str(node2) :
			throughSum=throughSum+int(line[5])*8
	throughPut=float(throughSum)/(timeFinal-timeStart)/ (1024 * 1024)
		
	return throughPut
	
def calcDropRate(traceLines,nodeStart,nodeEnd):
	pacDict=tcpPacketCount(traceLines,nodeStart,nodeEnd)
	pacSent=pacDict['tcpinQue']+pacDict['ackinQue']
	pacRecvd=pacDict['TCPrecieved']+pacDict['ACKrecieved']
	if pacSent == 0:
        	return 0
    	else:
        	return float(pacSent - pacRecvd) / float(pacSent)
	
	


def calcAvgLatency(traceLines,node1,node2,nodeStart,nodeEnd):
	
	
	startNode=str(float(nodeStart))
	endNode=str(float(nodeEnd))
	

	
	duration=0
	start_time = {}
    	end_time = {}
    	total_duration = 0.0
    	total_packet = 0
		
	for x in range(0,len(traceLines)):
		line=traceLines[x].split(" ")
		if line[0]=='+' and line[2]==str(node1) and line[3]==str(node2) and line[8]==startNode and line[9]==endNode:
			
			
			start_time.update({line[11]: float(line[1])})
			
			
		elif line[0]=='r' and line[2]==str(node1) and line[3]==str(node2) and line[8]==startNode and line[9]==endNode:
			
			chkflag=line[11]
			end_time.update({line[11]: float(line[1])})

	
	
	
	for i in start_time:
		if i in end_time:
        		start = start_time[i]
        		end = end_time[i]
			
        		duration = float(end) - float(start)
        		if duration > 0:
				total_duration += duration
				total_packet += 1
	if total_packet == 0:
		return 0
	else:
    		return float(total_duration) / total_packet*1000
			
	

