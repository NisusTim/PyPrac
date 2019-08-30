import time
import threading
import queue

class Worker(threading.Thread):
  def __init__(self, queue, num, lock):
    threading.Thread.__init__(self)
    self.queue = queue
    self.num = num
    self.lock = lock

  def run(self):
    while self.queue.qsize() > 0:
      msg = self.queue.get()
      self.lock.acquire()
      print("Lock acquired by Worker %d" % self.num)
      print("Worker %d: %s" % (self.num, msg))
      time.sleep(1)
      print("Lock released by Worker %d" % self.num)
      self.lock.release()

if __name__ == '__main__':
  que = queue.Queue()
  for i in range(5):
    que.put("Data %d" % i)
  lock = threading.Lock()
  worker_1 = Worker(que, 1, lock)
  worker_2 = Worker(que, 2, lock)
  worker_1.start()
  worker_2.start()
  worker_1.join()
  worker_2.join()
  print("Done.")
