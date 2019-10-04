from ctypes import *

lib = cdll.LoadLibrary('./libpycallc.so')

# int avg(int x, int y);
fun = lib.CalAvg
fun.argtypes = [c_int, c_int]  # arg type: check, protect
fun.restype = c_double         # ret type: optional
(x, y) = (3, 4)
res = fun(x, y)
print("CalAvg of ({}, {}): {}".format(x, y, res))

class Num_t(Structure):
  _fields_ = [
    ('num', c_uint16)
  ]

class Coord_t(Structure):
  _fields_ = [
    ('name', c_uint8 * 16),  # unsigned char name[16]
    ('x', c_uint16),
    ('y', c_uint16),
    ('n', POINTER(Num_t))
  ]
  
# void ResetOrigin(coord_t *X)
n = Num_t(87)
A = Coord_t((c_ubyte*16).from_buffer_copy(("A"+15*'\0').encode()), 8, 7, pointer(n))
print("Coord A(x, y, t): ({}, {}, {})".format(A.x, A.y, A.n.contents.num))
lib.ResetOrigin(pointer(A))
print("Reset A(x, y, t): ({}, {}, {})".format(A.x, A.y, A.n.contents.num))

# double CalDistance(coord_t *, coord_t *);
A = Coord_t((c_ubyte*16).from_buffer_copy(("A"+15*'\0').encode()), 8, 7)  # char array padding is nec
B = Coord_t((c_ubyte*16).from_buffer_copy(("B"+15*'\0').encode()), 5, 3)
fun = lib.CalDistance
fun.argtypes = [POINTER(Coord_t), POINTER(Coord_t)]
fun.restype = c_double
res = fun(pointer(A), pointer(B))
print("Distance between A({}, {}) and B({}, {}): {}".format(A.x, A.y, B.x, B.y, res))
