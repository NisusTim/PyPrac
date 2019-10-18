import re

log = "Log_1017145743.txt"

def GetTextFromLog(log):
  with open(log) as f:
    log_data = f.read()  # read all as log_data text
  return log_data

def FrameParsing(txt):
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

if __name__ == '__main__':
  txt = GetTextFromLog(log)
  extract = FrameParsing(txt)
  [print(e) for ex in extract for e in ex]
