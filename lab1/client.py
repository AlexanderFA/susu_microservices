import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
sock.send(b'Hello!\n')
data = sock.recv(1024)
udata = data.decode("utf-8")
print("Server > " + udata)
sock.close()