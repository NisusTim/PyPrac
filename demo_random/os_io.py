# Ref:
# https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user?noredirect=1&lq=1
class _Getch:
  """Gets a single character from standard input.  Doesnot echo to screen."""
  def __init__(self):
    try:
      self.impl = _GetchWindows()
    except ImportError:
      self.impl = _GetchUnix()


  def __call__(self):
    return self.impl()

class _GetchUnix:
  def __init__(self):
    import sys, tty

  def __call__(self):
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1) 
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class _GetchWindows:
  def __init__(self):
    import msvcrt

  def __call__(self):
    import msvcrt
    return msvcrt.getch()

if __name__ == '__main__':
  from time import sleep
  import sys
  getch = _Getch()
  print("starting console... ")
  cmd = ''
  line = ''
  cnt = 0
  ch = ''
  while ch != '\x1b':
    ch = getch()
    if ch == '\x7f':
      print('\b \b', end="", flush=True)
      if cnt > 0:
        cnt -= 1
        line = line[:cnt]
      # print("cnt: {}, line: {}, ch: {}".format(cnt, line, ch))
    elif ch == '\r':
      ch = '\n'
      print(ch, end="", flush=True)
      cmd = line[:cnt].encode()
      # reset
      cnt = 0
      line = ''
      print(cmd, flush=True)
    else:
      print(ch, end="", flush=True)
      cnt += 1
      line += ch 
