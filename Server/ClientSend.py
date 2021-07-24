import socket               # Import socket module
import time
import json

def sendMessage(info=[]):
    data = json.dumps(info)
    s = socket.socket()
    ip = 'localhost'
    port = 1024
    dataSize = 1024
    s.connect((ip, port))
    s.sendall(bytes(data, encoding='utf-8'))
    d = s.recv(dataSize)
    s.close()



currentLocation = "32-38 Exhibition Walk, Clayton VIC 3800"
destination = "20 Research Way, Clayton VIC 3800"
vehicle = ("Toyota, Yarris, 2013")

sendMessage([currentLocation,destination,vehicle])
sendMessage('exit')
