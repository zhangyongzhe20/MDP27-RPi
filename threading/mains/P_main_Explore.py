#!/usr/bin/env python2
from pcServer import pcAPI
from config import *
from imgrec import image_rec
import Queue
import thread
import threading
import os
import time

__author__ = "Zhang Y.Z."


class Main:
    def __init__(self):
        self.pc = pcAPI()
        self.pc.init_pc_comm()

        # initialize queues
        self.Aqueue = Queue.Queue(maxsize=0)
        self.Rqueue = Queue.Queue(maxsize=0)
        self.Pqueue = Queue.Queue(maxsize=0)
        # initialization done

    # read/write Android
    def readAndroid(self, Pqueue):
        while 1:
            msg = self.android.read()
            Pqueue.put_nowait(msg)
            print "Read from BT: %s\n" % msg
            f.write("Read from BT: %s\n" % msg)

    def writeAndroid(self, Aqueue):
        while 1:
            if not Aqueue.empty():
                msg = Aqueue.getnowait()
                self.android.write(msg)
                print "Write to android: %s\n" % msg
                f.write("Write to android: %s\n" % msg)

    # read/write Robot
    def readRobot(self, Pqueue):
        while 1:
            msg = self.robot.read_from_serial()
            Pqueue.put_nowait(msg)
            print "Read from Robot: %s\n" % msg
            f.write("Read from Robot: %s\n" % msg)

    def writeRobot(self, Rqueue):
        while 1:
            if not Rqueue.empty():
                msg = Rqueue.get_nowait()
                self.robot.write_to_serial(msg)
                print "Write to Robot: %s\n" % msg
                f.write("Write to Robot: %s\n" % msg)
    # read/write Robot

    def readPC(self, Rqueue, Aqueue, Pqueue):
        while 1:
            msg = self.pc.read_from_PC()
            if msg:
                destination = msg[0]
                dataBody = msg[1:]
                print "Read from PC: %s\n" % msg
                f.write("Read from PC: %s\n" % msg)
                if destination == 'a':
                    Aqueue.put_nowait(dataBody)
                  # fatest path
                elif destination == 'r':
                    Rqueue.put_nowait(dataBody)
                    # trigger camera
                elif destination == 'c':
                    label = image_rec()
                    Pqueue.put_nowait("c%s" % label)
                else:
                    print "unknown destination for pc message"

    def writePC2(self):
        while 1:
            msg = raw_input("write to pc:\n")
            self.pc.write_to_PC(msg + "\n")
            # print "Write to PC: %s\n" % msg
            f.write("Write to PC: %s\n" % msg)

    def Mthreads(self, mode):
        if mode == 'e':
            try:
                # PC responds to init command
                thread.start_new_thread(
                    self.readPC, (self.Rqueue, self.Aqueue, self.Pqueue,))
            #    thread.start_new_thread(self.readRobot,(self.Pqueue,))
            #     explore path msg
            #    thread.start_new_thread(self.writeRobot,(self.Rqueue,))
            #     # sensor reading msg
                thread.start_new_thread(self.writePC2, ())
                thread.start_new_thread(self.writePC,(self.Pqueue,))
                # map info
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
    f = open('output.txt', 'w+')
    main.Mthreads('e')

except KeyboardInterrupt:
    print "Terminating the main program now..."
