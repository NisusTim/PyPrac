# Ref: https://blog.gtwang.org/programming/python-threading-multithreaded-programming-tutorial/
import threading
import time

def job():
  for i in range(5):
    print("Child thread:", i)
    time.sleep(1)

if __name__ == '__main__':
  thrd = threading.Thread(target=job)
  thrd.start()
  for i in range(3):
    print("Main thread:", i)
    time.sleep(1)
  thrd.join()
  print("Done.")
