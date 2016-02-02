from __future__ import print_function
import sys

import traceLib

traceFile=open(sys.argv[1],'r')
traceData=traceFile.read()

traceLines=traceData.split("\n")


throughPut=traceLib.tcpCalcThroughput(traceLines,0,10,2,3,1.0,4.0)
#calculate data flowing between link 2 and 3 starting from node 1 ending at at node 4
print(sys.argv[1])
print("TCP Throughput=data flowing/sec  in Mb/sec is",throughPut)

latency=traceLib.calcAvgLatency(traceLines,2,3,1.0,4.0)
#calculate average delay between link 1 and 2 starting from node 1 ending at at node 4
pacCount=traceLib.tcpPacketCount(traceLines,1.0,4.0)

print("The average propagation delay  in miliseconds is",latency)

dropAll=pacCount['DropAll']
print("the total number of TCp and ack dropped packets are ",dropAll)
print("")
l1=sys.argv[1].split('.')
proto,rate=l1[0].split("_output-")

throughPutFile=proto+"ThroughPut.txt"
latencyFile=proto+"Latency.txt"
droppedPacketsFile=proto+"DroppedPackets.txt"
f1 = open(throughPutFile, 'a')
f2 = open(latencyFile, 'a')
f3= open(droppedPacketsFile, 'a')

f1.write(str(rate)+"\t"+str(throughPut)+'\n')
f2.write(str(rate)+"\t"+str(latency)+'\n')
f3.write(str(rate)+"\t"+str(dropAll)+'\n')

f1.close()
f2.close()
f3.close()
