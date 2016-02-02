#!/usr/bin/python
import socket
from struct import *
import netUtils




##### Pack the IP headers together #####
def packHeader(src_ip,destn_ip):
	source_ip=src_ip
	dest_ip = destn_ip # or socket.gethostbyname('www.google.com')
 
	# ip header fields
	ip_ihl = 5 #header length
	ip_ver = 4
	ip_tos = 0
	ip_tot_len = 0  # kernel will fill the correct total length
	ip_id = 54321   #Id of this packet
	ip_frag_off = 0
	ip_ttl = 255
	ip_proto = socket.IPPROTO_TCP
	ip_check = 0    # kernel will fill the correct checksum
	
	ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
	ip_daddr = socket.inet_aton ( dest_ip )
 
	ip_ihl_ver = (ip_ver << 4) + ip_ihl
 
	# the ! in the pack format string means network order
	ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
	return ip_header
	

###### Unpack the IP header that is received ######
def unpackHeader(ip_header):
	iph = unpack('!BBHHHBBH4s4s' , ip_header)
	version_ihl = iph[0]
	version = version_ihl >> 4
	ip_ihl = version_ihl & 0xF  
	#header length
	ip_ttl = iph[5]
	ip_proto = iph[6]
	source_ip = socket.inet_ntoa(iph[8]);
	dest_ip = socket.inet_ntoa(iph[9]);
	return (ip_ihl,source_ip,dest_ip,iph)
