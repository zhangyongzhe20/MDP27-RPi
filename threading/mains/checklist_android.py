from androidServer import androidAPI
from config import *

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

        print "Android connected\n"


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
            
            if send_msg:
              self.android.write(send_msg)
              print "Write to android: %s\n" % send_msg

    # read/write Robot

    def Mthreads(self):
        try:
            # 1: Read from android
            thread.start_new_thread(self.readAndroid)
            # 5: Write to Android
            thread.start_new_thread(self.writeAndroid)

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
