import socket
import os

sock = socket.socket()
sock.connect(('localhost', 9090))

SID = os.getenv('SID') or '-'  # эмуляция сессионного токена (берем из переменной окружения)
sock.send(SID.encode())  # отправляем сессионный токен, чтобы сервер нас узнал

# user_name = input("Enter your name: ")
# sock.send(user_name.encode())
# print("Server response: {}".format(sock.recv(1024).decode("utf-8")))

server_msg = sock.recv(1024).decode("utf-8")
if server_msg == 'Enter your name: ':
    user_name = input(server_msg)
    sock.send(bytes(user_name, "utf-8"))
    print(sock.recv(1024).decode("utf-8"))
else:
    print(server_msg)  # welcome back

while True:
    msg = input()
    sock.send(bytes(msg, "utf-8"))  # отправляем сообщение даже если это \exit
    print("Server response: {}".format(sock.recv(1024).decode("utf-8")))
    if msg == "\\exit":
        break

sock.close()
