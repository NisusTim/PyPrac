from helios_h import *
import numpy as np
import sys


class Helios():
  pack_switch_action = {}
  unpack_switch_action = {}
  header = helios_hdr()

  def __init__(self, fd, send_rout):
    self.fd = fd
    self.sendv = send_rout
    self.init_switch_action()

  @classmethod
  def init_switch_action(cls):
    cls.pack_switch_action = {
      kDT_NULL:  lambda: None,
      kDT_MMAP:  cls.pack_mmap,
      kDT_MEM:   cls.pack_mem,
      kDT_TEXT:  cls.pack_text,
      kDT_PARAM: cls.pack_param,
      kDT_RFSP:  cls.pack_rfsp,
      kDT_LNCH:  cls.pack_lnch,
      kDT_PAUSE: cls.pack_pause,
      kDT_PLAY:  cls.pack_play,
      kDT_CONT:  cls.pack_cont,
      kDT_ADC:   cls.pack_adc,
      kDT_RANGE: cls.pack_range,
      kDT_DPPLR: cls.pack_dpplr,
      kDT_FFT3D: cls.pack_fft3d,
      kDT_HIST:  cls.pack_hist,
      kDT_PEAK:  cls.pack_peak,
      kDT_MEAS:  cls.pack_meas,
      kDT_CAP:   lambda: None
    }
    cls.unpack_switch_action = {
      kDT_NULL:  lambda: None,
      kDT_MMAP:  cls._unpack_mmap,
      kDT_MEM:   cls._unpack_mem,
      kDT_TEXT:  cls._unpack_text,
      kDT_PARAM: cls._unpack_param,
      kDT_RFSP:  cls._unpack_rfsp,
      kDT_LNCH:  cls._unpack_lnch,
      kDT_PAUSE: cls._unpack_pause,
      kDT_PLAY:  cls._unpack_play,
      kDT_CONT:  cls._unpack_cont,
      kDT_ADC:   cls._unpack_adc,
      kDT_RANGE: cls._unpack_range,
      kDT_DPPLR: cls._unpack_dpplr,
      kDT_FFT3D: cls._unpack_fft3d,
      kDT_HIST:  cls._unpack_hist,
      kDT_PEAK:  cls._unpack_peak,
      kDT_MEAS:  cls._unpack_meas,
      kDT_CAP:   lambda: None
    }

  def unpack_handler(self, msg):
    if len(msg) < HEADER_MSIZE:
      print(sys.stderr, "unpack_handler(): msg size < HEADER_MSIZE")
      return

    # memcpy(): bytes >> ctypes, no need to be converted back prior to sending
    memmove(addressof(self.header), msg, sizeof(helios_hdr))
    self.payload = np.frombuffer(msg[HEADER_MSIZE:], dtype=np.uint8)

    self.unpack_switch_action[self.header.dt]()

  def pack_handler(self, header, pld):
    '''@header: helios_hdr
       @pld:    bytes'''
    pld_msize = len(pld)
    pkt_csize = (pld_msize + PAYLOAD_MSIZE - 1) // PAYLOAD_MSIZE
    # convert helios_hdr to bytes and print
    # hdr = string_at(addressof(header), sizeof(helios_hdr))
    # print(hdr)

    while True:
      if pld_msize > PAYLOAD_MSIZE:
        header.rt = kOngo
        self.sendv(self.fd, [header, pld[ :PAYLOAD_MSIZE]])
        pld = pld[PAYLOAD_MSIZE: ]
        pld_msize = pld_msize - PAYLOAD_MSIZE
        pkt_csize = pkt_csize - 1
      else:
        header.rt = kDone
        self.sendv(self.fd, [header, pld[ :pld_msize]])
        pkt_csize = 0
      if pkt_csize <= 0:
        return

  def _unpack_mmap(self):
    pass

  def _unpack_mem(self):
    pass

  def _unpack_text(self):
    pass

  def _unpack_param(self):
    pass

  def _unpack_rfsp(self):
    pass

  def _unpack_lnch(self):
    pass

  def _unpack_pause(self):
    pass

  def _unpack_play(self):
    print('play')

  def _unpack_cont(self):
    pass

  def _unpack_adc(self):
    pass

  def _unpack_range(self):
    pass

  def _unpack_dpplr(self):
    pass

  def _unpack_fft3d(self):
    pass

  def _unpack_hist(self):
    pass

  def _unpack_peak(self):
    pass

  def _unpack_meas(self):
    pass

  def pack_mmap(self):
    pass

  def pack_mem(self):
    pass

  def pack_text(self):
    pass

  def pack_param(self):
    pass

  def pack_rfsp(self):
    pass

  def pack_lnch(self):
    pass

  def pack_pause(self):
    header = helios_hdr()
    header.dt = kDT_PAUSE
    header.rw = kRead
    header.pdt = kPDT_BIN
    self.pack_handler(header, b'')
    del header

  def pack_play(self, fr, ps):
    header = helios_hdr()
    header.dt = kDT_PLAY
    header.rw = kRead
    header.pdt = kPDT_BIN
    header.arg[0] = fr
    header.arg[1] = ps
    self.pack_handler(header, b'')
    del header

  def pack_cont(self):
    pass

  def pack_adc(self):
    pass

  def pack_range(self):
    pass

  def pack_dpplr(self):
    pass

  def pack_fft3d(self):
    pass

  def pack_hist(self):
    pass

  def pack_peak(self):
    pass

  def pack_meas(self):
    pass

