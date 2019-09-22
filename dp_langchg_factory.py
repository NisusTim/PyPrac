# Ref:
# https://github.com/faif/python-patterns/blob/master/patterns/creational/factory.py

"""
Creational Pattern: Factory
delegate a specialized function/method to create instances
A Factory is an object for creating other objects.
"""

class EnglishGetter:
  """Simply echoes the msg"""
  def get(self, msg):
    return str(msg)

class ChineseGetter:
  """A simple localizer"""
  def __init__(self):
    self.trans = dict(dog='狗', cat="貓")

  def get(self, msg):
    # return str(msg) if no matched
    return self.trans.get(msg, str(msg))

def main():
  """
  >>> e, c = EnglishGetter(), ChineseGetter()
  >>> for msg in "dog parrot cat bear".split():
  ...   print(e.get(msg), c.get(msg))
  dog 狗
  parrot parrot
  cat 貓
  bear bear
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()

