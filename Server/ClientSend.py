import socket               # Import socket module
import time
import json

ip = '194.193.148.240'
# ip = 'localhost'
port = 1024

def sendMessage(info={},raw=False):
    print("Started")
    if raw:
        s = socket.socket()
        dataSize = 1024
        s.connect((ip, port))
        s.sendall(b'\x00\x9c{"requestType":"directions","data":{"start":"lat\\/lng: (-37.810108,144.9582684)","destinations":"[lat\\/lng: (-37.8174907,144.9545615)]","vehicle":"ABC123"}}')
        print(s.recv(1024))
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
data = "test"
sendMessage(data,True)
m = b'\x00\x9c{"requestType":"directions","data":{"start":"lat\\/lng: (-37.810108,144.9582684)","destinations":"[lat\\/lng: (-37.8174907,144.9545615)]","vehicle":"ABC123"}}'
# killServer()

