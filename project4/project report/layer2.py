import binascii
import socket
import struct
import sys



def packARPpacket(dstIP):
	hardware_type = 0x0001  # ethernet
	protocol_type = 0x0800  # ip arp resolution
	header_length = 6  # len(Mac Address)
	protocol_length = 4  # len(IP Address)
	operation_code = 1  # 1 for request, 2 for reply
	src_mac = netUtils('eth0')
	src_ip = get_localhost_ip('eth0')
	dst_mac = '000000000000'
	# dst_ip = infoLocation[3]
	frame = struct.pack('!HHBBH6s4s6s4s',hardware_type,protocol_type,header_length,protocol_length,operation_code,binascii.unhexlify(self.src_mac),
						socket.inet_aton(self.src_ip),binascii.unhexlify(self.dst_mac),socket.inet_aton(self.dst_ip))
	return frame
	
	
def unpackARPpacket(frame):
	arp_list=struct.unpack('!HHBBH6s4s6s4s', arp_frame)
	dest_mac_addr = eth_fields[0]
	src_mac_addr = eth_fields[1]
	return arp_list
	

def findMac(frame):	
	arp_list=unpackARPpacket(frame)
	src_mac_addr = eth_fields[1]
	return dest_mac_addr
	
	
def packEthpacket(dstIP):
	hardware_type = 0x0001  # ethernet
	protocol_type = 0x0800  # ip arp resolution
	header_length = 6  # len(Mac Address)
	protocol_length = 4  # len(IP Address)
	operation_code = 1  # 1 for request, 2 for reply
	src_mac = get_mac_address('eth0')
	src_ip = get_localhost_ip('eth0')
	dst_mac = infoLocation[2]
	dst_ip = infoLocation[3]
	frame = struct.pack('!HHBBH6s4s6s4s',hardware_type,protocol_type,header_length,protocol_length,operation_code,binascii.unhexlify(self.src_mac),
						socket.inet_aton(self.src_ip),binascii.unhexlify(self.dst_mac),socket.inet_aton(self.dst_ip))
	return frame
	return frame

	
