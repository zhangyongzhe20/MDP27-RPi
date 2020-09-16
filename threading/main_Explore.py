#!/usr/bin/env python2
# from arduinoServer import robotAPI
# from androidServer import androidAPI
from pcServer import pcAPI
from config import *

import Queue
import thread
import threading
import os
import time


class Main:
    def __init__(self):
        # allow rpi android to be discoverable
        # os.system("sudo hciconfig hci0 piscan")

        # initial connections
        #self.android = androidAPI
        # self.robot = robotAPI
        self.pc = pcAPI()
        self.pc.init_pc_comm()
        #self.android.connect()
        ##self.robot.connect()
        ## explore
        self.mode = 'e'

        # initialize queues
        self.Aqueue = Queue.Queue(maxsize=0)
        self.Rqueue = Queue.Queue(maxsize=0)
        self.Pqueue = Queue.Queue(maxsize=0)
        self.Pqueue.put_nowait("msg from another thread")

        # initialization done

    # read/write Android
    def readAndroid(self, Pqueue):
        while 1:
            msg = self.android.read()
            Pqueue.put_nowait(msg)
            print "Read from BT: %s\n" % msg

    def writeAndroid(self, Aqueue):
        while 1:
            if not Aqueue.empty():
                msg = Aqueue.getnowait()
                self.android.write(msg)
                print "Write to android: %s\n" % msg

    # read/write Robot
    def readRobot(self, Pqueue):
        while 1:
            msg = self.robot.read_from_serial()
            Pqueue.put_nowait(msg)
            print "Read from Robot: %s\n" % msg

    def writeRobot(self, Rqueue):
        while 1:
            if not Rqueue.empty():
                msg = Rqueue.get_nowait()
                self.robot.write_to_serial(msg)
                print "Write to Robot: %s\n" % msg

    # read/write Robot

    def readPC(self, Rqueue, Aqueue):
        msg = self.pc.read_from_PC()
        if msg:
            destination = msg[0]
            dataBody = msg[1:]
            print "Read from PC: %s\n" % msg
            if destination == 'a':
                Aqueue.put_nowait(dataBody)
                # fatest path
            else:
                Rqueue.put_nowait(dataBody)

    def writePC(self, Pqueue):
        if not Pqueue.empty():
            msg = Pqueue.get_nowait()
            if msg:
                self.pc.write_to_PC(msg)
                print "Write to PC: %s\n" % msg
    # Multi-threadings

    # Define a function for the thread
    def print_time(self, tName, delay):
       count = 0
       while count < 5:
           time.sleep(delay)
           count += 1
           print "%s: %s" % (tName, time.ctime(time.time()) )

    def Mthreads(self, mode):
        if mode == 'e':
            try:
                # PC responds to init command
               thread.start_new_thread(self.readPC, (self.Rqueue, self.Aqueue, ))
               thread.start_new_thread(self.print_time, ("Thread-1", 2, ))
            #    thread.start_new_thread(self.writePC, (self.Pqueue,))
            #     # sensor reading msg
            #    thread.start_new_thread(self.readRobot, (self.Pqueue,))
            #    thread.start_new_thread(self.writePC, (self.Pqueue,))
            #    # image recognition????????????????
            #    thread.start_new_thread(
            #        self.readPC, (self.Rqueue, self.Aqueue, mode))
            #    thread.start_new_thread(self.writeAndroid, (self.Aqueue,))

            except Exception, e:
                # print "Error in mode %s: %s" % mode % str(e)
                print "Error in Mthreading"

            while 1:
                pass

        # else:
        #     try:
        #         thread.start_new_thread(self.readAndroid, (self.Pqueue,))
        #         thread.start_new_thread(self.writePC, (self.Pqueue,))
        #         thread.start_new_thread(
        #             self.readPC, (self.Rqueue, self.Aqueue, mode))
        #     except Exception, e:
        #         print "Error in mode %s: %s" % mode % str(e)

        #     while 1:
        #         pass


    def getMode(self):
         # default mode is 'explore'
        default = 'e'
        self.msg = self.android.read()
        if msg:
            return msg
        return default


# Driver code
try:

    main = Main()
        ## Android send init command: 'explore' or 'fastest path'
        ##mode = main.getMode()
    mode = 'e'
        ## send 'e' or 'f' to PC
    # if main.pc.pc_is_connected:
    #     print 'write init command %s' %mode
    #     main.pc.write_to_PC(mode)
    if main.pc.pc_is_connected():
        main.Mthreads(mode)
        # print("AQueue: ", main.Aqueue.get_nowait())
        # print("RQueue: ", main.Rqueue.get_nowait())

except KeyboardInterrupt:
    print "Terminating the main program now..."
            
    


    



