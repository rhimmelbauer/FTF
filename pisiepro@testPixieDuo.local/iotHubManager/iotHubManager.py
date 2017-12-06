import time, sys, json,unicodedata,random
import iothub_client
from iothub_client import *

receiveContext = 0
avgWindSpeed = 20.0
message_count = 0
received_count = 0

# global counters
receive_callbacks = 0
send_callbacks = 0

# transport protocol
Protocol = IoTHubTransportProvider.AMQP


class IoTHubManager:
    # String containing Hostname, Device Id & Device Key in the format:    
    _connectionString = 'HostName=FTF-Pixie-Demo.azure-devices.net;DeviceId=%s;SharedAccessKey=%s'

    def __init__(self, credentials):
        self._iothub_client_init(credentials)
        self._deviceId = credentials['deviceId']
    
    def _iothub_client_init(self,credentials):
        deviceConnStr = str(self._connectionString % (credentials['deviceId'], credentials['deviceKey']))
        self._iotHubClient = IoTHubClient(deviceConnStr,Protocol)
        self._iotHubClient.set_message_callback(receive_message_callback, receiveContext)

    def send_message(self,msg):
        try:
            message=IoTHubMessage(bytearray(msg,'utf8'))
            self._iotHubClient.send_event_async(
                message, send_confirmation_callback, message_count)
        except:
            print "unexpected error"

    def get_status(self):
        return self._iotHubClient.get_send_status()

def send_confirmation_callback(message, result, userContext):   
    global send_callbacks
    print ("Confirmation[%d] received for message with result = %s" % (userContext, result))
    mapProperties = message.properties()
    keyValuePair = mapProperties.get_internals()
    send_callbacks += 1

def receive_message_callback(self,message, counter):
    buffer = message.get_bytearray()
    size = len(buffer)
    print ("Received Message [%d]:" % counter)
    print ("    Data: <<<%s>>> & Size=%d" % (buffer[:size].decode('utf-8') , size))
    mapProperties = message.properties()
    keyValuePair = mapProperties.get_internals()
    print ("    Properties: %s" % keyValuePair)
    counter += 1
    receive_callbacks += 1
    print ("    Total calls received: %d" % receive_callbacks)
    return IoTHubMessageDispositionResult.ACCEPTED

