import can

def recv_loop():
  bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS2', bitrate=250000)
  bus.state = can.bus.BusState.ACTIVE
  try:
    while True:
      msg = bus.recv(1)
      if msg is not None:
        print(msg)
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  recv_loop()
