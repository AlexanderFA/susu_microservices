import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(2)
print('waiting for connection...')
conn, addr = sock.accept()
print('connected: ', addr)

user_name = conn.recv(1024).decode("utf-8")
print('user_name = ' + user_name)

while True:
    client_msg = conn.recv(1024).decode("utf-8")
    client_msg = bytes("User {} wrote: {}".format(user_name, client_msg), "utf-8")
    conn.send(client_msg)

conn.close()
