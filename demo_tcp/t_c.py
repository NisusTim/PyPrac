import socket

HOST = '0.0.0.0'
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = "input msg"
    s.send(cmd.encode())
    data = s.recv(1024)
    print("server send : %s " % (data))
