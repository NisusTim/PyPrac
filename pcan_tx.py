import can

def send():
  bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
  msg = can.Message(arbitration_id=0xc0ffee,
                    data=[0x31, 0x32, 0x33, 0x34])
  try:
    bus.send(msg)
    print("channel: {},  send_msg: {}".format(bus.channel_info, msg))
  except can.CanError:
    print("fail in sending message")

if __name__ == '__main__':
  send()
