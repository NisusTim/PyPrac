import fcntl, termios, array

def fionread(fd):
  ''' @fd: file descriptor '''
  sock_size = array.array('i', [0])
  fcntl.ioctl(fd, termios.FIONREAD, sock_size)
  return sock_size[0]
