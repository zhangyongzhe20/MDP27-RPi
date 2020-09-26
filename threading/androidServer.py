from bluetooth import *
from config import RFCOMM_PORT as RFCOMM_PORT, UUID as UUID, ANDROID_SOCKET_BUFFER_SIZE as ANDROID_SOCKET_BUFFER_SIZE

__author__ = 'Zhang Y.Z.'

class AndroidAPI(object):

    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.bt_is_connected = False

    def close_bt_socket(self):
        """
        Close socket connections
        """
        if self.client_socket:
            self.client_socket.close()
            print "Closing client socket"
        if self.server_socket:
            self.server_socket.close()
            print "Closing server socket"
        self.bt_is_connected = False


    def bt_is_connect(self):
        """
        Check status of BT connection
        """
        return self.bt_is_connected


    def connect_bluetooth(self):
        """
        Connect to the Nexus 7 device
        """
        # Creating the server socket and bind to port		
        try:
            self.server_socket = BluetoothSocket( RFCOMM )
            self.server_socket.bind(("", RFCOMM_PORT))
            self.server_socket.listen(RFCOMM_PORT)	# Listen for requests
            self.port = self.server_socket.getsockname()[1]

            advertise_service( self.server_socket, "MDP27Server",
                               service_id = UUID,
                               service_classes = [ UUID, SERIAL_PORT_CLASS ],
                               profiles = [ SERIAL_PORT_PROFILE ]                                )
            print "6"
            print "Waiting for BT connection on RFCOMM channel %d" % self.port
            # Accept requests
            self.client_socket, client_address = self.server_socket.accept()
            print "Accepted connection from ", client_address
            self.bt_is_connected = True

        except Exception, e:
            print "Error: %s" %str(e)
            # self.close_bt_socket()


    def write_to_bt(self, message):
        """
        Write message to Nexus
        """
        try:
            self.client_socket.send(str(message))
        except BluetoothError:
            print "Bluetooth Error. Connection reset by peer"
            self.connect_bluetooth()	# Reestablish connection

            
    def read_from_bt(self):
        """
        Read incoming message from Nexus
        """
        try:
            msg = self.client_socket.recv(2048)
            # print "Received [%s] " % msg
            return msg
        except BluetoothError:
            print "Bluetooth Error. Connection reset by peer. Trying to connect..."
            self.connect_bluetooth()	# Reestablish connection

if __name__ == "__main__":
    print "Running Main"
    bt = AndroidAPI()
    # bt.init_bluetooth()
    bt.connect_bluetooth()
    
    # send_msg = raw_input()
    # print "Write(): %s " % send_msg
    # bt.write_to_bt(send_msg)

    print "read"
    print "data received: %s " % bt.read_from_bt()

    print "closing sockets"
    bt.close_bt_socket()

