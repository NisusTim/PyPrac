from ctypes import *
from collections import namedtuple
import re

""" MACRO """
FRAME_CAP              = 65536
META_MEAS_CAP          =   256
META_MEAS_GROUP_CAP    =     2
MAX_VELOCITY_SUPPORTED =    70

""" Typedef """
kNotPaired = 10

class meta_meas_t(Structure):
  pass

class meta_meas_group_t(Structure):
  pass

class MeasAsn(Structure):
  pass
 
meta_meas_t._fields_ = [
  ('rng',     c_float),
  ('rng_x',   c_float),
  ('rng_y',   c_float),
  ('vel',     c_float),
  ('ang',     c_float),
  ('ang_ver', c_float),
  ('cos_val', c_float),
  ('mag',     c_uint16),
  ('vbin',    c_int8),
  ('flip',    c_int8)
]

meta_meas_group_t._fields_ = [
  ('mm',         meta_meas_t * META_MEAS_CAP),
  ('vel_max',    c_float),
  ('mm_cnt',     c_uint16)
]

MeasAsn._fields_ = [
  ('mmg',        meta_meas_group_t * META_MEAS_GROUP_CAP),
  ('gate',       meta_meas_t),
  ('curr',       POINTER(meta_meas_group_t)),
  ('prev',       POINTER(meta_meas_group_t)),
  ('time_delta', c_float),
  ('mult_vel',   c_uint8),
  ('curr_idx',   c_uint8),
  ('API_Association', CFUNCTYPE(None, POINTER(MeasAsn)))
]

""" Methods """
lib = cdll.LoadLibrary('./libmeasasn.so')
lib.API_NewMeasAsn.argtypes = [POINTER(MeasAsn)]
lib.API_NewMeasAsn.restype = None

MetaMeas = namedtuple('MetaMeas', 
  ['rng', 'rng_x', 'rng_y', 'vel', 'ang', 'ang_ver', 'cos_val', 'mag', 'vbin',
   'flip'])

class MeasAssociation:
  def __init__(self):
    pass

  def Parsing(self, log):
    txt = self.GetTextFromLog(log)
    parser = TGG_Parser(txt)
    self.extract = parser.extract

  def Invoking(self):
    pass

  def Feeding(self):
    M = []
    pass

  @staticmethod
  def GetTextFromLog(log):
    with open(log) as f:
      log_data = f.read()  # read all as log_data
    return log_data

class TGG_Parser:
  Tgg = namedtuple('Tgg', ['Hdr', 'Item'])
  Header = namedtuple('Hdr', ['sl', 'ru', 'vu', 'dt'])
  Item = namedtuple('Item', ['idx', 'ang', 'vel', 'rng', 'mag'])

  RE_FLTINT = r"([-]?[0-9]+[.]?[0-9]*)"
  # RE_MEAS = r"e([0-9]+),a:{},v:{},r:{},h:{},m:{}" \
  #   .format(RE_FLOAT, RE_FLOAT, RE_FLOAT, RE_FLOAT, RE_FLOAT)
  RE_TGG_HDR = r"tgg\({}\):ru={},vu={},dt={}s" \
    .format(*(RE_FLTINT, ) * 4)
  RE_TGG = r"t{},a:{},v:{},r:{},m:{}" \
    .format(*(RE_FLTINT, ) * 5)

  def __init__(self, txt):
    self.extract = self.Parsing(txt)

  def Parsing(self, txt):
    """ for two layered: header and items
    extract[list: Tgg_idx]x[tuple: Hdr, Item]
    Hdr[tuple: sl, ru, vu, dt]
    Item[tuple: idx]x[tuple: idx, ang, vel, rng, mag]
    """
    extract = []
    start = 0
    curr_hdr = re.search(self.RE_TGG_HDR, txt[start:])  # first header search
    while curr_hdr is not None:
      start += curr_hdr.end() + 1
      next_hdr = re.search(self.RE_TGG_HDR, txt[start:])  # next header search
      if next_hdr is not None:
        end = start + next_hdr.start()
      else:
        end = len(txt)
      curr_item = re.findall(self.RE_TGG, txt[start:end])  # list
      hdr = self.Header(
        *(self.str2num(e) for e in curr_hdr.groups()))
      item = tuple(self.Item(
        *(self.str2num(e) for e in ls)) for ls in curr_item)
      extract.append(self.Tgg(hdr, item))
      curr_hdr = next_hdr
    return extract  

  def EzParsing(self, txt):
    """ for no layered architecture data structure """
    REGEX = ''
    extract = re.findall(REGEX, txt)
    extract = tuple(self.str2num(extract) for e in extract)
    return extract

  @staticmethod
  def str2num(str):
    return int(str) if str.find(".") == -1 else float(str)

class Feeder:
  pass

class Ctype:
  def __init__(self, obj):
    self.obj = obj

  def __repr__(self):
    obj = self.obj
    info = ""
    for field_name, field_type in obj._fields_:
      info += "{:>10s}: {:10.2e}\n".format(field_name, getattr(obj, field_name))
    return info
