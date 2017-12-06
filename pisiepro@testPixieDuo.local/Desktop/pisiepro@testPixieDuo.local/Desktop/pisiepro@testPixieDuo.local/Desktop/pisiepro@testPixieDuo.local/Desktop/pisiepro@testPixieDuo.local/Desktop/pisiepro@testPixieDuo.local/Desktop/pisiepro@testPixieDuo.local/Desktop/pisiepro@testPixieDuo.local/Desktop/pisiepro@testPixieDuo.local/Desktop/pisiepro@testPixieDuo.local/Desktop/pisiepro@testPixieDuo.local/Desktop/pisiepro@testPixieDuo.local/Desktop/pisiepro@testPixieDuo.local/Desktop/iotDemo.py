import imp, json,cv2,os
import sys, threading, Queue, time
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

fd = imp.load_source('FaceDetector','faceDetector/FaceDetector.py')
am = imp.load_source('AzureCognitiveManager','azureCogServManager/AzureCognitiveManager.py')
iot = imp.load_source('iotHubManager','iotHubManager/iotHubManager.py')
ws = imp.load_source('server','WebsocketServer/server.py')

weightsPath =  "/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/weights.txt"
capturePath = "/home/pixiepro/Desktop/ftf-iot-demo/faceDetector/img.jpg"
azureKeys = "/home/pixiepro/Desktop/keys/azureKeys.txt"
deviceKeys = "/home/pixiepro/Desktop/keys/deviceKeys.txt"

class Face():
    def _init__():
        self._faceAttr = None
        self._emotion = None
        self._faceId = ""

def initObjects():
    faceDetector = fd.FaceDetector(weightsPath,
                                                           capturePath)
    with open(azureKeys,"r") as f:
        sub = json.load(f)
        f.close() 
    azureCognitive = am.AzureCognitiveManager(sub)

    with open(deviceKeys,"r") as f:
        credentials = json.load(f)
        f.close()
    iotHub = iot.IoTHubManager(credentials)

    face = Face()
    return faceDetector, azureCognitive, iotHub,face


def startWebsocketServer():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8001")
    factory.protocol = ws.MyServerProtocol

    q = Queue.Queue()
    r = Queue.Queue()
    ws.MyServerProtocol.setQueue(q,r)

    reactor.listenTCP(8001, factory)
    t = threading.Thread(target = reactor.run, kwargs = {'installSignalHandlers':0})
    t.start()
    return q,r

def pollMsg():
    while q.empty():
        pass
    return q.get()

def startGame(msg):
    faceDetector.resetAttr()
    t = threading.Thread(target=faceDetector.detectFace)
    t.start()

    while not faceDetector._faceDetected: pass
    face._faceAttr, tempFaceId = azureCognitive.getFaceAttr(capturePath)
    similar = azureCognitive.findSimilar(tempFaceId)
    if similar:
        face._faceId= similar['faceId']
        print "Hello again!"
    else:
        face._faceId = tempFaceId
        with open("azureCogServManager/faceids.txt","a") as f:
            f.write(face._faceId+'\n')
            f.close()
        print "Hi, new person!"
    r.put("Start")

def stopGame(msg):
    print "STOP GAME!"
    faceDetector.stop()
    time.sleep(1)
    face._emotion = azureCognitive.getEmotion(capturePath)
    activity = encodeActivity(msg,face)

    print 'Message:' + json.dumps(activity)
    iotHub.send_message(json.dumps(activity))


##    while True:
##        print 'Message:' + json.dumps(activity)
##        iotHub.send_message(json.dumps(activity))
##        time.sleep(3)

def pollResponse(msg):
    pass


def encodeActivity(msg,face):
    activity = dict()
    activity['deviceId'] = iotHub._deviceId
    activity['date'] = msg['date']
    activity['score'] = msg['score']

    activity['gender'] = face._faceAttr['gender']
    activity['age'] = face._faceAttr['age']
    activity['glasses'] = face._faceAttr['glasses']
    activity['emotion'] = face._emotion
    activity['faceId'] = face._faceId

    activity['smile'] = faceDetector._smileDetected

    return activity

    
commands = {
        "stopGame" : stopGame,
        "startGame" : startGame,
        "pollResponse": pollResponse
        }

def decodeMsg(msg):
    try:
        print "received %s" % msg['cmd']
        commands[msg['cmd']](msg)
    except KeyError:
        print "Oops! Unknown command!"
    except Exception as e:
        print "Oops! Unexpected error!" + str(e)
    
faceDetector = None
azureCognitive = None
iotHub = None
face = None


if __name__== "__main__":
    faceDetector, azureCognitive, iotHub, face = initObjects()
    q,r = startWebsocketServer()

    while True:
        msg = json.loads(pollMsg())
        decodeMsg(msg)
