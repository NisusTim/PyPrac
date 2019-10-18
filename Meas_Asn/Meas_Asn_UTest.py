from meas_association import *
import numpy as np
import re
from math import sin, cos, pi
import copy

# log = 'Log_0916113313_test.txt'
log = 'Log_1016163153_asso1.txt'

# def GetMeasByFrame(extract):
#   M = [MetaMeasGroup() for _ in range(extract_cnt)]
#   mmg_idx, mmg_cnt, mm_idx = 0, 0, 0
#   while (new_head < extract_cnt):
#     if (extract[new_head][0] == 0):
#       mmg_cnt += 1
#       mmg_idx = mmg_cnt - 1
#       mm_idx = 0
#       # initialize new one
#       M[mmg_idx].vel_max = 20.0
#       M[mmg_idx].time_delta = 62.5
#     rng, vel, ang = extract[new_head][3], extract[new_head][2], extract[new_head][1]
#     M[mmg_idx].mm[mm_idx] = MetaMeas(
#       rng=rng, vel=vel, ang=ang, rng_x=rng*cos(ang/pi), rng_y=rng*sin(ang/pi))
#     M[mmg_idx].mm_cnt += 1
#     mm_idx += 1
#     new_head += 1
  #for i in range(mmg_cnt):
  #  print("M[{:2}]".format(i))
  #  for j in range(M[i].mm_cnt):
  #    print("M[{:2}].mm[{:2}]: rng:{:7.2f}, vel:{:7.2f}, ang:{:7.2f}"
  #      .format(i, j, M[i].mm[j].rng, M[i].mm[j].vel, M[i].mm[j].ang))
# return M

def PrintMMG(mmg):
  cnt = mmg.mm_cnt
  for i in range(cnt):
    x = mmg.mm[i]
    print('{:2}: rng:{:7.2f}, vel:{:7.2f}, ang:{:7.2f}, flip:{:3}'.format(i, x.rng, x.vel, x.ang, x.flip))

def PrintMM(mm):
  x = mm
  print('rng:{:7.2f}, vel:{:7.2f}, ang:{:7.2f}, flip:{:3}'.format(x.rng, x.vel, x.ang, x.flip))

def PrintWithinGate(curr_mm, prev, gate):
  cnt = prev.mm_cnt
  PrintMM(curr_mm)
  for i in range(cnt):
    rng_delta = curr_mm.rng - prev.mm[i].rng
    # vel_delta = curr_mm.vel - prev.mm[i].vel
    ang_delta = curr_mm.ang - prev.mm[i].ang
    x = prev.mm[i]
    if (rng_delta < -gate.rng):
      break
    if (rng_delta > gate.rng):
      continue
    # if (abs(vel_delta) < vel_gate and abs(ang_delta) < ang_gate):
    print('{}{:2}: rng:{:7.2f}, vel:{:7.2f}, ang:{:7.2f}, flip:{:3}{}'
          .format('\033[92m', i, x.rng, x.vel, x.ang, x.flip, '\033[0m'))

def Test1():
  obj = MeasAssociation()
  obj.Parsing(log)
  M = GetMeasByFrame(obj.extract)
  G = MetaMeas(
    rng = 1.414,
    rng_x = 3,
    rng_y = 4,
    vel = 2)
  MA = MeasAsn(
    gate = G,
    prev = pointer(M[0]),
    curr = pointer(M[1]),
    mult_vel = 3,
    time_delta = 62.5
    )
  lib.API_NewMeasAsn(pointer(MA))
  MA.API_Association(pointer(MA))
  # PrintMM(MA.curr.contents.mm[0])
  PrintMMG(MA.prev.contents)
  for i in range(MA.curr.contents.mm_cnt):
    PrintWithinGate(MA.curr.contents.mm[i], MA.prev.contents, MA.gate)

if __name__ == '__main__':
  a = MeasAssociation()
  a.Parsing(log)
  a.extract = tuple(e for e in a.extract if len(e.Item) != 0)
#  extract_cnt = len(a.extract)
#  M = [meta_meas_group_t() for _ in range(extract_cnt)] 
#  for mmg_idx in range(extract_cnt):
#    E = a.extract[mmg_idx]
#    M[mmg_idx].mm_cnt = len(E.Item)
#    M[mmg_idx].vel_max = 60
#    for mm_idx in range(M[mmg_idx].mm_cnt):
#      I = E.Item[mm_idx]
#      rng, vel, ang, mag = I.rng*E.Hdr.ru, I.vel, I.ang, I.mag
#      b = meta_meas_t(
#        rng=rng, vel=vel, ang=ang, rng_x=rng*cos(ang/180*pi), rng_y=rng*sin(ang/180*pi))
#      M[mmg_idx].mm[mm_idx] = b
#  x = M[0].mm[0]
