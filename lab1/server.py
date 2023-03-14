import socket
import threading
from datetime import datetime
import re

clients = {}
DEFAULT_ROOM = 'common'
rooms = [DEFAULT_ROOM]

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(2)
print('waiting for connection...')


def send_to_all(msg):
    for client_SID, client_data in clients.items():
        if client_data['conn'] is not None:
            client_data['conn'].send(msg)


def send_to_all_in_room(msg, room_name=DEFAULT_ROOM):
    for client_SID, client_data in clients.items():
        if client_data['conn'] is not None and client_data['room'] == room_name:
            client_data['conn'].send(msg)


# отправка сообщения всем клиентам, кроме отправителя
def sent_to_all_except(msg, current_sid):
    for client_SID, client_data in clients.items():
        if client_SID != current_sid and client_data['conn'] is not None:
            client_data['conn'].send(msg)


def handle_client(conn, addr):
    SID = conn.recv(1024).decode("utf-8")
    # print(f"User with sid {SID} entered")
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if SID in clients:
        user_name = clients[SID]['name']
        clients[SID]['conn'] = conn
        clients[SID]['room'] = DEFAULT_ROOM
        conn.send(bytes(f"Welcome back {user_name}! Time now is: {now_time}", "utf-8"))
    else:
        conn.send(bytes("Enter your name: ", "utf-8"))
        user_name = conn.recv(1024).decode("utf-8")
        clients[SID] = {
            'name': user_name,
            'conn': conn,
            'room': DEFAULT_ROOM,
        }
        conn.send(bytes(f"Hello {user_name}! Start to send messages!", "utf-8"))

    sent_to_all_except(bytes(f"User {user_name} entered the chat {now_time}", "utf-8"), SID)

    while True:
        client_msg = conn.recv(1024).decode("utf-8")
        if client_msg == "\\exit":
            clients[SID]['conn'] = None
            conn.close()
            send_to_all(bytes(f"{user_name} has left the chat!", "utf-8"))
            break

        if client_msg == "\\list":
            client_names = [client['name'] for client in clients.values()]
            client_names_str = ", ".join(client_names)
            conn.send(bytes(f"User list:\n{client_names_str}", "utf-8"))
            continue

        match = re.search(r'^\\create\s(\w+)', client_msg)
        if match:
            rooms.append(match.group(1))
            clients[SID]['room'] = match.group(1)
            conn.send(bytes(f'You have just created and entered the room "{match.group(1)}"', "utf-8"))
            continue

        match = re.search(r'^\\join\s(\w+)', client_msg)
        if match:
            if match.group(1) in rooms:
                clients[SID]['room'] = match.group(1)
                conn.send(bytes(f'You have just entered the room "{match.group(1)}"', "utf-8"))
            else:
                conn.send(bytes(f'There is no "{match.group(1)}" room, \\create <room_name> to create it', "utf-8"))
            continue

        send_to_all_in_room(bytes("\033[1;32m{}\033[0m: {}".format(user_name, client_msg), "utf-8"), clients[SID]['room'])


while True:
    conn, addr = sock.accept()  # conn это и есть сокет
    print(conn)
    print(f"{addr} connected")
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()

conn.close()
