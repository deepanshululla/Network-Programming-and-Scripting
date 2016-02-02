import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.google.com', 443))
sslSocket = socket.ssl(s)
print sslSocket
s.close()
