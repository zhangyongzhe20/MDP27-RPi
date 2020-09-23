#!/usr/bin/env python2
from arduinoServer import robotAPI
from androidServer2 import androidAPI
from pcServer import pcAPI
from config import *

import Queue
import thread
import threading
import os


class Main:
    def __init__(self):
        # allow rpi bluetooth to be discoverable
        # os.system("sudo hciconfig hci0 piscan")

        # initial connections
        self.bluetooth = androidAPI()
        #self.arduino = robotAPI()
        #self.pc = pcAPI()
        print("Before connect")
        self.bluetooth.connect()

        print("test1")
        #self.arduino.connect_serial()
        self.mode = 0

        # initialize queues
        self.Bqueue = Queue.Queue(maxsize=0)
        self.Aqueue = Queue.Queue(maxsize=0)
        self.Pqueue = Queue.Queue(maxsize=0)

        # initialization done

    # read/write Bluetooth

    def readBluetooth(self, Pqueue):
        while 1:
            msg = self.bluetooth.read()
            Pqueue.put_nowait(msg)
            print "Read from BT: %s\n" % msg

    def writeBluetooth(self, Bqueue):
        while 1:
            if not Bqueue.empty():
                msg = Bqueue.getnowait()
                self.bluetooth.write(msg)
                print "Write to bluetooth: %s\n" % msg

    # read/write Arduino
    def readArduino(self, Pqueue):
        while 1:
            msg = self.arduino.read_from_serial()
            Pqueue.put_nowait(msg)
            print "Read from Arduino: %s\n" % msg

    def writeArduino(self, Aqueue):
        while 1:
            if not Aqueue.empty():
                msg = Aqueue.get_nowait()
                self.arduino.write_to_serial(msg)
                print "Write to Arduino: %s\n" % msg

    # read/write Arduino

    def readPC(self, Aqueue, Bqueue, mode):
        while 1:
            msg = self.pc.read_from_PC()
            print "Read from PC: %s\n" % msg
            # exploration
            if mode == 'e':
                Bqueue.put_nowait(msg)
            # fatest path
            else:
                Aqueue.put_nowait(msg)

    def writePC(self, Pqueue):
        while 1:
            if not Pqueue.empty():
                msg = Pqueue.get_nowait()
                self.pc.write_to_PC(msg)
                print "Write to PC: %s\n" % msg

    # Multi-threadings

    def Mthreads(self, mode):
        if mode == 'e':
            try:
                # sensor reading msg
               thread.start_new_thread(self.readArduino, (self.Pqueue,))
               thread.start_new_thread(self.writePC, (self.Pqueue,))
               # image recognition????????????????
               thread.start_new_thread(
                   self.readPC, (self.Aqueue, self.Bqueue, mode))
               thread.start_new_thread(self.writeBluetooth, (self.Bqueue,))

            except Exception, e:
                print "Error in mode %s: %s" % mode % str(e)

            while 1:
                pass

        else:
            try:
                thread.start_new_thread(self.readBluetooth, (self.Pqueue,))
                thread.start_new_thread(self.writePC, (self.Pqueue,))
                thread.start_new_thread(
                    self.readPC, (self.Aqueue, self.Bqueue, mode))
            except Exception, e:
                print "Error in mode %s: %s" % mode % str(e)

            while 1:
                pass

    def getMode(self):
         # mode = 1 for exploration, mode = 2 for fast
        if self.mode == 0:
            self.msg = self.bluetooth.read()
        if msg:
            Pqueue.put_nowait(msg)
            Aqueue.put_nowait(msg)
        return msg


# Driver code
try:
    main = Main()
    mode = main.getMode()
    while 1:
       
        main.Mthreads(mode)

except KeyboardInterrupt:
    print "Terminating the main program now..."
            
    


    



