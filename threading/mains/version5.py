#!/usr/bin/env python2

# second way of I.R.  Deep learning
from arduinoServer import robotAPI
from androidServer import androidAPI
from pcServer import pcAPI
from config import *
from picamera import PiCamera
from picamera.array import PiRGBArray
import Queue
import thread
import threading
import os
import time
import datetime
from imgrec_final import img_rec

__author__ = "Zhang Y.Z."


class Main:
    def __init__(self):
        # allow rpi android to be discoverable
        # os.system("sudo hciconfig hci0 piscan")
        # initial connections
        self.android = androidAPI()
        self.robot = robotAPI()
        self.pc = pcAPI()
        # first establish
        self.android.connect()
        # second establish
        self.pc.init_pc_comm()
        # third establish
        self.robot.connect_serial()

        print "All end-devices are connected\n"

        # initialize queues
        self.Aqueue = Queue.Queue(maxsize=0)
        self.Rqueue = Queue.Queue(maxsize=0)
        self.Pqueue = Queue.Queue(maxsize=0)
        # initialization done

        # Label lists
        self.labels = []

    # read/write Android
    def readAndroid(self, Pqueue):
        while 1:
            if self.android.bt_is_connect:
                msg = self.android.read()
                if msg:
                    Pqueue.put_nowait(msg)
                    print "Read from BT: %s\n" % msg

    def writeAndroid(self, Aqueue):
        while 1:
            if not Aqueue.empty():
                msg = Aqueue.get_nowait()
                self.android.write(msg)
                print "Write to android: %s\n" % msg

    # read/write Robot
    def readRobot(self, Pqueue):
        while 1:
            if self.robot.is_arduino_connected:
                msg = self.robot.read_from_serial()
                if msg[0] != 'd':
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
            if self.pc.pc_is_connected:
                msg = self.pc.read_from_PC()
                if msg:
                    destination = msg[0]
                    dataBody = msg[1:]
                    print "Read from PC: %s\n" % msg
                    ##send to android
                    if destination == 'a':
                        Aqueue.put_nowait(dataBody)
                    ##send to robot
                    elif destination == 'r':
                        Rqueue.put_nowait(dataBody)
                    ##trigger camera       
                    elif destination == 'c':
                        try:
                           label = img_rec()
                        except:
                            label = -1
                        if label not in self.labels:
                            self.labels.append(label)
                            Pqueue.put_nowait("%s" %label)
                        else:
                            Pqueue.put_nowait("-1")
                    else:
                        print "unknown destination for pc message"

    def readRobot2(self, Pqueue):
     while 1:
          msg =  raw_input()         
          #msg = self.robot.read_from_serial()
          Pqueue.put_nowait(msg)
          print "Read from Robot: %s\n" % msg

    def writePC(self, Pqueue):
        while 1:
            if not Pqueue.empty():
                msg = Pqueue.get_nowait()
                if msg:
                    self.pc.write_to_PC(msg + "\n")
                    print "Write to PC: %s\n" % msg


    def take_pic(self):
        start_time = datetime.now()
        try:
            # initialize the camera and grab a reference to the raw camera capture
            camera = PiCamera(resolution=(IMAGE_WIDTH, IMAGE_HEIGHT))  # '1920x1080'
            rawCapture = PiRGBArray(camera)
            
            # allow the camera to warmup
            time.sleep(0.1)
            
            # grab an image from the camera
            camera.capture(rawCapture, format=IMAGE_FORMAT)
            image = rawCapture.array
            camera.close()

            print('Time taken to take picture: ' + str(datetime.now() - start_time) + 'seconds')
            
            # to gather training images
            # os.system("raspistill -o images/test"+
            # str(start_time.strftime("%d%m%H%M%S"))+".png -w 1920 -h 1080 -q 100")
        
        except Exception as error:
            print('Taking picture failed: ' + str(error))
        
        return image
    

    def Mthreads(self):
        try:
            # 1: Read from android
            thread.start_new_thread(self.readAndroid, (self.Pqueue,))
            # 2: Write to PC
            thread.start_new_thread(self.writePC, (self.Pqueue,))
            # 3: Read from PC
            thread.start_new_thread(self.readPC, (self.Rqueue, self.Aqueue, ))
            # 4: Write to Robot
            thread.start_new_thread(self.writeRobot, (self.Rqueue,))
            # 5: Write to Android
            thread.start_new_thread(self.writeAndroid, (self.Aqueue,))
            # 6: Read from Arduino
            thread.start_new_thread(self.readRobot, (self.Pqueue,))

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