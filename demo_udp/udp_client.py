# import socket
# from time import time

# addr = socket.getaddrinfo(
#   # 'localhost', 6000,
#   '127.0.0.1', 6000,
#   socket.AF_INET, socket.SOCK_DGRAM)[0]

# with socket.socket(*addr[:3]) as s:
#   s.connect(addr[4])
#   for i in range(10000):
#     t1 = time()
#     s.send(b'client')
#     t2 = time()
#     s.recv(1024)
#     t3 = time()
#     if i % 100 == 0:
#       print('{:.3f}ms {:.3f}ms'.format((t2 - t1) * 1000, (t3 - t2) * 1000))

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'This is the message.  It will be repeated.'

try:

    # Send data
    print(sys.stderr, 'sending "%s"' % message)
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    print(sys.stderr, 'waiting to receive')
    data, server = sock.recvfrom(4096)
    print(sys.stderr, 'received "%s"' % data)

finally:
    print(sys.stderr, 'closing socket')
    sock.close()
