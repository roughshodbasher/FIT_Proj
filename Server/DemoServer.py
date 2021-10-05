import socket  # Import socket module
import json
import directions
import threading
import AccessDatabase as db

def boot(basePort):
    s = socket.socket()
    s.bind(('0.0.0.0',basePort))
    return s

if __name__ == "__main__":
    mainSock = boot(1024)
    mainSock.listen(5)
    while True:
        client, addr_init = mainSock.accept()
        print("Got connection from",addr_init)
        data = client.recv(1024)
        data = data[data.find(b'{'):]
        data = json.loads(data.decode())
        if data['type'] == 0:
            client.close()
            r = directions.Travelling((data['data']))
            client, addr_init = mainSock.accept()
            client.sendall(((json.dumps({"action": 0, "polyline": r.polyLine[0]})) + '\n').encode("utf-8"))
            client.close()
        elif data['type'] == 1:
            d = db.get_trip(data['data'])
            client.sendall(d)
            client.close()
        