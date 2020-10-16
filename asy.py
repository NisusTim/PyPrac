import asyncio
import cv2
import time
import os

from queue import Queue
from threading import Thread
from io import BytesIO
import numpy as np

LOOP_CSIZE = 1000
VID_FPS    = 20.0
IMG_WIDTH  = 1280
IMG_HEIGHT = 720

path = os.path.dirname(os.path.abspath(__file__))
print(path)
path = path + '/test'
cnt = 0
cnt2 = 0
t = time.time()
buff = BytesIO()
# pro_n = 0
con_n = 0
que = Queue(30)

async def cam_read(cam):
  global cnt
  t1 = time.time(); # print("read() start   %d: %f sec" % (cnt, t1 - t))
  _, img = cam.read()
  t2 = time.time(); # print("read() end     %d: %f sec" % (cnt, t2 - t))
  print("read() elapsed %d: %f sec" % (cnt, t2 - t1))
  cnt += 1
  return img

async def cam_save_img(cam, img):
  global cnt2
  # cv2.imwrite(path + time.strftime("%m%d_%H%M%S") + str(cnt2) + '.png', frame)
  t1 = time.time(); # print("save() start   %d: %f sec" % (cnt2, time.time() - t))
  cv2.imwrite(path + str(cnt2) + '.png', img)
  t2 = time.time(); # print("save() end     %d: %f sec" % (cnt2, time.time() - t))
  print("save() elapsed %d: %f sec" % (cnt2, t2 - t1))
  cnt2 += 1

async def cam_chain(cam):
  img = await cam_read(cam)
  await cam_save_img(cam, img)

def asy_image():
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)
  loop = asyncio.get_event_loop()
  tasks = [loop.create_task(cam_chain(cam)) for i in range(LOOP_CSIZE)]
  loop.run_until_complete(asyncio.wait(tasks))

def cam_read_pro(cam):
  global cnt
  # global pro_n
  if not que.full():
    t1 = time.time(); # print("read() start   %d: %f sec" % (cnt, t1 - t))
    _, img = cam.read()
    _, img = cv2.imencode(".jpg", img)
    a = buff
    # a.seek(pro_n)
    n = a.write(img)
    que.put(n)
    # pro_n += n
    t2 = time.time(); # print("read() end     %d: %f sec" % (cnt, t2 - t))
    print("read() elapsed %d: %f sec" % (cnt, t2 - t1))
    cnt += 1
  else:
    time.sleep(1)
    cam_read_pro(cam)

def cam_save_con():
  global cnt2
  global con_n
  while cnt2 < LOOP_CSIZE:
    if not que.empty():
      t1 = time.time(); # print("save() start   %d: %f sec" % (cnt2, t1 - t))
      a = buff
      a.seek(con_n)
      n = que.get()
      # x = a.read(n)
      con_n += n
      # img = a.read(n)
      img = cv2.imdecode(np.fromstring(a.read(n), dtype=np.uint8), cv2.IMREAD_COLOR)
      cv2.imwrite(path + str(cnt2) + '.jpg', img)
      t2 = time.time(); # print("read() end     %d: %f sec" % (cnt2, t2 - t))
      print("save() elapsed %d: %f sec" % (cnt2, t2 - t1))
      cnt2 += 1

def cam_pro_con():
  '''
  - scan: poll or trigger?
  - queue: memcpy image or integer
  - compress: jpeg or png?
  '''
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)
  t = Thread(target=cam_save_con)
  t.daemon = True
  t.start()
  t1 = time.time()
  for i in range(LOOP_CSIZE):
    cam_read_pro(cam)
  t.join()
  print("stm total: %f sec" % (time.time() - t1))

def cam_read_mcp(cam):
  global cnt
  if not que.full():
    t1 = time.time(); # print("read() start   %d: %f sec" % (cnt, t1 - t))
    _, img = cam.read()
    _, img = cv2.imencode(".jpg", img)
    que.put(img)
    t2 = time.time(); # print("read() end     %d: %f sec" % (cnt, t2 - t))
    print("read() elapsed %d: %f sec" % (cnt, t2 - t1))
    cnt += 1
  else:
    time.sleep(1)
    cam_read_mcp(cam)

def cam_save_mcp():
  global cnt2
  while cnt2 < LOOP_CSIZE:
    if not que.empty():
      t1 = time.time(); # print("save() start   %d: %f sec" % (cnt2, t1 - t))
      img = que.get()
      img = cv2.imdecode(np.fromstring(img, dtype=np.uint8), cv2.IMREAD_COLOR)
      cv2.imwrite(path + str(cnt2) + '.png', img)
      t2 = time.time(); # print("save() end     %d: %f sec" % (cnt2, t2 - t))
      print("save() elapsed %d: %f sec" % (cnt2, t2 - t1))
      cnt2 += 1

def mcp_main():
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)
  t = Thread(target=cam_save_mcp)
  t.daemon = True
  t.start()
  t1 = time.time()
  for i in range(LOOP_CSIZE):
    cam_read_mcp(cam)
  t.join()
  print("mcp total: %f sec" % (time.time() - t1))

def stm_video():
  ''' streaming store as video '''
  cam = cv2.VideoCapture(0)  # arg: dev_no
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # arg: encode
  # arg: file, encode, fps, resolution
  cam_out = cv2.VideoWriter(path + 'video.avi', fourcc, VID_FPS, (IMG_WIDTH, IMG_HEIGHT))

  try:
    tmp = BytesIO()  # _io.BytesIO
    for i in range(LOOP_CSIZE):
      _, img = cam.read()  # numpy.ndarray shape of (h, w, 3)
      _, en_img = cv2.imencode(".jpg", img) # numpy.ndarray shape of (n, 1)
      tmp.write(en_img)
      tmp.seek(0)
      de_img = cv2.imdecode(np.fromstring(tmp.read(), dtype=np.uint8), cv2.IMREAD_COLOR)
      tmp.seek(0)
      cam_out.write(de_img)
  except KeyboardInterrupt:
    cam.release()
    cam_out.release()
  cam.release()
  cam_out.release()

def seq_video():
  ''' sequencial store as video '''
  cam = cv2.VideoCapture(0)  # arg: dev_no
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # arg: encode
  # arg: file, encode, fps, resolution
  cam_out = cv2.VideoWriter(path + 'video.avi', fourcc, VID_FPS, (IMG_WIDTH, IMG_HEIGHT))

  try:
    for i in range(LOOP_CSIZE):
      _, img = cam.read()  # numpy.ndarray
      cam_out.write(img)
  except KeyboardInterrupt:
    cam.release()
    cam_out.release()
  cam.release()
  cam_out.release()

if __name__ == '__main__':
  # seq_video()
  # stm_video()
  # asy_image()
  # cam_pro_con()
  # mcp_main()
  pass
