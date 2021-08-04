import socket               # Import socket module
import time
import json

ip = 'localhost'
port = 1025

def sendMessage(info={}):
    data = json.dumps(info)
    s = socket.socket()
    dataSize = 1024
    s.connect((ip, port))
    s.sendall(bytes(data, encoding='utf-8'))
    d = s.recv(dataSize)
    print(d)
    s.close()


def killServer():
    data = {"requestType" : "exit"}
    sendMessage(data)

currentLocation = "Disneyland"
destination = "Universal Studios Hollywood"
vehicle = ("Toyota, Yarris, 2013")

data = {"requestType": "directions","start": currentLocation, "end" : destination, "vehicle" : vehicle}
sendMessage(data)
killServer()

