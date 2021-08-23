import socket  # Import socket module
import json
import directions
import threading
#import AccessDatabase as db


class threadRoute(threading.Thread):
    def __init__(self,threadId,port):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.port = port
        self.sock = None

    def run(self):
        #call funtion
        clientThread(self.port)
        return

def clientThread(port):
    s = socket.socket()
    s.bind(('0.0.0.0',port))
    s.listen(5)
    while True:
        client, addr = s.accept()
        d = client.recv(1024)
        d = d.decode(encoding='utf-8')
        d = json.loads(d)
        if d["type"] == 0:
            directions_thread(s,d["data"])
        elif d["type"] == 1:
            #do database stuff
            #toSend = bytes(db.handle_db_request(d["data"]), encoding='utf-8')
            #client.sendall(toSend)
            pass
        return

def directions_thread(s,data):
    #calculate route
    r = directions.Travelling(data)
    atDestination = False
    while not atDestination:
        data = s.recv(1024)
        data = data.decode()
        position = data["position"]
        if r.atEnd(position):
            atDestination = True
        else:
            if not r.onRoute(position):
                print("Route being re-calculated")
                d = json.loads({"polyline" : r.path.polyline})
            else:
                print("On Route")
                d = json.loads({})
            s.sendall(bytes(d,encoding='utf-8'))


def boot(basePort):
    s = socket.socket()
    s.bind(('0.0.0.0',basePort))
    return s

def clientPortSwitch(client,addr_init,openPorts):
    dataSize = 256
    clientsFull = True
    for i,open in enumerate(openPorts):
        if open:
            openPorts[i][0] = False
            clientsFull = False
            dataSend = bytes(json.dumps({"port" :openPorts[i][1]}),encoding='utf-8')
            newClient = socket.socket()
            newClient.bind(("0.0.0.0",openPorts[i][1]))
            client.sendall(dataSend)
            # +
            newClient.listen(5)
            while True:
                client, addr = newClient.accept()
                d = client.recv(dataSize)
                print(d)
                # client.close()
                print("???")
                break
            break
    return True


if __name__ == "__main__":
    threads = []
    mainSock = boot(1024)
    clientSize = 100
    openPorts = [[True,1025 + i] for i in range(clientSize)]
    mainSock.listen(5)  # Now wait for client connection.
    while True:
        client, addr_init = mainSock.accept()  # Establish connection with client.
        print('Got connection from', addr_init)
        """
        fix changing port
        check that threading function actually works
        
        """
        threads.append(threadRoute(0,))
        # data = c.recv(dataSize)
        # data = json.loads(data)
        # if data['requestType'] == "exit":
        #     break
        # elif data['requestType'] == "directions":
        #     #thread
        #     toSend = bytes(json.dumps(directions.getDirectionsDemo()),encoding='utf-8')
        #     c.sendall(toSend)
        # elif data['requestType'] == 'information':
        #     #get things from the db
        #     continue
        # c.close()  # Close the connection
        break
