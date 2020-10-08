# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 09:27:43 2019

@author: erichu
"""

import threading
import queue as Queue
import cv2


class pngsave(threading.Thread):
    def __init__(self, t_name, cam_done, quque):
        threading.Thread.__init__(self,name=t_name)
        self.done = cam_done
        self.data = quque
    def run(self):
        while 1:
            try:
                cam_data = self.data.get(True, 1)
                if cam_data:
                    cv2.imwrite(cam_data[1]+".png", cam_data[0])
                    print(cam_data[1]+".png")
            except:
                if self.done[0]:
                    print(f'%s : closed!' % self.getName())
                    break

class picture():
    done = False
    thread = None
    cap = None
    path_name = None
    dev = 0
    # evt = None
    cam_done = [False]
    cam_ret = None
    cam_frame = None
    cam_frame_queue = None

    def __init__(self, dev=0, pn=None):
        self.dev = dev
        # self.evt = threading.Event()
        self.thread = threading.Thread(target=self.cap_thread, args=())
        self.stream = cv2.VideoCapture(self.dev)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cam_ret, self.cam_frame = self.stream.read()
        self.path_name = pn
        self.cam_frame_queue = Queue.Queue()
        self.gngSave = pngsave('Save_PNG', self.cam_done, self.cam_frame_queue)
        self.gngSave.start()
        self.thread.start()
        # sleep(0.1)

    def cap_thread(self):
        print("cam: thread start")
        while True:
            if self.done:
                return
            self.cam_ret, self.cam_frame = self.stream.read()
            # self.evt.wait()
            # self.evt.clear()

        self.cap.release()
        self.cap = None
        print("cam: thread done")
        return

    def take(self, pn=None):
        # print(f"cam:{pn}")
        tmep_list = [self.cam_frame, pn]
        self.cam_frame_queue.put(tmep_list)
        # self.evt.set()
        return

    def cls(self):
        if self.thread:
            self.done = True
            # self.evt.set()
            self.thread.join()
            self.thread = None
            # self.evt = None
        if self.gngSave:
            self.cam_done[0] = True
            self.gngSave.join()
        print("cam: closed!")
        return
