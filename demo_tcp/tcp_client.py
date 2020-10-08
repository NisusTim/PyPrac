import ipv4_sockets as ipv4
import select  # select
import sys     # stdin, argv
import os      # read
import helios
import helios_h
import cam_capture

SELECT_FD = -1

def main(ip, port):
  sv_socket = ipv4.ipv4_connect(ip, port, ipv4.socket.SOCK_STREAM)
  fd = sv_socket.fileno()
  if (fd != -1):
    global SELECT_FD
    SELECT_FD = fd

  read_fds = [sv_socket, sys.stdin]
  write_fds = [sv_socket]


  path = os.path.dirname(os.path.abspath(__file__))
  path = path + '/test.png'
  cam = cam_capture.picture(0, path)

  while True:
    try:
      readable, _, err = select.select(read_fds, [], [])

      for fd in readable:
        if fd is sys.stdin:
          stdin_handle()
        elif fd is sv_socket:
          data = sv_socket.recv(1032)

    except select.error as e:
      sv_socket.close()
      print(stderr, "select %s", e);
      break;
    except KeyboardInterrupt:
      sv_socket.close()
      break;

def stdin_handle():
  data = os.read(sys.stdin.fileno(), 255)
  b = trim_newline(data)
  # print("  stdin: %s" % b.decode('latin-1'))
  cnsl_cmd_handle(b)

def trim_newline(b):
  size = len(b)

  if (b[size-1:size] == b'\n'):
    return b[ :-1: ]

def cnsl_cmd_handle(b):
  token = b.split(b' ')

  if token[0] == b'send':
    os.write(SELECT_FD, token[1:])
  elif token[0] == b'helios':
    he = helios.Helios(SELECT_FD, os.writev)
    if token[1] == b'play':
      he.pack_play(0, 0)
    elif token[1] == b'pause':
      he.pack_pause()
    del he


if __name__ == '__main__':
  ip, port = sys.argv[1], sys.argv[2]
  main(ip, int(port))
