import os

TCP_Variant3 = ['Reno', 'SACK','Cubic']
QUEUE_Variant = ['DropTail', 'RED']

os.system("rm *.txt")

for proto in TCP_Variant3:
	for q in QUEUE_Variant:
		throughPutFile=proto+q+"ThroughPut.txt"
		latencyFile=proto+q+"Latency.txt"
		droppedPacketsFile=proto+q+"DroppedPackets.txt"

		f1 = open(throughPutFile, 'w')
		f2 = open(latencyFile, 'w')
		f3= open(droppedPacketsFile, 'w')

		f1.write("time"+"\t"+"throughPut"+'\n')
		f2.write("time"+"\t"+"latency"+'\n')
		f3.write("time"+"\t"+"dropped packets"+'\n')

		f1.close()
		f2.close()
		f3.close()

for var in TCP_Variant3:
	
    for q in QUEUE_Variant:
        os.system("ns exp3.tcl " + var + " " + q)
	os.system("python traceCheckExp3.py " + var + "-" +q+"_output"+'.tr')
		

f4=open("Drop_rate.txt", 'w')

f4.write("protocol"+"\t"+"Queue"+"\t"+"DropRate"+"\n")

f4.close()

os.system("rm *.tr")
os.system("rm *.nam")
