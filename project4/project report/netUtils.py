import os
import struct
from struct import *
from random import randint
import layer3
import layer4

def net_param():
	out1=os.popen('ifconfig eth0')
	out_list=out1.read().split('\n')
	return out_list

def get_source_mac():
	out_list=net_param()
	mac_line=out_list[0]
	source_mac=mac_line.split("HWaddr ")[1][0:17]
	return source_mac
		
def get_source_ip():
	out_list=net_param()
	
	ip_line=out_list[1]
	
	source_ip=ip_line.split("Bcast")[0].split("inet addr:")[1][0:13]
	return source_ip
	
def get_gateway_ip():
	out1=os.popen('route -n')
	out_list=out1.read().split('\n')
	data = commands.getoutput('route -n').split('\n')
	for line in data:
		record=line.split()
		dest_ip=record[0]
		if dest_ip=='0.0.0.0':
			gateway_ip = record[1]
			return gateway_ip
			break

			

def checkSum(msg):
	#print len(msg)
	#msg=layer4.pseudoHeader(source_ip, dest_ip, tcp_len)+tcp_header+data
	msg2 = 0
	if len(msg) % 2 == 1:  # the length of msg in bytes is an odd number
		msg += struct.pack('B', 0)
		msg2 = 0
        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
                w = ord(msg[i]) + (ord(msg[i + 1]) << 8)
                msg2 += w
        msg2 = (msg2 >> 16) + (msg2 & 0xffff)
        msg2 += msg2 >> 16
        # complement and mask to 4 byte short
        msg2 = ~msg2 & 0xffff
        return msg2
	
def serverNameExtract(url):
	try:
		q1=url.split("//")[1]
		url=q1		
		q=url.find('/')
		if q!=-1:
			server=url[0:q]
		
			path=url[q:len(url)]
			if path[len(path)-1]!='/':
				path=path
		if q==-1:
			server=url
			path='/'
	except:
		sys.exit('Please try in the format python rawhttpget.py http://www.ccs.neu.edu')
	return [server,path]

	
def seperatePacket(packet):
	packet = packet[0]
	ip_header = packet[0:20]
	ihl,source_ip,dest_ip,iph = layer3.unpackHeader(ip_header)

	iph_length = ihl * 4
	
	t = iph_length
	tcp_header = packet[t:t+20]
	tcph = layer4.unpackTCPHeader(tcp_header)
	doff_reserved = tcph[4]
	tcph_length = doff_reserved >> 4
	h_size = iph_length + tcph_length * 4
	data_size = len(packet) - h_size
	data = packet[h_size:]
	
	return [ip_header,tcp_header,data]

def xtractPacket(packet):
	
	packet = packet[0]
	ip_header = packet[0:20]
	ihl,source_ip,dest_ip,iph = layer3.unpackHeader(ip_header)

	iph_length = ihl * 4
	
	t = iph_length
	tcp_header = packet[t:t+20]
	
	tcph = layer4.unpackTCPHeader(tcp_header)
	doff_reserved = tcph[4]
	tcph_length = doff_reserved >> 4
	#print len(packet)	
	#print tcph_length
	#print iph_length
	h_size = iph_length + tcph_length * 4
	#print h_size
	
	data_size = len(packet) - h_size
	#print data_size
	data = packet[h_size:]
	#payloadLength=data_size+tcph_length * 4
	#payloadLength=payloadLength-20
	payloadLength=len(data)
	#print "the length of payload is " +str(payloadLength)
	return [ihl,tcph,source_ip,dest_ip,iph,data,payloadLength]

def get_filename(url):
	[server,path]=serverNameExtract(url)
	k=len(path)
	print path		
	if path[k-1]=='/':
		name = 'index.html'
	else:
		path_array = url.split('/')
		print path_array
		m=len(path_array)-1

		name=path_array[m]               
	return name
	
def getFreePort():
	x= randint(35000,42949)
	for portNo in range(x,65000):
		comand='netstat -a | grep '+ str(portNo)
		if os.popen(comand).read()=='':
			
			return portNo
			break
		else:
			print 'busy port'
			
			
