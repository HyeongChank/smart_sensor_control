import socket
 
host = ''
port = 9999
 
server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(1)
 
while True:
    print("connecting....")
    client_sock, addr = server_sock.accept()
 
    print('Connected by', addr)
    data = client_sock.recv(1024)
    data = data.decode()
    print(data)
 
    while True:
        data = client_sock.recv(4)
        length = int.from_bytes(data, "little")
        msg = client_sock.recv(length)
        if len(data) <= 0:
            break
        msg = msg.decode()
        print(msg)
 
        msg = "eco: " + msg
        data = msg.encode()
 
        length = len(data)
        client_sock.sendall(length.to_bytes(4, byteorder="little"))
        client_sock.sendall(data)
 
    client_sock.close()
 
server_sock.close()