import threading
import time

def job(num):
  for i in range(3):
    print("Thread {}-{}".format(num, i))
    time.sleep(1)

if __name__ == '__main__':
  thrds = []
  for i in range(5):
    thrds.append(threading.Thread(target=job, args=(i, )))
    thrds[i].start()
  for i in range(5):
    thrds[i].join()
  print("Done.")
