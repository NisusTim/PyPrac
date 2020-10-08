from multiprocessing import Process, Pipe
import cv2
import time
import os

path = os.path.dirname(os.path.abspath(__file__))
path = path + '/test'
cnt = 0
cnt2 = 0
t = time.time()
RUN = True

def cam_read(cam, p_in):
  global cnt
  print("read() start %d: %f sec" % (cnt, time.time() - t))
  r, f = cam.read()
  print("read() end   %d: %f sec" % (cnt, time.time() - t))
  p_in.send(f)
  cnt += 1
  return f

def cam_save(cam, pipe):
  p_out, p_in = pipe
  p_in.close()
  global cnt2
  while RUN:
    try:
      frame = p_out.recv()
      # cv2.imwrite(path + time.strftime("%m%d_%H%M%S") + str(cnt) + '.png', frame)
      print("save() start %d: %f sec" % (cnt2, time.time() - t))
      cv2.imwrite(path + str(cnt2) + '.png', frame)
      print("save() end   %d: %f sec" % (cnt2, time.time() - t))
      cnt2 += 1
    except EOFError:
      break

def main():
  global RUN
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  p_out, p_in = Pipe()
  save_proc = Process(target=cam_save, args=(cam, (p_out, p_in), ))
  save_proc.daemon = True
  save_proc.start()

  p_out.close()
  for i in range(100):
    cam_read(cam, p_in)
  p_in.close()
  RUN = False
  save_proc.join()


if __name__ == '__main__':
  main()

