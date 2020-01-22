import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
  # s.bind(('localhost',6000))
  s.bind(('127.0.0.1',6000))
  while True:
    data, addr = s.recvfrom(1024)
    s.sendto(b'',addr)
