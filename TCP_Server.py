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

MESSAGES = {}   #сообщения (ключ - файловый дескриптор сокета клиента)

while True:
    R, W, ERR = select.select(FOR_READ, FOR_WRITE, FOR_READ)
    for r in R:

        if r is srv_sock:    #подключение нового клиента
            client, addr = srv_sock.accept()
            client.setblocking(False)
            FOR_READ.append(client)
            print("Client {} connected".format(addr))

        else:
            response_temp = "Сlient {}".format(r)
            data = r.recv(2048)
            if data:
                data = data.decode("utf-8")
                respons = response_temp + data
                MESSAGES[r.fileno()] = respons
                FOR_WRITE.append(r)
            else:
                print('Client disconnected ...')

                if r in FOR_WRITE:
                    FOR_WRITE.remove(r)

                FOR_READ.remove(r)
                r.close()
                del MESSAGES[r.fileno()]

    for w in W:
        data = MESSAGES[w.fileno()]
        w.send(data.encode("utf-8"))

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

