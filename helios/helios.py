import io                      # BytesIO
from datetime import datetime  # now()
from threading import Thread
from queue import Queue
from .helios_h import *

import logging  # debug, basicConfig
from time import time

QUEUE_CSIZE_CAPACITY = 64*1024
SOCK_RECV_BUFF_MSIZE = 64*1024
IO_WRITE_BUFF_MSIZE = 4*1024
THREAD_SENTINEL = object()  # terminating flag via queue

DBGP = logging.debug
# logging.basicConfig(level=logging.DEBUG)  # comment this line to disable DBGP
# TODO: helios is abstract layer, something needs to be extracted like recv()
#       helios should NOT know what fd is.
# TODO:

class Helios():
  pack_switch_action = {}
  unpack_switch_action = {}
  header = helios_hdr()

  def __init__(self, fd, send_rout, recv_rout, adc_callback):
    self.fd = fd
    self.sendv = send_rout  # writev(fd, [msg1, msg2, ...])
    self.recv = recv_rout   # read(fd, msize)
    self.init_switch_action()

    self.is_adc_first_pkt = True
    self.adc_first_pkt_callback = adc_callback
    self.recv_buff = b''
    self.desc_wr_msize = 0
    self.desc_stream = io.BytesIO()
    self.log_stream = io.BytesIO()  # log: desc + adc
    self.log_queue = Queue(QUEUE_CSIZE_CAPACITY)
    self.save_thrd = Thread(target=self.save_log,
                            args=(self.log_stream, self.log_queue))
    self.save_thrd.start()

  @classmethod
  def init_switch_action(cls):
    cls.pack_switch_action = {
      kDT_NULL:  lambda x: None,
      kDT_MMAP:  cls.pack_mmap,
      kDT_MEM:   cls.pack_mem,
      kDT_TEXT:  cls.pack_text,
      kDT_PARAM: cls.pack_param,
      kDT_RFSP:  cls.pack_rfsp,
      kDT_LNCH:  cls.pack_lnch,
      kDT_PAUSE: cls.pack_pause,
      kDT_PLAY:  cls.pack_play,
      kDT_CONT:  cls.pack_cont,
      kDT_DESC:  lambda x: None,
      kDT_FHDR:  lambda x: None,
      kDT_ADC:   cls.pack_adc,
      kDT_RANGE: cls.pack_range,
      kDT_DPPLR: cls.pack_dpplr,
      kDT_FFT3D: cls.pack_fft3d,
      kDT_HIST:  cls.pack_hist,
      kDT_PEAK:  cls.pack_peak,
      kDT_MEAS:  cls.pack_meas,
      kDT_CAP:   lambda x: None
    }
    cls.unpack_switch_action = {
      kDT_NULL:  lambda x: None,
      kDT_MMAP:  cls._unpack_mmap,
      kDT_MEM:   cls._unpack_mem,
      kDT_TEXT:  cls._unpack_text,
      kDT_PARAM: cls._unpack_param,
      kDT_RFSP:  cls._unpack_rfsp,
      kDT_LNCH:  cls._unpack_lnch,
      kDT_PAUSE: cls._unpack_pause,
      kDT_PLAY:  cls._unpack_play,
      kDT_CONT:  cls._unpack_cont,
      kDT_DESC:  cls._unpack_desc,
      kDT_FHDR:  cls._unpack_fdhr,
      kDT_ADC:   cls._unpack_adc,
      kDT_RANGE: cls._unpack_range,
      kDT_DPPLR: cls._unpack_dpplr,
      kDT_FFT3D: cls._unpack_fft3d,
      kDT_HIST:  cls._unpack_hist,
      kDT_PEAK:  cls._unpack_peak,
      kDT_MEAS:  cls._unpack_meas,
      kDT_CAP:   lambda x: None
    }

  def unpack_handler(self):
    ''' '''

    self.recv_buff = self.recv_buff + self.recv(self.fd, SOCK_RECV_BUFF_MSIZE)

    while len(self.recv_buff) >= HEADER_MSIZE:

      msg = self.recv_buff[ :HEADER_MSIZE]
      memmove(addressof(self.header), msg, sizeof(helios_hdr))
      payload_msize = self.header.pl * PADDING_UNIT_MSIZE

      ''' expected payload msize not enough, then break! '''
      if payload_msize > len(self.recv_buff)-HEADER_MSIZE:
        break

      self.payload = self.recv_buff[HEADER_MSIZE:HEADER_MSIZE+payload_msize]
      self.recv_buff = self.recv_buff[HEADER_MSIZE+payload_msize: ]

      ''' if msg transmission is reliable protocol KeyError should NOT occurs '''
      try:
        self.unpack_switch_action[self.header.dt](self)
      except KeyError:
        DBGP("  self.recv_buff size: {}".format(len(self.recv_buff)))
        DBGP("  msg len: {}  pl: {}  payload len: {}"
              .format(len(msg), self.header.pl, len(self.payload)))


  def pack_handler(self, header, pld):
    '''@header: helios_hdr
       @pld:    bytes'''
    pld_msize = len(pld)
    pkt_csize = (pld_msize + PAYLOAD_MSIZE - 1) // PAYLOAD_MSIZE

    while True:

      if pld_msize > PAYLOAD_MSIZE:
        header.done = kOngo
        header.pl = (PAYLOAD_MSIZE + PADDING_UNIT_MSIZE - 1)  \
                    // PADDING_UNIT_MSIZE
        self.sendv(self.fd, [header, pld[ :PAYLOAD_MSIZE]])
        pld = pld[PAYLOAD_MSIZE: ]
        pld_msize = pld_msize - PAYLOAD_MSIZE
        pkt_csize = pkt_csize - 1
      else:
        ''' last one packet '''
        header.done = kDone
        header.pl = (pld_msize + PADDING_UNIT_MSIZE - 1) // PADDING_UNIT_MSIZE
        if pld_msize != header.pl * PADDING_UNIT_MSIZE:
          paddings = bytes((PADDING_VALUE for i in range(
                            header.pl * PADDING_UNIT_MSIZE - pld_msize)))
          pld = pld + paddings
          pld_msize = header.pl * PADDING_UNIT_MSIZE
        self.sendv(self.fd, [header,  pld[ :pld_msize]])
        pkt_csize = 0
        return

      if pkt_csize <= 0:
        break

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
    pass

  def _unpack_cont(self):
    pass

  def _unpack_desc(self):
    ''' to log desc file '''
    self.desc_wr_msize = self.desc_stream.write(self.payload)

    if self.header.done == kDone:
      file_name = "{}.desc".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
      with io.open(file_name, 'wb', IO_WRITE_BUFF_MSIZE) as f:
        self.desc_stream.seek(0)
        data = self.desc_stream.read(self.desc_wr_msize)
        f.write(data)

  def _unpack_fdhr(self):
    ''' @self.payload: if less than 1024 byte, padded
                       else, not defined!             '''
    TARGET_MSIZE = 1024
    append_msize = TARGET_MSIZE - len(self.payload)
    if append_msize > 0:
      paddings = bytes((PADDING_VALUE for i in range(append_msize)))
      self.payload = self.payload + paddings

    self.write_log(self.log_stream, self.payload, self.log_queue)

  def _unpack_adc(self):
    if self.header.done == kDone:
      self.adc_first_pkt_callback()

    self.write_log(self.log_stream, self.payload, self.log_queue)

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
    header.pdt = kPDT_BIN
    header.rw = kRead
    self.pack_handler(header, b'')
    del header

  def pack_play(self, fr, ps):
    header = helios_hdr()
    header.dt = kDT_PLAY
    header.pdt = kPDT_BIN
    header.rw = kRead
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

  def close(self):
    DBGP("  Helios(): close instance.")
    self.log_queue.put(THREAD_SENTINEL)
    self.save_thrd.join()
    DBGP("  Helios(): close done.")


  @staticmethod
  def header_print(helios_header):
    ''' @helios_header: helios_hdr
        convert <helios_hdr> into <bytes>'''
    hdr_in_bytes = string_at(addressof(helios_header), sizeof(helios_hdr))
    print(hdr_in_bytes)

  @staticmethod
  def write_log(stream, msg, log_queue):
    ''' producer to enqueue msg
        @stream: BytesIO.         '''
    write_msize = stream.write(msg)
    log_queue.put(write_msize)

  @staticmethod
  def save_log(stream, log_queue):
    ''' consumer to dequeue msg and save into a log file.
        @stream: BytesIO.                                   '''
    total = 0
    cnt = 0
    t = 0

    file_name = "{}.adc".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    with io.open(file_name, 'wb', IO_WRITE_BUFF_MSIZE) as f:
      while True:
        f.flush()
        read_msize = log_queue.get()
        if read_msize is THREAD_SENTINEL:
          break
        stream.seek(0)
        data = stream.read(read_msize)

        f.write(data)
        total += read_msize

        # for debug
        if read_msize == 32 or read_msize == 256:
          if cnt == 0:
            t = time()
          cnt += 1
          if cnt % 20 == 0:
            print("  save():  {:6.3f} sec  ({:5d})  {:12d} (+{:4d} bytes)"
                  .format(time() - t, cnt, total, read_msize))

