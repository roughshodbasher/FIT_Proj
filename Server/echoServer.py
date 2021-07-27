import socket
if __name__ == '__main__':
    dataSize = 1024
    port = 1025
    s = socket.socket()
    s.bind(('0.0.0.0', port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.
    while True:
        c, addr = s.accept()  # Establish connection with client.
        data = c.recv(dataSize)
        c.sendall(data)
        f = open("log.txt",'a')
        f.write(data+"\n")
        f.close()
        if data.decode() == "exit":
            break
    print("exiting")