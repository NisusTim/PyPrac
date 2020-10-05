import ipv4_sockets as ipv4
import select  # select
import sys     # argv
# import time

def main(ip, port):
  sv_socket = ipv4.ipv4_connect(ip, port, ipv4.socket.SOCK_STREAM)
  print(sv_socket)
  sv_socket.send('play'.encode())

  read_fds = [sv_socket]
  write_fds = [sv_socket]

  while True:
    try:
      readable, _, err = select.select(read_fds, [], [])

      for fd in readable:
        # if fd is sv_socket and fd.fileno() != -1:
        if fd is sv_socket:
          data = sv_socket.recv(1032)
          # print(data.decode('latin-1'))
        else:
          pass

    except select.error as e:
      sv_socket.close()
      print(stderr, "select %s", e);
      break;
    except KeyboardInterrupt:
      sv_socket.close()
      break;


if __name__ == '__main__':
  ip, port = sys.argv[1], sys.argv[2]
  main(ip, int(port))
