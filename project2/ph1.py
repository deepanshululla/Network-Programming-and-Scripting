
#purpose of phase1 was to create a web crawler using normal requests,getting web page 
#and extracting header information
from __future__ import print_function
import socket


server="www.ietf.org"
port=80
clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((server,port))


CRLF = "\r\n"

request = [
    "GET / HTTP/1.1",
    "Host: www.ietf.org",
    "Connection: Close",
    "",
    "",
]
clientSocket.send(CRLF.join(request))
# clientSocket.send("GET / HTTP/1.1 \r\n")

response = ''
buffer = clientSocket.recv(4096)

# print('buffer scanning')


# print(buffer)
while buffer:
	response += buffer
	buffer = clientSocket.recv(4096)
	# print(buffer)

# HTTP headers will be separated from the body by an empty line
header_data, _, body = response.partition(CRLF + CRLF)
k=header_data.split(CRLF)
print(k)


# print(response)
