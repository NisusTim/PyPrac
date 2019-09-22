# Ref:
# https://github.com/faif/python-patterns/blob/master/patterns/creational/abstract_factory.py

"""
Creational Pattern: Abstract Factory
use a generic function with specific factories
"""

import random

class PetShop:
  def __init__(self, animal_factory=None):
    """input argument: class"""
    self.pet_factory = animal_factory

  def __repr__(self):
    """create an initiation from class"""
    pet = self.pet_factory()
    return str(pet)

class Dog:
  def speak(self):
    return "woof!"

  def __repr__(self):
    fmt = '{}: "{}"'
    return fmt.format("Dog", self.speak())

class Cat:
  def speak(self):
    return "meow~"

  def __repr__(self):
    fmt = '{}: "{}"'
    return fmt.format("Cat", self.speak())

def random_animal():
  return random.choice((Dog, Cat))

def main():
  """
  >>> PetShop(Cat)
  Cat: "meow~"
  >>> random.seed(1)
  >>> for i in range(5): PetShop(random_animal())
  Dog: "woof!"
  Dog: "woof!"
  Cat: "meow~"
  Dog: "woof!"
  Cat: "meow~"
  """

if __name__ == '__main__':
  import doctest
  doctest.testmod()

