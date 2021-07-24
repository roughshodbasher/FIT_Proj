import socket  # Import socket module
import json
import directions



if __name__ == "__main__":
    key = ''
    if not key:
        with open("key.api") as f:
            key = f.readline().rstrip()
    dataSize = 1024
    port = 1024
    s = socket.socket()  # Create a socket object
    s.bind(('0.0.0.0', port))  # Bind to the port




    s.listen(5)  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        data = c.recv(dataSize)
        data = json.loads(data)
        if data['requestType'] == "exit":
            break
        elif data['requestType'] == "directions":
            toSend = bytes(json.dumps(directions.getDirectionsDemo()),encoding='utf-8')
            c.sendall(toSend)
        c.close()  # Close the connection
