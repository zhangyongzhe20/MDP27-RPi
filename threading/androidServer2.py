import bluetooth as bt
from config import RFCOMM_CHANNEL as RFCOMM_CHANNEL, UUID as UUID, ANDROID_SOCKET_BUFFER_SIZE as ANDROID_SOCKET_BUFFER_SIZE

__author__ = 'Zhang Y.Z.'

class androidAPI(object):
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.bt_is_connected = False
        self.server_socket = bt.BluetoothSocket(bt.RFCOMM)
        self.server_socket.bind(("", RFCOMM_CHANNEL))
        self.server_socket.listen(RFCOMM_CHANNEL)  # Listen for requests
        self.port = self.server_socket.getsockname()[1]

        print('server socket:', str(self.server_socket))

    def disconnect(self):
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

    def isConnected(self):
        return self.bt_is_connected

    def connect(self):
        # Creating the server socket and bind to port
        # try:
        #     self.server_socket = bt.BluetoothSocket(bt.RFCOMM)
        #     self.server_socket.bind(("", RFCOMM_CHANNEL))
        #     self.server_socket.listen(RFCOMM_CHANNEL)  # Listen for requests
        #     self.port = self.server_socket.getsockname()[1]

        #     # bt.advertise_service(self.server_socket, "SampleServer",
        #     #                      service_id=UUID,
        #     #                      service_classes=[UUID, bt.SERIAL_PORT_CLASS],
        #     #                      profiles=[bt.SERIAL_PORT_PROFILE],
        #     #                      )
        #     print "Waiting for BT connection on RFCOMM channel %d" % self.port
        #     # Accept requests
        #     self.client_socket, client_address = self.server_socket.accept()
        #     print "Accepted connection from ", client_address
        #     self.bt_is_connected = True

        # except Exception, e:
        #     print "Error: %s" % str(e)
        #     # self.close_bt_socket()
        while True:
            retry = False

            try:
                print('Establishing connection with Android...')

                if self.client_socket is None:
                    self.client_socket, address = self.server_socket.accept()
                    self.isConnect = True
                    print("Successfully connected to Android at: " + str(address))
                    retry = False

            except Exception as error:	
                print("Connection with Android failed: " + str(error))

                if self.client_socket is not None:
                    self.client_socket.close()
                    self.client_socket = None
                
                retry = True

            if not retry:
                break

            print('Retrying Bluetooth Connection to Android...')

    def write(self, message):
        """
        Write message to Nexus
        """
        try:
            self.client_socket.send(str(message))
        except bt.BluetoothError:
            print "Bluetooth Error. Connection reset by peer"
            self.connect()  # Reestablish connection

    def read(self):
        """
        Read incoming message from Nexus
        """
        try:
            if self.client_socket != None:
                msg = self.client_socket.recv(2048)
                # print "Received [%s] " % msg
                return msg
        except bt.BluetoothError:
            print "Bluetooth Error. Connection reset by peer. Trying to connect..."
            self.connect()  # Reestablish connection

if __name__ == "__main__":
	print "Running Main"
	an = androidAPI()
	an.connect()

	send_msg = raw_input()
	print "Write(): %s " % send_msg
	an.write(send_msg)

	print "read"
	print "data received: %s " % an.read()

	print "closing sockets"
	an.disconnect()
