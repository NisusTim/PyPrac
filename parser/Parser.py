#coding=utf-8
import re
import numpy as np

def GetTextFromLog(log):
  with open(log) as f:
    log_data = f.read()  # read all as log_data text
  return log_data

def reform(item):
  if any(isinstance(e, list) for e in item) \
    or any(isinstance(e, tuple) for e in item) \
    and len(item) == 1:
    return tuple(str2num(e) for ls in item for e in ls)
  else:
    return tuple(tuple(str2num(e) for e in ls) for ls in item)

def str2num(s):
  if not isinstance(s, str) or not s:
    return
  elif s.find('.') == -1:
    return int(s)
  else:
    return float(s)

def FrameParse(txt):
  # '(', ')', '[', ']': prefix with '\'
  # '.': packed with '[]' => '[.]'
  RE_FLTINT = r"([-]?[0-9]+[.]?[0-9]*)"
  RE_B = r"bw={}M,tg={},rg={},{}~{},ct={},ru={},vu={},ts={}ms" \
    .format(*(RE_FLTINT, ) * 9)
  RE_F = r"f{}-1 {}ms,\[{},{}\]" \
    .format(*(RE_FLTINT, ) * 4)
  RE_E = r"(?:ham:|e{},)a:{},v:{},r:{},h:{},m:{}" \
    .format(*(RE_FLTINT, ) * 6)
  RE_T = r"Tracking\(f:{},l:{},r:{},y:{},ax:{},ay:{},az:{},v:{},g:{},d:{}," \
    r"t:{},ca:{}\)".format(*(RE_FLTINT, ) * 12)
  RE_D = r"[.]{{3}}Done\(m:{},t:{},T:{}us\)" \
    .format(*(RE_FLTINT, ) * 3)
  RE_M = r"mclt:tggs=>{},{}m" \
    .format(*(RE_FLTINT, ) * 2)

  extract = []
  start = 0
  curr_hdr = re.search(RE_B + r"\n.*" + RE_B, txt[start:])
  while curr_hdr is not None:
    start += curr_hdr.end() + 1
    next_hdr = re.search(RE_B + r"\n.*" + RE_B, txt[start:])
    if next_hdr is not None:
      end = start + next_hdr.start()
    else:
      end = len(txt)
    item_b = curr_hdr.groups()
    b_cnt = len(item_b)
    item_b = tuple(item_b[i:i + b_cnt//2] for i in range(0, b_cnt, b_cnt//2))
    item_f = re.findall(RE_F, txt[start:end])
    item_e = re.findall(RE_E, txt[start:end])
    item_t = re.findall(RE_T, txt[start:end])
    item_d = re.findall(RE_D, txt[start:end])
    item_m = re.findall(RE_M, txt[start:end])
    item_b = reform(item_b)
    item_f = reform(item_f)
    item_e = reform(item_e)
    item_t = reform(item_t)
    item_d = reform(item_d)
    item_m = reform(item_m)
    extract.append((item_b, item_f, item_e, item_t, item_d, item_m))
    curr_hdr = next_hdr
  return extract

def GoFrameParse():
  log = "Log_1017145743.txt"
  txt = GetTextFromLog(log)
  extract = FrameParse(txt)
  [print(e) for ex in extract for e in ex]

def BlackBoxParse(txt):
  RE_API = r"(?<=[[\d+]]\s)([\s0-9A-F]{71})(?=\n)"
  RE_API2 = r"(?<=[[\d+]]\s)([\s0-9A-F]{71})(?=--[\d]+,[\d]+\n)"
  RE_BBOX_start = r"flash dump fd0000 30000"
  RE_BBOX = r"(?<=[[\d+]]\s\s\s)([\s0-9A-F]{71})(?=\n)"
  FLASH_BLANK = 'FFFFFFFF'
  BLANK_PAGE = " ".join([FLASH_BLANK, ] * 8)

  start = 0
  curr_hdr = re.search(RE_BBOX_start, txt[start:])
  start += curr_hdr.end() + 1
  extract = re.findall(RE_BBOX, txt[start:])

  sort_head = 0
  for i in range(2048, len(extract), 2048):
    if (BLANK_PAGE == extract[i - 1]):
      sort_head = i
      break
  extract_sort = extract[sort_head:] + extract[:sort_head]

  re_api_head = extract_sort[1][2:-4]
  curr_hdr = re.search(re_api_head, txt[:])
  start = curr_hdr.start() - 30
  extract_api = re.findall(RE_API, txt[start:])
  return extract_api, extract, extract_sort

def BlackBoxTruncate(api, bbox):
  bbox_truncated = []
  bbox_page = len(bbox)
  for i in range(bbox_page):
    if bytes.fromhex(bbox[i][2:18]) == b'Cub.Inc':
      continue
    if bbox[i] == ' '.join(['FFFFFFFF', ] * 8):
      break
    bbox_truncated.append(bbox[i][2:-4])

  api_truncated = [item[2:-4] for item in api]
  return api_truncated, bbox_truncated

def GoBlackBoxParse():
  log = "Log_1203152819.txt"
  txt = GetTextFromLog(log)
  api, b, bbox = BlackBoxParse(txt)
  api_t, bbox_t = BlackBoxTruncate(api, bbox)

  with open('bbox_truncated.txt', 'w') as f:
    for item in bbox_t:
      f.write("{}\n".format(item))

  with open('api_truncated.txt', 'w') as f:
    for item in api_t:
      f.write("{}\n".format(item))

def TestBlackBox():
  """
  >>> [api, b, bbox] = GoBlackBoxParse()
  >>> api = np.array([np.frombuffer(bytes.fromhex(item), dtype=np.uint8) for item in api])
  >>> bbox = np.array([np.frombuffer(bytes.fromhex(item), dtype=np.uint8) for item in bbox])
  >>> bbox.shape == (6 * 0x400, 32)
  True
  >>> api.shape[0] <= 6 * 0x400
  True
  >>> api.shape[1] <= 32
  True
  >>> api = api[-(6 * 0x400):]
  >>> res = True
  >>> for i in range(10):
  ...   api[i] == bbox[i]
  True
  """

if __name__ == '__main__':
  GoBlackBoxParse()

#  np_api = np.array([np.frombuffer(bytes.fromhex(item), dtype=np.uint8) for item in api])
#  np_bbox = np.array([np.frombuffer(bytes.fromhex(item), dtype=np.uint8) for item in bbox])
#  bbox_cap = np_bbox.shape[0]
#  api_count = 0
#  for idx in range(10000):
#    if np_bbox[idx, 1:8].tobytes() == b'Cub.Inc':
#      print("continue")
#      continue
#    if (np_bbox[idx] == 0xFF * np.ones(32, dtype=np.uint8)).all():
#      print("FF")
#      break
#    if (np_bbox[idx, 1:31] != np_api[api_count, 1:31]).any():
#      print("bbox: {}".format(np_bbox[idx, 1:31]))
#      print("api:  {}".format(np_api[api_count, 1:31]))
#    api_count += 1

  # import doctest
  # doctest.testmod()
