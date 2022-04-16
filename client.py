import socket

print('For disconnect - type: close me, quit, exit, q')

HOST = '127.0.0.1'
PORT = 7897

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    while True:
        message = input('\nType message >>> ')   #клиент пишет сообщение

        if any(message.lower() in ext for ext in ['close me', 'quit', 'exit', 'q']):   # условие выхода из чата
            break

        message = message.encode('utf-8') # перевод сообщения в байты
        client.send(message)        #отправка сообщения на серврер
        data = client.recv(2048)         #чтение сообщения с сервера
        print(data.decode('utf-8'))    #печать полученного сообщения