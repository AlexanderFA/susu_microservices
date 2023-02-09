import socket
import threading
from datetime import datetime

clients = {}

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(2)
print('waiting for connection...')


def handle_client(conn, addr):
    # conn.send(bytes(f"Welcome back {clients[client_socket]}!", "utf-8"))
    SID = conn.recv(1024).decode("utf-8")
    print(f"User with sid {SID} entered")
    if SID in clients:
        print(clients[SID])
        user_name = clients[SID]['name']
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.send(bytes(f"Welcome back {user_name}! Time now is: {now_time}", "utf-8"))
    else:
        conn.send(bytes("Enter your name: ", "utf-8"))
        user_name = conn.recv(1024).decode("utf-8")
        clients[SID] = {'name': user_name}
        conn.send(bytes(f"Hello {user_name}! Start to send messages!", "utf-8"))

    while True:
        client_msg = conn.recv(1024).decode("utf-8")
        if client_msg == "\\exit":
            conn.close()
            break
        client_msg = bytes("User {} wrote: {}".format(user_name, client_msg), "utf-8")
        conn.send(client_msg)


while True:
    conn, addr = sock.accept()  # conn это и есть сокет
    print(conn)
    print(f"{addr} connected")
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()

conn.close()
