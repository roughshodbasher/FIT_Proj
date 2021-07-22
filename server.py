import socket               # Import socket module

s = socket.socket()         # Create a socket object
s.bind(('0.0.0.0', 1025))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   data = c.recv(1025)
   print(data)
   c.close()                # Close the connection
   if data.decode() == 'exit':
      break
   
