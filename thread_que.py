import threading
import time
import queue

class Worker(threading.Thread):
  def __init__(self, queue, num):
    threading.Thread.__init__(self)
    self.queue = queue
    self.num = num
  
  def run(self):
    while self.queue.qsize() > 0:
      msg = self.queue.get()
      print("Workter %d: %s" % self.num, msg)
      time.sleep(1)
      time.slepp(a)

if __name__ == '__main__':
  que = queue.Queue()
  for i in range(10):
    que.put("Data %d" % i)
  worker_1 = Worker(que, 1)
  worker_2 = Worker(que, 2)
  worker_1.start()
  worker_2.start()
  worker_1.join()
  worker_2.join()
  print("Done.")
