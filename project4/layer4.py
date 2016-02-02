import socket
from struct import *

import netUtils

#src_ip=netUtils.get_source_ip()

###### Pack the TCP headers together ######
def packTCPHeader(src_ip,dest_ip, source_port, seq, ack, tcp_proto, data):
	source_ip=src_ip
	tcp_source = source_port  # source port
	tcp_dest = 80    # destination port
	tcp_seq = seq 
	tcp_ack_seq = ack 
	tcp_doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes

	#tcp flags
	tcp_fin = 0 
	tcp_syn = 0 
	tcp_rst = 0
	tcp_psh = 0
	tcp_ack = 0
	tcp_urg = 0

	if tcp_proto=='SYN':
		tcp_syn=1
        elif tcp_proto=='ACK':
		tcp_ack=1
        elif tcp_proto=='SYNACK':
		tcp_syn=1
		tcp_ack=1
        elif tcp_proto=='FIN':
		tcp_fin=1
        elif tcp_proto=='RST':
		tcp_rst=1
        elif tcp_proto=='FINACK':
		tcp_fin=1
		tcp_ack=1
        elif tcp_proto=='PSH':
		tcp_psh=1
        elif tcp_proto=='URG':
		tcp_urg=1
        elif tcp_proto=='PSHACK':
		tcp_psh=1
		tcp_ack=1

	tcp_window = socket.htons (15840)    #   maximum allowed window size
	tcp_check = 0
	tcp_urg_ptr = 0
 
	tcp_offset_res = (tcp_doff << 4) + 0
	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
	
	# the ! in the pack format string means network order
	tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

	tcp_len = len(tcp_header) + len(data)
	
	#psh1 = pseudoHeader(source_ip, dest_ip, tcp_len)+tcp_header+data
	#tcp_check = netUtils.checkSum(psh1)
	tcp_check=getTcpCheckSum(source_ip, dest_ip,tcp_header,data)

	tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H', tcp_urg_ptr)

	return tcp_header

###### Pseudo TCP header for calculating checksum ######
def pseudoHeader(source_ip,dest_ip,tcp_len):
	source_address = socket.inet_aton(source_ip)
	dest_address = socket.inet_aton(dest_ip)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_len);
	return psh


def getTcpCheckSum(source_ip, dest_ip,tcp_header,data):
	tcp_len = len(tcp_header) + len(data)
	psh1 = pseudoHeader(source_ip, dest_ip, tcp_len) + tcp_header + data
	tcp_check = netUtils.checkSum(psh1)
	
	return tcp_check

###### Unpack the TCP Headers ######
def unpackTCPHeader(tcp_header):
	tcph = unpack('!HHLLBBHHH' , tcp_header)
	source_port = tcph[0]
	dest_port = tcph[1]
	sequence = tcph[2]
	acknowledgement = tcph[3]
	doff_reserved = tcph[4]
	tcph_length = doff_reserved >> 4
	return tcph

def getServerSeqNo(tcph):
	server_seq_no=int(tcph[2])
	server_ack_no=int(tcph[3])
	return [server_seq_no,server_ack_no]

def getPorts(tcph):
	source_port=tcph[0]
	dest_port=tcph[1]
	return [source_port,dest_port]
	
def getPacType(tcph):	
	tcp_flag=tcph[5]
	if tcp_flag==0x010:
		flag='ACK'
	elif tcp_flag==0x018:
		flag='PSHACK'
	elif tcp_flag==0x001:
		flag='FIN'
	elif tcp_flag==0x011:
		flag='FINACK'
	else:
		flag='Unknown'
	return flag

