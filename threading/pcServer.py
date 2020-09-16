#!/usr/bin/env python2
import socket
import sys
from config import WIFI_IP as ip, WIFI_PORT as port

__author__ = "Zhang Y.Z."

class pcAPI(object):

    def __init__(self):
        self.tcp_ip = ip
        self.port = port
        self.conn = None
        self.client = None
        self.addr = None
        self.pc_is_connect = False

    def close_pc_socket(self):
        """
        Close socket connections
        """
        if self.conn:
            self.conn.close()
            print "Closing server socket"
        if self.client:
            self.client.close()
            print "Closing client socket"
        self.pc_is_connect = False

    def pc_is_connected(self):
        """
        Check status of connection to PC
        """
        return self.pc_is_connect

    def init_pc_comm(self):
        """
        Initiate PC connection over TCP
        """
        # Create a TCP/IP socket
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.bind((self.tcp_ip, self.port))
            self.conn.listen(1)		#Listen for incoming connections
            print "Listening for incoming connections from PC..."
            self.client, self.addr = self.conn.accept()
            print "Connected! Connection address: ", self.addr
            self.pc_is_connect = True
        except Exception, e: 	#socket.error:
            print "Error: %s" % str(e)
            print "Try again in a few seconds"


    def write_to_PC(self, message):
        """
        Write message to PC
        """
        try:
            self.client.sendto(message, self.addr)
        except TypeError:
            print "Error: Null value cannot be sent"


    def read_from_PC(self):
        """
        Read incoming message from PC
        """
        try:
            data = self.client.recv(1024)
            # print "Read [%s] from PC" %pc_data
            # pc_data = self.client.sendall(data)
            return data
        except Exception, e:
            print "Error: %s " % str(e)
            print "Value not read from PC"

## Driver code
pc = pcAPI()
pc.init_pc_comm()
# while True:
#    data = raw_input()
#    print "Write to PC(): %s " % data
#    pc.write_to_PC(data)

while pc.pc_is_connected():
    data = pc.read_from_PC()
    if data:
    #    break
        print "Read from PC: %s " % data


## some occasion need to close
pc.close_pc_socket()


# msg = pc.read_from_PC()
# print "data received: %s " % msg