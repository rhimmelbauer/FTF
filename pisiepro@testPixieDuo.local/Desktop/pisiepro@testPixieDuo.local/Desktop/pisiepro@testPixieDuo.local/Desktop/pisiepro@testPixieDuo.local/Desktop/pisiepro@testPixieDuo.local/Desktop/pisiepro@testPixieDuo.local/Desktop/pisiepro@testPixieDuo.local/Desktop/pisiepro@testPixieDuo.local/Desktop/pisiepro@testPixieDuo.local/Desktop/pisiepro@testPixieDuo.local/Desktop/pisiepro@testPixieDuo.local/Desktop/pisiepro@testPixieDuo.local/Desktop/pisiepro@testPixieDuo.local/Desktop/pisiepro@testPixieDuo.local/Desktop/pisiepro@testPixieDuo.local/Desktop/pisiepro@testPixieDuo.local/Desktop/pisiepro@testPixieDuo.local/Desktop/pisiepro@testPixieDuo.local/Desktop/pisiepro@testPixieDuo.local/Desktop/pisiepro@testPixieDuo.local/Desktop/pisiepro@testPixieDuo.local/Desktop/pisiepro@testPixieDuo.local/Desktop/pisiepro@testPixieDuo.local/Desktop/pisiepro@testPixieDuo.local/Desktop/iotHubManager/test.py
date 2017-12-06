import iotHubManager as ihm
import time, json


data = {
                "deviceId" : "PixiePro",
                "data" : "Hello IoT Hub from PixiePro!",
                "otherData" : "12345"
    }
message = json.dumps(data)

with open("/home/pixiepro/Desktop/keys/deviceKeys.txt","r") as f:
    credentials = json.load(f)
    f.close()

m = ihm.IoTHubManager(credentials)
m.send_message(message)

status = m.get_status()
print status
while 'IDLE' not in str(status):
    status = m.get_status()
    time.sleep(0.1)

print ("Send status: %s" % status)
