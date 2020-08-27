import time
import threading
import queue

class Worker(threading.Thread):
  def __init__(self, queue, num, semaphore):
    threading.Thread.__init__(self)
    self.queue = queue
    self.num = num
    self.semaphore = semaphore

  def run(self):
    while self.queue.qsize() > 0:
      msg = self.queue.get()
      self.semaphore.acquire()
      print("Semaphore acquired by Worker %d" % self.num)
      print("Worker %d: %s" % (self.num, msg))
      time.sleep(1)
      print("Semaphore released by Worker %d" %self.num)
      self.semaphore.release()

if __name__ == '__main__':
  que = queue.Queue()
  for i in range(5):
    que.put("Data %d" % i)
  sem = threading.Semaphore(2)
  worker_1 = Worker(que, 1, sem)
  worker_2 = Worker(que, 2, sem)
  worker_3 = Worker(que, 3, sem)
  worker_1.start()
  worker_2.start()
  worker_3.start()
  worker_1.join()
  worker_2.join()
  worker_3.join()
  print("Done.")
