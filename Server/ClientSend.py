import socket               # Import socket module
import time
import json
s = socket.socket()
d = json.dumps(['test',{"test" : "exit"},123,False])
#d = 'exit'
ip = 'localhost'
port = 1024
s.connect((ip,port))
s.sendall(bytes(d,encoding='utf-8'))

s.close()
