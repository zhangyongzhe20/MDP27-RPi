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
        # first establish
        self.android.connect()
        # second establish
        # third establish
        self.robot.connect_serial()

        print "All end-devices are connected\n"

        # initialize queues
        # self.Aqueue = Queue.Queue(maxsize=0)
        # self.Rqueue = Queue.Queue(maxsize=0)
        # self.Pqueue = Queue.Queue(maxsize=0)
        # initialization done

    # read/write Android
    def readAndroid(self, Pqueue):
        while 1:
            if self.android.bt_is_connect:
                msg = self.android.read()
                if msg:
                    print "Read from BT: %s\n" % msg

    def writeAndroid(self, Aqueue):
        while 1:
            send_msg = raw_input()
            print "Write(): %s " % send_msg
            if send_msg:
              self.android.write(send_msg)
              print "Write to android: %s\n" % msg

    # read/write Robot

    def Mthreads(self):
        try:
            # 1: Read from android
            thread.start_new_thread(self.readAndroid, (self.Pqueue,))
            # 5: Write to Android
            thread.start_new_thread(self.writeAndroid, (self.Aqueue,))

        except Exception, e:
            # print "Error in mode %s: %s" % mode % str(e)
            print "Error in Mthreadings of Exploration %s" % str(e)
        while 1:
            pass


# Driver code
try:
    main = Main()
    main.Mthreads()

except KeyboardInterrupt:
    print "Terminating the main program now..."
