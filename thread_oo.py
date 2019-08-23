import threading
import time

class MyThread(threading.Thread):
  def __init__(self, num):
    threading.Thread.__init__(self)
    self.num = num
  
  def run(self):
    print("Thread", self.num)
    time.sleep(1)

if __name__ == '__main__':
  thrds = []
  for i in range(5):
    thrds.append(MyThread(i))
    thrds[i].start()
  for i in range(5):
    thrds[i].join()
  print("Done.")
