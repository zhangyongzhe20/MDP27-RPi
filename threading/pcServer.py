#!/usr/bin/env python2
import socket
import sys
from config import WIFI_IP as ip, WIFI_PORT as port, Client_IP as clientIP, Client_PORT as clientPort

__author__ = "Zhang Y.Z."

class pcAPI(object):

    def __init__(self):
        self.tcp_ip = ip
        self.port = port
        self.conn = None
        self.client = clientIP
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
            print "Sent [%s] to PC [%s]" % message % addr
        except TypeError:
            print "Error: Null value cannot be sent"


    def read_from_PC(self):
        """
        Read incoming message from PC
        """
        try:
            pc_data = self.client.recv(2048)
            # print "Read [%s] from PC" %pc_data
            return pc_data
        except Exception, e:
            print "Error: %s " % str(e)
            print "Value not read from PC"

# if __name__ == "__main__":
# 	print "main" 
pc = pcAPI()
pc.init_pc_comm()
flag = True
# while(flag):
#     msg = pc.read_from_PC()
#     print "data received: %s" %msg
#     send_msg = "From RPi To Pc"
#     pc.write_to_PC(send_msg)
#     # if "done" in msg:
#     #     pc.close_pc_socket()
#     #     break
while True:
   send_msg = raw_input()
   print "write_to_PC(): %s " % send_msg
   pc.write_to_PC(send_msg)

   msg = pc.read_from_PC()
   print "data received: %s " % msg

print "closing sockets"
pc.close_pc_socket()