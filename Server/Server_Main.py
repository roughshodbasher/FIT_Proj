import socket  # Import socket module
import json

key = ''
if not key:
    with open("key.api") as f:
        key = f.readline().rstrip()
print(key)
dataSize = 1024
port = 1024
s = socket.socket()  # Create a socket object
s.bind(('0.0.0.0', port))  # Bind to the port




s.listen(5)  # Now wait for client connection.
while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    data = c.recv(dataSize)
    c.send(b"abc")
    print(data.decode())
    c.close()  # Close the connection
    if data.decode() == 'exit':
        break


print("Testing")