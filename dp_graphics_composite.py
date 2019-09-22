# Ref: 
# https://github.com/faif/python-patterns/blob/master/patterns/structural/composite.py

"""
Structural Pattern:
let clients treate individual objects and compoisitons uniformly
"""

class Graphic:
  def render(self):
    raise NotImplementedError("You should implement this.")

class CompositeGraphic(Graphic):
  def __init__(self):
    self.graphics = []

  def render(self):
    for graphic in self.graphics:
      graphic.render()

  def add(self, graphic):
    self.graphics.append(graphic)

  def remove(self, graphic):
    self.graphics.remove(graphic)

class Ellipse(Graphic):
  def __init__(self, name):
    self.name = name

  def render(self):
    print("Ellipse: {}".format(self.name))

def main():
  """
  >>> e1 = Ellipse("1")
  >>> e2 = Ellipse("2")
  >>> e3 = Ellipse("3")
  >>> e4 = Ellipse("4")
  >>> g1 = CompositeGraphic()
  >>> g2 = CompositeGraphic()
  >>> g1.add(e1)
  >>> g1.add(e2)
  >>> g1.add(e3)
  >>> g2.add(e4)
  >>> g0 = CompositeGraphic()
  >>> g0.add(g1)
  >>> g0.add(g2)
  >>> g0.render()
  Ellipse: 1
  Ellipse: 2
  Ellipse: 3
  Ellipse: 4
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()
