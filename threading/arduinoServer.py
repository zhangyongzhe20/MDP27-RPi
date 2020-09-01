import serial
import time
from config import BAUD as baud, SER_PORT0 as ser_port


__author__ = "Zhang Y.Z."

class arduinoAPI(object):
	def __init__(self):
		self.port = ser_port
		self.baud_rate = baud
		self.ser = None

	def connect_serial(self):
		"""
		Initialize serial socket
		"""
		try:
			self.ser = serial.Serial(self.port, self.baud_rate, timeout=3)
			#time.sleep(1)
			print "Serial link connected"
		except Exception, e:
			# print "Error (Serial): %s " % str(e)
			print "Error: Serial connection not established. Try reconnecting the serial cable and/or restart the pi"


	def close_sr_socket(self):
		if (self.ser):
			self.ser.close()
			print "Closing serial socket"


	def write_to_serial(self, msg):
		"""
		Write to arduino
		"""
		try:
			self.ser.write(msg)
			# print "Write to arduino: %s " % msg
		except AttributeError:
			print "Error in serial comm. No value to be written. Check connection!"

	def read_from_serial(self):
		"""
		Read from arduino

		Waits until data is received from arduino
		"""
		try:
			received_data = self.ser.readline()
			# print "Received from arduino: %s " % received_data
			return received_data
		except AttributeError:
			print "Error in serial comm. No value received. Check connection!"



print "Running Main"
sr = arduinoAPI()
sr.connect_serial()

send_msg = raw_input()
print "Writing [%s] to arduino" % send_msg
sr.write_to_serial(send_msg)

print "read"
print "data received from serial" % sr.read_from_serial

print "closing sockets"
sr.close_sr_socket()

     