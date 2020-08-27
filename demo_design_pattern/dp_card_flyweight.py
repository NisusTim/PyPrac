# Ref:
# https://github.com/faif/python-patterns/blob/master/patterns/structural/flyweight__py3.py

"""
Structural Pattern: Flyweight
transparently reuse existing instances of objects with similar/identical state
"""

import weakref

class Card:
  # Could be a simple dict.
  # With WithValueDictionary gc can reclaim the object
  #   when there are no other references to it.
  # _pool = weakref.WeakValueDictionary()
  _pool = {}

  def __new__(cls, value, suit):
    obj = cls._pool.get(value + suit)
    if obj is None:
      obj = object.__new__(Card)
      cls._pool[value + suit] = obj
      obj.value, obj.suit = value, suit  # Normally in `__init__`
    return obj

  # If uncomment `__init__` and comment-out `__new__`
  #   Card becomes normal (non-flyweight)
  # def __init__(self, value, suit):
  #   self.value, self.suit = value, suit

  def __repr__(self):
    return "Card: {}{}".format(self.value, self.suit)

def main():
  """
  >>> c1 = Card('9', 'h')
  >>> c2 = Card('9', 'h')
  >>> c1, c2
  (Card: 9h, Card: 9h)
  >>> c1 == c2
  True
  >>> c1 is c2
  True

  >>> c1.new_attr = 'temp'
  >>> c3 = Card('9', 'h')
  >>> hasattr(c3, 'new_attr')
  True

  >>> Card._pool.clear()
  >>> c4 = Card('9', 'h')
  >>> hasattr(c4, 'new_attr')
  False
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()

