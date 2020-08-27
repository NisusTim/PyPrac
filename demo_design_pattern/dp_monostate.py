# Ref:
# https://github.com/faif/python-patterns/blob/master/patterns/creational/borg.py

"""
there are multiple instances that share the same state
In Python, instance attributes are stored in a attribute dictionary called 
__dict__, Borg pattern shares the same dictionary
"""

class Borg:
  __shared_state = {}

  def __init__(self):
    self.__dict__ = self.__shared_state
    self.state = 'Init'

  def __repr__(self):
    return self.state

class SubBorg(Borg):
  pass

def main():
  """
  >>> b1 = Borg()
  >>> b2 = Borg()
  >>> b1.state = 'Idle'
  >>> b2.state = 'Running'
  >>> b1
  Running
  >>> b2
  Running
  >>> b2.state = 'Zombie'
  >>> b1
  Zombie
  >>> b2
  Zombie
  >>> b1 == b2
  False
  >>> b1 is b2
  False
  >>> b3 = SubBorg()
  >>> b1
  Init
  >>> b2
  Init
  >>> b3
  Init
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()

