from __future__ import print_function
import sys
import traceLib

traceFile=open(sys.argv[1],'r')
traceData=traceFile.read()

traceLines=traceData.split("\n")


thru1=traceLib.tcpCalcThroughput(traceLines,0,10,2,3,1.0,4.0)
#calculate data flowing between link 2 and 3 starting from node 1 ending at at node 4 from time 0 to time=5 seconds
thru2=traceLib.tcpCalcThroughput(traceLines,0,10,2,3,5.0,6.0)
#calculate data flowing between link 2 and 3 starting from node 5 ending at at node 6 from time 0 to time=5 seconds

delay1=traceLib.calcAvgLatency(traceLines,2,3,1.0,4.0)
#calculate average delay between link 1 and 2 starting from node 1 ending at at node 4
delay2=traceLib.calcAvgLatency(traceLines,2,3,5.0,6.0)
#calculate average delay between link 1 and 2 starting from node 5 ending at at node 6

drop1=traceLib.tcpPacketCount(traceLines,1.0,4.0)
drop2=traceLib.tcpPacketCount(traceLines,5.0,6.0)

#calculate dropped packets
dropTCPall1=drop1['TCPdropped']+drop1['ACKdropped']
dropTCPall2=drop2['TCPdropped']+drop2['ACKdropped']


print(sys.argv[1])
print("TCP Throughput=data flowing/sec is",thru1)
print("The average delay(RTT) is",delay1)
print("the number of TCP dropped packets are ",drop1['TCPdropped'])
print("the number of ACK dropped packets are ",drop1['ACKdropped'])
print("the total number of TCp and ack dropped packets are ",dropTCPall1)
print("")

print(sys.argv[1])
print("TCP Throughput=data flowing/sec is",thru2)
print("The average delay(RTT) is",delay2)
print("the number of TCP dropped packets are ",drop2['TCPdropped'])
print("the number of ACK dropped packets are ",drop2['ACKdropped'])
print("the total number of TCp and ack dropped packets are ",dropTCPall2)
print("")
print("-------------------------------------------------------------")
l1=sys.argv[1].split('.')
proto,rate=l1[0].split("_output-")

throughPutFile=proto+"ThroughPut.txt"
latencyFile=proto+"Latency.txt"
droppedPacketsFile=proto+"DroppedPackets.txt"
f1 = open(throughPutFile, 'a')
f2 = open(latencyFile, 'a')
f3= open(droppedPacketsFile, 'a')

f1.write(str(rate)+"\t"+str(thru1)+'\t'+str(thru2)+'\n')
f2.write(str(rate)+"\t"+str(delay1)+"\t"+str(delay2)+'\n')
f3.write(str(rate)+"\t"+str(dropTCPall1)+'\t'+str(dropTCPall2)+'\n')

f1.close()
f2.close()
f3.close()


