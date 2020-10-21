import os  # path, dirname, abspath
from threading import Thread
from queue import Queue
import cv2

import logging  # debug, basicConfig
from time import time

QUEUE_CSIZE_CAPACITY = 65536
THREAD_SENTINEL = object()  # terminating flag

DBGP = logging.debug
logging.basicConfig(level=logging.DEBUG)  # comment this line to disable DBGP


class Camera():
  '''
  capture_image(): producer, capture and enqueue image
  save_image(): consumer loop, dequeue image and save
  I/O performance:
    device: Logitech C720
                    platform,      cam.read(),   cam.imwrite()
    res  640 x 480:    Linux,  avg. ~30.0 fps,  avg. ~66.7 fps
    res 1280 x 720:    Linux,  avg. ~ 7.5 fps,  avg. ~28.6 fps
    res  640 x 480:  Windows,  avg. ~33.3 fps,  avg.       fps
    res 1280 x 720:  Windows,  avg. ~33.3 fps,  avg.       fps
  '''

  def __init__(self, dev_no=0, save_dir=None,
               res={'width': 640, 'height': 480}):
    self.dev_no = dev_no
    if save_dir is None:
      self.save_dir = os.path.dirname(os.path.abspath('__file__'))
    else:
      self.save_dir = save_dir
    self.cam = self.new_cam(dev_no, res)
    self.cnt_queue = Queue(QUEUE_CSIZE_CAPACITY)
    self.img_queue = Queue(QUEUE_CSIZE_CAPACITY)
    self.save_thrd = Thread(target=self.save_image,
                            args=(self.img_queue, self.save_dir))
    self.cap_thrd = Thread(target=self.capture_image,
                           args=(self.cam, self.cnt_queue, self.img_queue))
    self.save_thrd.start()
    self.cap_thrd.start()

  @staticmethod
  def new_cam(dev_no, res):
    ''' new object, set resolution and do first read (take longer time)
        Available backends:
        CAP_FFMPEG, CAP_GSTREAMER, CAP_INTEL_MFX, CAP_V4L2, CAP_IMAGES,
        CAP_OPENCV_MJPED
        use CAP_V4L2 on Linux; CAP_DSHOW on Windows '''
    cam = cv2.VideoCapture(dev_no, cv2.CAP_V4L2)  # for Linux platform
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

      t = time()
      img = img_queue.get()

      if img is THREAD_SENTINEL:
        break
      img_count += 1
      file_name = "{}/{:03d}.png".format(save_dir, img_count)
      cv2.imwrite(file_name, img)
      DBGP("  Camera: time(save_image)     {:5.3f} sec"
           .format(time()-t))
      DBGP("  Camera: save_image  file_name: {}".format(file_name))

    DBGP("  Camera: save_imgae terminate")

  @staticmethod
  def capture_image(cam, cnt_queue, img_queue):
    while True:

      t = time()
      cnt = cnt_queue.get()

      if cnt is THREAD_SENTINEL:
        img_queue.put(THREAD_SENTINEL)
        break

      ok, img = cam.read()
      img_queue.put(img)
      DBGP("  Camera: time(capture_image)  {:5.3f} sec".format(time()-t))

  def cap_image(self):
    self.cnt_queue.put(None)

  def close(self):
    self.cnt_queue.put(THREAD_SENTINEL)
    self.del_cam(self.cam)
    self.save_thrd.join()
    self.cap_thrd.join()


def demo_camera(csize=200):
  c = Camera(res={'width': 1280, 'height': 720})
  for i in range(csize):
    c.cap_image()
  c.close()


if __name__ == '__main__':
  demo_camera()
