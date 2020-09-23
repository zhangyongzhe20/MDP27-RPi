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
        self.bluetooth.connect()
        #self.arduino.connect_serial()

        # initialize queues
        self.queue = Queue.Queue(maxsize=0)

        # initialization done

    # read/write Bluetooth

    def readBluetooth(self, queue):
        while 1:
            msg = self.bluetooth.read()
            queue.put_nowait(msg)
            print "Read from BT: %s\n" % msg

    # read/write Arduino
    def readArduino(self, queue):
        while 1:
            msg = self.arduino.read_from_serial()
            queue.put_nowait(msg)
            print "Read from Arduino: %s\n" % msg

    # read/write Arduino

    def readPC(self, queue):
        while 1:
            msg = self.pc.read_from_PC()
            print "Read from PC: %s\n" % msg
            queue.put_nowait(msg)

    def writeAll(self, queue):
        while 1:
            if not queue.empty():
                msg = queue.get_nowait()
                self.bluetooth.write(msg)
                print "Write to Android: %s\n" % msg

    # Multi-threadings

    def Mthreads(self):
        try:
            # sensor reading msg
            thread.start_new_thread(self.readAndroid, (self.queue,))
            thread.start_new_thread(self.readArduino, (self.queue,))
            thread.start_new_thread(self.readPC, (self.queue,))
            thread.start_new_thread(self.writeAll, (self.queue,))

        except Exception, e:
            print "Error : %s" % str(e)


# Driver code
try:
    main = Main()
    main.Mthreads()

except KeyboardInterrupt:
    print "Terminating the main program now..."
            
    


    



