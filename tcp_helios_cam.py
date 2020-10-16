from demo_tcp import ipv4_sockets as ipv4
import select  # select
import sys     # stdin, argv
import os      # read
from helios.helios import Helios
from camera.camera import Camera

import time
import fcntl, termios, array
import socket

SELECT_FD = -1
HE = None


def main(ip, port):
  sv_socket = ipv4.ipv4_connect(ip, port, ipv4.socket.SOCK_STREAM)
  sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 16*1024*1024)
  fd = sv_socket.fileno()
  if (fd != -1):
    global SELECT_FD
    SELECT_FD = fd

  cam = Camera()
  global HE
  HE = Helios(SELECT_FD, sv_socket, os.writev, os.read, cam.cap_image)
  # HE = Helios(SELECT_FD, sv_socket, os.writev, os.read, None)
  # HE = Helios(SELECT_FD, sv_socket, sv_socket.send, sv_socket.recv)

  read_fds = [sv_socket, sys.stdin]
  write_fds = [sv_socket]

  while True:
    try:
      readable, _, err = select.select(read_fds, [], [])

      for fd in readable:
        if fd is sys.stdin:
          stdin_handle()
        elif fd is sv_socket:
          HE.unpack_handler()

    except select.error as e:
      sv_socket.close()
      print(sys.stderr, "select %s", e);
      break;
    except KeyboardInterrupt:
      sv_socket.close()
      break;

def stdin_handle():
  data = os.read(sys.stdin.fileno(), 255)
  b = trim_newline(data)
  # print("  stdin: %s" % b.decode('latin-1'))
  cnsl_cmd_handle(b)

def trim_newline(msg):
  ''' @msg: bytes type. Remove trailing newlines of @msg. '''
  if (msg[-1: ] == b'\n'):
    return trim_newline(msg[ :-1])
  else:
    return msg

def cnsl_cmd_handle(msg):
  ''' @msg: bytes type. '''
  token = msg.split(b' ')

  if token[0] == b'send':
    os.write(SELECT_FD, msg[5: ])
  elif token[0] == b'helios':
    if token[1] == b'play':
      HE.pack_play(0, 0)
    elif token[1] == b'pause':
      HE.pack_pause()
    elif token[1] == b'close':
      print('ready for close')
      HE.close()
  else:
    print('no this command')

def fionread(fd):
  ''' @fd: file descriptor '''
  sock_size = array.array('i', [0])
  fcntl.ioctl(fd, termios.FIONREAD, sock_size)
  return sock_size[0]


if __name__ == '__main__':
  ip, port = sys.argv[1], sys.argv[2]
  main(ip, int(port))
