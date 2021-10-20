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
    port = 1024
    mainSock = boot(port)
    mainSock.listen(5)
    while True:
        client, addr_init = mainSock.accept()
        print("Got connection from", addr_init)
        data = client.recv(1024)
        data = data[data.find(b'{'):]
        data = json.loads(data.decode())
        if data['type'] == 0:
            r = directions.Travelling((data['data']))
            print(r.polyLine[0])
            test = []
            for c in r.polyLine[0]:
                test.append(str(ord(c)))
            test = "-".join(test)
            client.sendall(bytes(json.dumps({"action": 0, "polyline": test}) + '\n', encoding='utf-8'))
            client.close()
            # go to update loop
            client, addr_init = mainSock.accept()
            data = client.recv(1024)
            data = data[data.find(b'{'):]
            data = json.loads(data.decode())
            cPos = [data["lat"],data["long"]]
            while not r.atEnd(cPos):
                if r.onRoute(cPos):
                    response = json.dumps({"action" : 0})
                    client.sendall(bytes(response + '\n',encoding = 'utf-8'))
                else:
                    response = json.dumps({"action": 1})
                    test = []
                    for c in r.polyLine[0]:
                        test.append(str(ord(c)))
                    test = "-".join(test)
                    client.sendall(bytes(json.dumps({"action": 0, "polyline": test}) + '\n', encoding='utf-8'))
                data = client.recv(1024)
                data = data[data.find(b'{'):]
                data = json.loads(data.decode())
                cPos = [data["lat"], data["long"]]
            client.close()

        elif data['type'] == 1:
            d = db.get_trip(data['data'])
            client.sendall(bytes(d, encoding='utf-8'))
            client.close()
        elif data['type'] == 2:
            rego = data['data']['rego']
            d = db.get_vehicle_info(rego)
            client.sendall(bytes(d, encoding='utf-8'))
            client.close()
        elif data['type'] == 3:
            print(data['data'])
            d = db.add_vehicle(data['data'])
            client.sendall(bytes(d, encoding='utf-8'))
            client.close()
