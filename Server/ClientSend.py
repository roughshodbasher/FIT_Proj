import socket               # Import socket module
import time
import json

ip = 'localhost'
port = 1024

def sendMessage(info={},raw=False):
    if raw:
        s = socket.socket()
        dataSize = 1024
        s.connect((ip, port))
        s.sendall(bytes(info, encoding='utf-8'))
        return
    data = json.dumps(info)
    s = socket.socket()
    dataSize = 1024
    s.connect((ip, port))
    # s.sendall(bytes(data, encoding='utf-8'))
    d = s.recv(dataSize)
    print(d)
    # s.close()
    d = json.loads(d)
    print(d["port"])
    s = socket.socket()
    s.connect((ip,d["port"]))
    s.sendall(bytes(data, encoding='utf-8'))
    # s.close()
    print("done")
    testRoute = [[33.8161014800008, -117.9225146125875], [33.82157343203593, -117.92277292780344],
                 [33.8353080852262, -117.92214664830355], [33.8821008, -118.0249616], [33.8155166, -117.9238358],
                 [33.8215783, -117.9226437],[33.81052620294962, -117.9312339328883]]
    for pos in testRoute:
        sendData = json.dumps({"position": pos})
        s.sendall(bytes(sendData))
        d = s.recv(1024)
        print(d)


    return

def killServer():
    data = "exit"
    sendMessage(data,True)

currentLocation = "Disneyland"
destination = "Universal Studios Hollywood"
vehicle = ("Toyota, Yarris, 2013")

data = {"type": 0,"start": currentLocation, "destinations" : destination, "vehicle" : vehicle}
sendMessage(data)
# killServer()

