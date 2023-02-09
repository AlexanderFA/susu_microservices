import socket

sock = socket.socket()
sock.connect(('localhost', 9090))

user_name = input("Enter your name: ")
sock.send(user_name.encode())

while True:
    msg = input("Type a message (type '\\exit' to exit): ")
    if msg == "\\exit":
        break
    sock.send(msg.encode())
    print("Server response: {}".format(sock.recv(1024).decode("utf-8")))

sock.close()
