import socket
import select

FOR_READ = list()
FOR_WRITE = list()

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7897

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_sock.bind((SERVER_HOST, SERVER_PORT))
srv_sock.listen(2000)

srv_sock.setblocking(False)
FOR_READ.append(srv_sock)

BUFFER = {}

while True:
    R, W, ERR = select.select(FOR_READ, FOR_WRITE, FOR_READ)
    for r in R:
        if r is srv_sock:
            client, addr = srv_sock.accept()
            client.setblocking(False)
            FOR_READ.append(client)
            print("New client: {}".format(addr))
        else:
            response_temp = "Response for client {} | ".format(r)
            data = r.recv(2048)
            data = data.decode("utf-8")
            respons = response_temp + data
            BUFFER[r.fileno()] = respons
            FOR_WRITE.append(r)
    for w in W:
        data = BUFFER[w.fileno()]
        w.send(data.encode("utf-8"))
        if w in FOR_READ:
            FOR_READ.remove(w)
        if w in FOR_WRITE:
            FOR_WRITE.remove(w)
        w.close()

