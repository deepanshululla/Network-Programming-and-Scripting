import os

TCP_Variant2 = ['Reno_Reno', 'NewReno_Reno', 'Vegas_Vegas', 'NewReno_Vegas', 'Cubic_Reno' , 'Cubic_NewReno','Cubic_Vegas']
k=os.getcwd()
os.system("rm *.txt")

for proto in TCP_Variant2:
	throughPutFile=proto+"ThroughPut.txt"
	latencyFile=proto+"Latency.txt"
	droppedPacketsFile=proto+"DroppedPackets.txt"
	tcps = proto.split('_')
	f1 = open(throughPutFile, 'w')
	f2 = open(latencyFile, 'w')
	f3= open(droppedPacketsFile, 'w')

	f1.write("CBR rate"+"\t"+"throughPut "+tcps[0]+"\t throughPut "+tcps[1]+'\n')
	f2.write("CBR rate"+"\t"+"latency for "+tcps[0]+"\t latency for "+tcps[1]+'\n')
	f3.write("CBR rate"+"\t"+"dropped packets"+tcps[0]+"\t dropped packets "+tcps[1]+'\n')

	f1.close()
	f2.close()
	f3.close()

for var in TCP_Variant2:
    for rate in range(1, 11):
        tcps = var.split('_')
        os.system("ns exp2.tcl " + tcps[0] + " " + tcps[1] + " " + str(rate))
	os.system("python traceCheckExp2.py " + var + "_output-" + str(rate)+'.tr')
		

os.system("rm *.tr")
os.system("rm *.nam")
