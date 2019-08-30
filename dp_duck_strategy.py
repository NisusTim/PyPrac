# Ref:
# https://gist.github.com/SheikhSajid/46be73501d9f80bb19bcfc7c393241d8#file-main-py

import abc  # Python's built-in abstract class library

class QuackStrategyAbstract(object):
  """You do not need to know about metaclasses.
     Just know that this is how you define abstract
     classes in Python."""
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def quack(self):
    """Required Method"""

class LoudQuackStrategy(QuackStrategyAbstract):
  def quack(self):
    print("QUACK! QUACK!!")

class GentleQuackStrategy(QuackStrategyAbstract):
  def quack(self):
    print("quack~")

class LightStrategyAbstract(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def lights_on(self):
    """Required Method"""

class OnForTenSecondStrategy(LightStrategyAbstract):
  def lights_on(self):
    print("Light on for 10 seconds")

###
# from dp_duck_strategy import LoudQuackStrategy
# from dp_duck_strategy import GentleQuackStrategy
# from dp_duck_strategy import OnForTenSecondStrategy

loud_quack = LoudQuackStrategy()
gentle_quack = GentleQuackStrategy()
ten_seconds = OnForTenSecondStrategy()

class Duck(object):
  def __init__(self, quack_strategy, light_strategy):
    self._quack_strategy = quack_strategy
    self._light_strategy = light_strategy

  def quack(self):
    self._quack_strategy.quack()

  def lights_on(self):
    self._light_strategy.lights_on()

# Types of Ducks
class VillageDuck(Duck):
  def __init__(self):
    super(VillageDuck, self).__init__(loud_quack, None)

  def go_home(self):
    print("Going to the river")

class ToyDuck(Duck):
  def __init__(self):
    super(ToyDuck, self).__init__(gentle_quack, ten_seconds)  

class CityDuck(Duck):
  def __init__(self):
    super(CityDuck, self).__init__(gentle_quack, None)

  def go_home(self):
    print("Going to the Central Park pond")

class RobotDuck(Duck):
  def __init__(self):
    super(RobotDuck, self).__init__(loud_quack, ten_seconds)

if __name__ == '__main__':
  # Note: Calling lights_on() on CityDuck or VillageDuck will result in 
  #       Attributeerror
  robo = RobotDuck()
  robo.quack()  # QUACK! QUACK!!
  robo.lights_on()  # Lights on for 10 seconds





