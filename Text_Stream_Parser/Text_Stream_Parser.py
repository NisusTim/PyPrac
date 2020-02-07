from collections import namedtuple
import re
import string

class TextStreamParser:
  """ text stream parser by regex """
  Const = namedtuple('Const', ('Regex', 'Pattern'))
  Regex = namedtuple('Regex', ('num', 'int', 'float'))
  Pattern = namedtuple('Pattern', ('format', 'field'))

  _RE_NUM = "([-]?[0-9]+[.]?[0-9]*)"
  _RE_HEX = "((0[xX])?[0-9a-fA-F]+)"
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

class TypeCast:
  @staticmethod
  def str_tuple_to_num(item, base=10):
    """str elements in list/tuple cast to num elements in tuple"""

    if any(isinstance(e, list) for e in item) \
      or any(isinstance(e, tuple) for e in item) and len(item) == 1:
      return tuple(TypeCast.str2num(e, base) for ls in item for e in ls)
    else:
      return tuple(tuple(TypeCast.str2num(e, base) for e in ls) for ls in item)

  @staticmethod
  def str2num(s, base=10):
    """cast str to int or float"""

    if not isinstance(s, str) or not s:
      return None
    elif s.isdigit():
      return int(s, base)
    elif all(c in set(string.hexdigits) for c in s):
      return int(s, 16)
    elif s.find('.') != -1:
      try:
        float(s)
        return float(s)
      except:
        return s

import unittest
class TypeCastTestCase(unittest.TestCase):
  def test_str_tuple_to_num(self):
    input1 = (('450', '7', '38.3', '0.19990'), ('150', '182666', '26.3', '0.29111'))
    expect1 = ((450, 7, 38.3, 0.19990), (150, 182666, 26.3, 0.29111))
    self.assertEqual(TypeCast.str_tuple_to_num(input1), expect1)
    self.assertEqual(TypeCast.str_tuple_to_num((input1[0], )), expect1[0])

  def test_str2num(self):
    self.assertEqual(TypeCast.str2num("3.14"), 3.14)
    self.assertEqual(TypeCast.str2num("9487"), 9487)
    self.assertEqual(TypeCast.str2num("ABCD"), 0xABCD)
    self.assertEqual(TypeCast.str2num("0xABCD"), None)

if __name__ == '__main__':
  # unittest.main()
  # t = TextStreamParser(1)
  # f = FrameParser()
  # print(f.b)
  pass
