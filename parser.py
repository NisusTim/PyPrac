import pandas as pd
from datetime import timedelta
from io import StringIO
import re
from bitarray import bitarray
import struct
import sys
sys.path.append(r"/home/nisustim/Developments/Projects/Python_script/Py_Prac/Text_Stream_Parser")
from Text_Stream_Parser import TypeCast

def int_from_byte_in_bit(byte, start, end):
  pass

# log = 'can165615_s.log'
log = 'can175012.log'
with open(log) as f:
  text = f.read()

_RE_HEX = "([0-9a-fA-F]+)"
_RE_CAN = "([0-9]+:[0-9]+:[0-9]+.[0-9]+) ID = 0x{}  data = {}\n"
# _RE_CAN = "([0-9]+:[0-9]+:[0-9]+.[0-9]+) ID = 0x{}  data = {} {} {} {} {} {} {} {}"
RE_500 = _RE_CAN.format("(500)", "([0-9a-fA-F\s]+)")
RE_503 = _RE_CAN.format("(503)", "([0-9a-fA-F\s]+)")
RE_504 = _RE_CAN.format("(504)", "([0-9a-fA-F\s]+)")
# RE_500 = _RE_CAN.format(*(["(500)"] + [_RE_HEX, ] * 8))
# RE_503 = _RE_CAN.format(*(["(503)"] + [_RE_HEX, ] * 8))
# RE_504 = _RE_CAN.format(*(["(503)"] + [_RE_HEX, ] * 8))

COL_FIELD = ('time', 'can_id', 'i64')
# text = "17:01:19.658 ID = 0x503  data = 22 64 2A 68 87 EF 18 03"
item = re.findall(RE_500, text)
df = pd.DataFrame(item, columns=COL_FIELD)
df['time'] = pd.to_timedelta(df['time'])
df['i64'] = df['i64'].apply(lambda x: struct.pack(">Q", int(x.replace(" ", ""), 16)))
cipv_id = df['i64'].apply(lambda x: x[2])
acc_id = df['i64'].apply(lambda x: x[3])
aeb_id = df['i64'].apply(lambda x: x[4])
frame = df['i64'].apply(lambda x: ((x[6] << 8) & 0xFFFF) + x[7])
df_500 = pd.concat([df['time'], cipv_id, aeb_id, aeb_id, frame], axis=1)
df_500.columns = ('time', 'cipv_id', 'acc_cipv_id', 'aeb_cipv_id', 'radar_frame')

item = re.findall(RE_503, text)
df = pd.DataFrame(item, columns=COL_FIELD)
df['time'] = pd.to_datetime(df['time'])
df['i64'] = df['i64'].apply(lambda x: struct.pack(">Q", int(x.replace(" ", ""), 16)))
pos_x = df['i64'].apply(lambda x: (((x[0] << 4) & 0x0FFF) + ((x[1] >> 4) & 0x000F)) * 0.125)
pos_y = df['i64'].apply(lambda x: (((x[1] << 8) & 0x0FFF) + x[2]) * 0.125 - 128)
vel_x = df['i64'].apply(lambda x: (((x[3] << 4) & 0x0FFF) + ((x[4] >> 4) & 0x000F)) * 0.05 - 102)
vel_y = df['i64'].apply(lambda x: (((x[4] << 8) & 0x0FFF) + x[5]) * 0.05 - 102)
df_503 = pd.concat([pos_x, pos_y, vel_x, vel_y], axis=1)
df_503.columns = ('pos_x', 'pos_y', 'vel_x', 'vel_y')

item = re.findall(RE_504, text)
df = pd.DataFrame(item, columns=COL_FIELD)
df['time'] = pd.to_datetime(df['time'])
df['i64'] = df['i64'].apply(lambda x: struct.pack(">Q", int(x.replace(" ", ""), 16)))
acc_x = df['i64'].apply(lambda x: (((x[0] << 4) & 0x0FFF) + ((x[1] >> 4) & 0x000F)) * 0.04 - 40)
df_504 = pd.concat([acc_x, ], axis=1)
df_504.columns = ('acc_x', )

df_rd = pd.concat([df_500, df_503, df_504], axis=1)

# log2 = "Session 2.csv"
log2 = "Session 4.csv"
df_vb = pd.read_csv(log2)
df_vb['UTC time'] = pd.to_timedelta(df_vb['UTC time'], unit='s') + timedelta(hours=8)
# df_vb['UTC time'] = pd.to_datetime(df_vb['UTC time'], unit='s')
# df_vb['UTC time'] = df_vb['UTC time'].dt.tz_localize('utc').dt.tz_convert('Asia/Taipei')

df_rd = df_rd.loc[df_rd['time'] >= df_vb['UTC time'].iloc[0]]
df_rd = df_rd.loc[df_rd['time'] <= df_vb['UTC time'].iloc[-1]]
sel = ((df_vb['UTC time'] - df_vb['UTC time'].iloc[0]) % timedelta(seconds=0.0625)) < timedelta(seconds=0.01)
df_vb = df_vb.loc[sel]

df_rd.reset_index(drop=True, inplace=True)
df_vb.reset_index(drop=True, inplace=True)
df = pd.concat([df_rd, df_vb], axis=1)
# convert to string format before exporting
df['time'] = df['time'].astype(str).str.split().str[-1].str[-18:-6]
df['UTC time'] = df['UTC time'].astype(str).str.split().str[-1].str[-18:-6]
df.to_csv('test.csv', sep=',', encoding='utf-8', index=False)
