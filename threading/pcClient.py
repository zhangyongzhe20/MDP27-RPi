#!/usr/bin/env python2
import socket
from config import WIFI_IP as serverIP, WIFI_PORT as serverPort

__author__ = "Zhang Y.Z."


HOST = serverIP  # The server's hostname or IP address
PORT = serverPort        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Hello, world')
#used to  terminate transmission
#s.sendall(b'done')
data = s.recv(1024)

print'Received %s' %repr(data)
