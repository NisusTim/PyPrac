import socket
import sys  # stderr

def ipv4_bind(port, type):
  return ipv4_passive_socket(port, type, False, 0)

def ipv4_listen(port, backlog):
  return ipv4_passive_socket(port, socket.SOCK_STREAM, True, backlog)

def ipv4_connect(ip, port, type):
  sv_socket = None
  sock_addr = (ip, port)

  try:
    sv_socket = socket.socket(socket.AF_INET, type, 0)
  except socket.error as e:
    print(sys.stderr, "socket: %s", e)
    sys.exit(1)

  try:
    sv_socket.connect(sock_addr)
  except socket.error as e:
    sv_socket.close()
    print(sys.stderr, "socket: %s", e)
    sys.exit(1)

  return sv_socket

def ipv4_passive_socket(port, type, do_listen, backlog):
  sv_socket = None
  sock_addr = ('', port)

  try:
    sv_socket = socket.socket(socket.AF_INET, type, 0)
  except socket.error as e:
    print(sys.stderr, "socket: %s", e)
    sys.exit(1)

  if (do_listen):
    try:
      sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
      sv_socket.close()
      print(sys.stderr, "setsockopt: %s", e)
      sys.exit(1)

  try:
    sv_socket.bind(sock_addr)
  except socket.error as e:
    sv_socket.close()
    print(sys.stderr, "bind: %s", e)
    sys.exit(1)

  if (do_listen):
    try:
      sv_socket.listen(backlog)
    except socket.error as e:
      sv_socket.close()
      print(sys.stderr, "listen: %s", e)
      sys.exit(1)

  return sv_socket


if __name__ == '__main__':
  pass
