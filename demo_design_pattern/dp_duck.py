# Ref:
# https://medium.com/@sheikhsajid/design-patterns-in-python-part-1-the-strategy-pattern-54b24897233e

class Duck(object):
  def __init__(self, name, weight):
    self.name = name
    self.weight = weight

# Quack Behaviour
class LoudDuck(Duck):
  def quack(self):
    print("QUACK! QUACK!!")

class GentleDuck(Duck):
  def quack(self):
    print("quack~")

# Types of Ducks
class VillageDuck(LoudDuck):
  def go_home(self):
    print("Going to the river")

class ToyDuck(GentleDuck):
  def lights_on(self):
    print("Lights on for 10 seconds")

class CityDuck(GentleDuck):
  def go_home(self):
    print("Goint to the Central Park pond")

# If a new type of duck, RobotDuck is a LoudDuck and needs to have "lights-on"
# Inheritance from ToyDuck is not good
#   1. RobotDuck has no is-a releationship with ToyDuck
#   2. Even if so, ToyDuck is-a GentleDuck and RobotDuck needs to be a LoudDuck
