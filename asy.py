import asyncio
import cv2
import time
import os

path = os.path.dirname(os.path.abspath(__file__))
path = path + '/test'
cnt = 0
cnt2 = 0
t = time.time()

async def cam_read(cam):
  global cnt
  print("read() start %d: %f sec" % (cnt, time.time() - t))
  r, f = cam.read()
  print("read() end   %d: %f sec" % (cnt, time.time() - t))
  cnt += 1
  return f

async def cam_save(cam, frame):
  global cnt2
  # cv2.imwrite(path + time.strftime("%m%d_%H%M%S") + str(cnt) + '.png', frame)
  print("save() start %d: %f sec" % (cnt2, time.time() - t))
  cv2.imwrite(path + str(cnt2) + '.png', frame)
  print("save() end   %d: %f sec" % (cnt2, time.time() - t))
  cnt2 += 1

async def cam_chain(cam):
  f = await cam_read(cam)
  await cam_save(cam, f)

def main():
  cam = cv2.VideoCapture(0)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
  loop = asyncio.get_event_loop()
  tasks = [loop.create_task(cam_chain(cam)) for i in range(10)]
  loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
  main()

