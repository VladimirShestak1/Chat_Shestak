import socket
import select


FOR_READ = list() #сокеты, откуда приходят сообщения
FOR_WRITE = list() #сокеты, куда будем отправлять сообщения

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7897

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_sock.bind((SERVER_HOST, SERVER_PORT))
srv_sock.listen(10)

srv_sock.setblocking(False)
FOR_READ.append(srv_sock)

MESSAGES = {}   #сообщения (ключ - сокет клиента)

while True:
    R, W, ERR = select.select(FOR_READ, FOR_WRITE, FOR_READ)
    for r in R:

        if r is srv_sock:    #подключение нового клиента
            client, addr = srv_sock.accept()
            client.setblocking(False)
            FOR_READ.append(client)
            print("Client {} connected".format(addr))

            for clnt in FOR_WRITE:
                mess = "Client {} connected".format(addr)
                clnt.send(mess.encode("utf-8"))

        else:
            data = r.recv(2048)
            if data:
                data = data.decode("utf-8")

                if MESSAGES.get(r, None):
                    MESSAGES[r].append(data)
                    for clnt in FOR_WRITE:
                        clnt.send(data.encode("utf-8"))

                else:
                    MESSAGES[r] = [data]

                if r not in FOR_WRITE:
                    FOR_WRITE.append(r)

            else:
                print('Client disconnected ...')

                if r in FOR_WRITE:
                    FOR_WRITE.remove(r)

                FOR_READ.remove(r)
                r.close()
                del MESSAGES[r]

    for r in W:
        message = MESSAGES.get(r, None)

        if len(message):
            temp_resp = message.pop(0).encode('utf-8')

            for r in R:
                r.send(temp_resp)
        else:
            FOR_WRITE.remove(r)

    for r in ERR:      # ошибка
        print('Ошибка, клиент отключился...')
        FOR_READ.remove(r)

        if r in FOR_WRITE:
            FOR_WRITE.remove(r)

        r.close()

        del MESSAGES[r]





    # for w in W:
    #     data = BUFFER[w.fileno()]
    #     w.send(data.encode("utf-8"))
    #     if w in FOR_READ:
    #         FOR_READ.remove(w)
    #     if w in FOR_WRITE:
    #         FOR_WRITE.remove(w)
    #     w.close()

