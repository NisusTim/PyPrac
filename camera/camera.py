import os  # path, dirname, abspath
from threading import Thread, Condition
from queue import Queue
import cv2

import logging
import time

QUEUE_CSIZE_CAPACITY = 100
COND_MUTEX = Condition()  # condition variable
THREAD_SENTINEL = object()  # terminating flag

DBGP = logging.debug
# logging.basicConfig(level=logging.DEBUG)  # comment this line to disable DBGP


class Camera():
  '''
  capture_image: producer, capture and enqueue image
  save_image: consumer loop, dequeue image and save
  '''

  def __init__(self, dev_no=0, save_dir=None,
               res={'width': 1280, 'height': 720}):
    self.dev_no = dev_no
    if save_dir is None:
      self.save_dir = os.path.dirname(os.path.abspath('__file__'))
    self.cam = self.new_cam(dev_no, res)
    self.img_queue = Queue(QUEUE_CSIZE_CAPACITY)
    self.save_thrd = Thread(target=self.save_image,
                            args=(self.img_queue, self.save_dir))
    self.save_thrd.start()

  @staticmethod
  def new_cam(dev_no, res):
    ''' new object, set resolution and do first read (take longer time) '''
    cam = cv2.VideoCapture(dev_no)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, res['width'])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, res['height'])
    DBGP("  Camera: new_cam  device_no: {}  resolution: {} x {}"
         .format(dev_no, res['width'], res['height']))
    cam.read()
    return cam

  @staticmethod
  def del_cam(cam):
    del cam
    DBGP("  Camera: del_cam")

  @staticmethod
  def save_image(img_queue, save_dir):
    img_count = 0

    while True:

      COND_MUTEX.acquire()
      while img_queue.empty():
        COND_MUTEX.wait()
      t = time.time()
      img = img_queue.get()
      COND_MUTEX.release()

      if img is THREAD_SENTINEL:
        break
      img_count += 1
      file_name = "{}/{:03d}.jpg".format(save_dir, img_count)
      cv2.imwrite(file_name, img)
      DBGP("  Camera: time(save_image)     {:5.3f} sec"
           .format(time.time()-t))
      DBGP("  Camera: save_image  file_name: {}".format(file_name))
    DBGP("  Camera: save_imgae terminate")

  @staticmethod
  def capture_image(cam, img_queue):
    ''' to do: without queue.full() handle '''
    COND_MUTEX.acquire()
    t = time.time()
    ok, img = cam.read()
    img_queue.put(img)
    COND_MUTEX.notify()
    COND_MUTEX.release()
    DBGP("  Camera: time(capture_image)  {:5.3f} sec".format(time.time()-t))
    DBGP("  Camera: capture_image...")

#     if not img_queue.full():
#       t = time.time()
#       ok, img = cam.read()
#       if not ok:
#         return

  def cap_image(self):
    self.capture_image(self.cam, self.img_queue)

  def close(self):
    self.img_queue.put(THREAD_SENTINEL)
    self.del_cam(self.cam)
    self.save_thrd.join()


def demo_camera(csize=QUEUE_CSIZE_CAPACITY):
  c = Camera()
  for i in range(csize):
    c.cap_image()
  c.close()


if __name__ == '__main__':
  demo_camera()
