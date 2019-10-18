from collections import namedtuple
import re

class TextStreamParser:
  """ text stream parser by regex """
  Const = namedtuple('Const', ('Regex', 'Pattern'))
  Regex = namedtuple('Regex', ('num', 'int', 'float'))
  Pattern = namedtuple('Pattern', ('format', 'field'))

  _RE_NUM = "([-]?[0-9]+[.]?[0-9]*)"
  _RE_INT = "([-]?[0-9]+)"
  _RE_FLT = "([-]?[0-9]+[.][0-9]+)"

  CONST = Const(Regex(_RE_NUM, _RE_INT, _RE_FLT), 1)

  def __init__(self, x):
    self.info = x

  def LayeredParsing(self):
    pass

  def Update(self):
    pass

class FrameParser:
  T = TextStreamParser(1)
  b_field = ('bw', 'tg', 'rg', '00', '11', 'ct', 'ru', 'vu', 'ts')
  b_dict = dict.fromkeys(b_field, 'num')
  f_field = ('f', 't', '00', '11')
  f_dict = dict.fromkeys(f_field, 'num')
  b = T.Pattern(
        r"bw={}M,tg={},rg={},{}~{},ct={},ru={},vu={},ts={}ms" \
        .format(*(T.CONST.Regex.num, ) * 9), b_dict)
  f = T.Pattern(
        r"f{}-1 {}ms,\[{},{}\]" \
        .format(*(T.CONST.Regex.num, ) * 4), f_dict)
#    'e': r"(?:ham:|e{},)a:{},v:{},r:{},h:{},m:{}" \
#         .format(*(T.CONST.Regex.num, ) * 6),
#    't': r"Tracking\(f:{},l:{},r:{},y:{},ax:{},ay:{},az:{},v:{},g:{},d:{}," \
#    r"t:{},ca:{}\)".format(*(RE_FLTINT, ) * 12)
#  RE_D = r"[.]{{3}}Done\(m:{},t:{},T:{}us\)" \
#    .format(*(RE_FLTINT, ) * 3)
#  RE_M = r"mclt:tggs=>{},{}m" \
#    .format(*(RE_FLTINT, ) * 2)
  def __init__(self):
    pass

if __name__ == '__main__':
  t = TextStreamParser(1)
  f = FrameParser()
  print(f.b)
