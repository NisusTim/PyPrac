from ctypes import *
import sys, os

def demo_cal_avg(x, y):
  fun = lib.CalAvg
  fun.argtypes = [c_int, c_int]  # arg type: check, protect
  fun.restype = c_double         # ret type: optional
  res = fun(x, y)
  print("  (x, y): ({}, {})".format(x, y))
  print("  CalAvg({}, {}): {:.2f}".format(x, y, res))
  print("")

class Num_t(Structure):
  _fields_ = [
    ('cnt', c_uint16)
  ]

class Coord_t(Structure):
  _fields_ = [
    ('name', c_uint8 * 8),  # unsigned char name[8]
    ('vec_x', c_uint16),
    ('vec_y', c_uint16),
    ('n', POINTER(Num_t))
  ]

def demo_cal_distance(x, y):
  fun = lib.CalDistance
  fun.argtypes = [POINTER(Coord_t), POINTER(Coord_t)]
  fun.restype = c_double
  res = fun(pointer(x), pointer(y))
  print("  {}({}, {})".format(string_at(x.name, 8).decode(), x.vec_x, x.vec_y))
  print("  {}({}, {})".format(string_at(y.name, 8).decode(), y.vec_x, y.vec_y))
  print("  CalDistance({}, {}): {:.2f}".format(
         string_at(x.name, 8).decode(), string_at(y.name, 8).decode(), res));
  print("")

def demo_reset_origin(x):
  fun = lib.ResetOrigin
  fun.argtypes = [POINTER(Coord_t)]
  fun.restype = None
  print("  before: {}({}, {})".format(string_at(x.name, 8).decode(),
                                      x.vec_x, x.vec_y))
  res = fun(pointer(x))
  print("  ResetOrigin({})".format(string_at(x.name, 8).decode()))
  print("  after : {}({}, {})".format(string_at(x.name, 8).decode(),
                                     x.vec_x, x.vec_y))
  print("")


if __name__ == '__main__':
  # Load dynamic shared object.
  shared_obj = "libcoord.so"
  shared_obj = os.path.join(os.path.dirname(sys.path[0]), 'build') \
               + os.path.sep + shared_obj
  lib = cdll.LoadLibrary(shared_obj)

  # double CalAvg(int, int)
  demo_cal_avg(7, 8)

  # double CalDistance(coord_t *, coord_t *);
  n = Num_t(87)
  # char array padding is nec
  A = Coord_t((c_ubyte*8).from_buffer_copy(("point A"+1*'\0').encode()), 8, 7, pointer(n))
  B = Coord_t((c_ubyte*8).from_buffer_copy(("point B"+1*'\0').encode()), 5, 3)
  demo_cal_distance(A, B)

  # void ResetOrigin(coord_t *)
  demo_reset_origin(A)
