# Ref:
# https://openhome.cc/Gossip/DesignPattern/SingletonPattern.htm

"""
have only one instance of a class
"""

class Singleton:
  __single = None

  def __new__(cls):
    if not Singleton.__single:
      Singleton.__single = object.__new__(cls)
    return Singleton.__single

  def do_something(self):
    print("do something")

def main():
  """
  >>> s1 = Singleton()
  >>> s1.do_something()
  do something
  >>> s2 = Singleton()
  >>> s1 == s2
  True
  >>> s1 is s2
  True
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()

