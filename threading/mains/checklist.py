#!/usr/bin/env python2
from arduinoServer import robotAPI
from androidServer import androidAPI
from pcServer import pcAPI
from config import *

import Queue
import thread
import threading
import os
import time

__author__ = "Zhang Y.Z."
class Main:
    def __init__(self):
        # allow rpi android to be discoverable
        # os.system("sudo hciconfig hci0 piscan")
        # initial connections
        self.android = androidAPI()
        self.robot = robotAPI()
        self.pc = pcAPI()
        self.pc.init_pc_comm()
        self.android.connect()
        self.robot.connect_serial()
        
        # initialize queues
        self.Aqueue = Queue.Queue(maxsize=0)
        self.Rqueue = Queue.Queue(maxsize=0)
        self.Pqueue = Queue.Queue(maxsize=0)
        # initialization done

    # read/write Android
    def readAndroid(self, Rqueue):
        while 1:
            msg = self.android.read()
            Rqueue.put_nowait(msg)
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
        while 1:
            msg = self.pc.read_from_PC()
            if msg:
                destination = msg[0]
                dataBody = msg[1:]
                print "Read from PC: %s\n" % msg
                if destination == 'a':
                   Aqueue.put_nowait(dataBody)
                 # fatest path
                elif destination == 'r':
                   Rqueue.put_nowait(dataBody)
                else:
                   print "unknown destination for pc message"
        print "readPC is called"


    def writePC(self, Pqueue):
        while 1:
            if not Pqueue.empty():
                msg = Pqueue.get_nowait()
                if msg:
                   self.pc.write_to_PC(msg)
                   print "Write to PC: %s\n" % msg

    def Mthreads(self, mode):
        if mode == 'e':
            try:
                # 1: Read from android
               thread.start_new_thread(self.readAndroid, (self.Rqueue,))
                # 4: Write to Robot
               thread.start_new_thread(self.writeRobot,(self.Rqueue,))
                # 6: Read from Arduino
               thread.start_new_thread(self.readRobot,(self.Pqueue,))
                # 2: Write to PC
               thread.start_new_thread(self.writePC,(Pqueue,))
            #     # 3: Read from PC
            #    thread.start_new_thread(self.readPC, (self.Rqueue, self.Aqueue, ))
            #     # 5: Write to Android
            #    thread.start_new_thread(self.writeAndroid,(self.Aqueue,))


            except Exception, e:
                # print "Error in mode %s: %s" % mode % str(e)
                print "Error in Mthreading"

            while 1:
                pass

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
    main.Mthreads('e')

except KeyboardInterrupt:
    print "Terminating the main program now..."
            
    


    


