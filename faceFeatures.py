import imp, json,cv2,os
import sys, threading, time
from multiprocessing import Queue
from avatar.AvatarBuilder import AvatarBuilder
from captureStats.DisplayInfo import DisplayInfo
from captureStats.faceCSVInfoWriter import FaceCSVInfoWriter
import time

weightsPath =  "faceDetector/weights.txt"
capturePath = "faceDetector/img.jpg"
azureKeys = "keys/azureKeys.txt"

fd = imp.load_source('FaceDetector','faceDetector/FaceDetector.py')
am = imp.load_source('AzureCognitiveManager','azureCogServManager/AzureCognitiveManager.py')

lockAzureThread = True

class Face():
    def _init__():
        self._faceAttr = None
        self._emotion = None
        self._faceId = ""
        self.GetAzureData = False

def initObjects():
    faceDetector = fd.FaceDetector(weightsPath, capturePath)
    with open(azureKeys,"r") as f:
        sub = json.load(f)
        f.close()
    azureCognitive = am.AzureCognitiveManager(sub)

    face = Face()
    return faceDetector, azureCognitive, face 

def pretty(d,indent=0):
    for k,v in d.items():
        print('\t' * indent + str(k))
        if isinstance(v,dict):
                    pretty(v, indent+1)
        else:
            print ('\t' * (indent+1) + str(v))

def showAvatar(dic, msg, faceId):
    print("//////////////Show Avatar Enter//////////////")
    avatarBuilder = AvatarBuilder()
    print("//////////////Show cycle//////////////")
    avatarBuilder.cycleDictionary(dic)
    print("//////////////Show Avatar show set image//////////////")
    avatarBuilder.setImageToAvatar()

    print("//////////////displayImage Enter //////////////")
    displayImage(avatarBuilder.avatar.ImagePath, msg)

    print("//////////////Show Display Info Enter//////////////")
    displayInfo(avatarBuilder.avatar)

    print("//////////////Show display Ad//////////////")
    displayAd(avatarBuilder.avatar)

    
##    file = FaceCSVInfoWriter()
##    file.getAvatarData(avatarBuilder.avatar)
##    file.writeData()


def displayInfo(avatar):
    displayInfo = DisplayInfo()
    displayInfo.writeLine("Gender: " + str(avatar.Gender))
    displayInfo.writeLine("Age: " + str(avatar.Age))
    displayInfo.writeLine("Glasses: " + str(avatar.Glasses))
    displayInfo.writeLine("Facial Hair: " + str(avatar.FacialHairValue))
    displayInfo.writeLine("Hair Color: " + str(avatar.HairColorValue))
    displayInfo.writeLine("Baldness: " + str(avatar.Bald*100) + "%")
    displayInfo.writeLine("Anger: " + str(avatar.Anger*100) + "%")
    displayInfo.writeLine("Contempt: " + str(avatar.Contempt*100) + "%")
    displayInfo.writeLine("Disgust: " + str(avatar.Disgust*100) + "%")
    displayInfo.writeLine("Fear: " + str(avatar.Fear*100) + "%")
    displayInfo.writeLine("Happiness: " + str(avatar.Happiness*100) + "%")
    displayInfo.writeLine("Neutral: " + str(avatar.Neutral*100) + "%")
    displayInfo.writeLine("Sadness: " + str(avatar.Sadness*100) + "%")
    displayInfo.writeLine("Surprise: " + str(avatar.Surprise*100) + "%")
    displayInfo.showInfo()

def displayAd(avatar):
    smartAd = cv2.imread(avatar.AdPath,cv2.IMREAD_COLOR)

    cv2.namedWindow('Smart Advertisement', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Smart Advertisement', 640, 550)
    cv2.moveWindow('Smart Advertisement', 640, 480)
    cv2.imshow('Smart Advertisement', smartAd)
    
    
def displayImage(imagePath, msg):
    avatar = cv2.imread(imagePath,cv2.IMREAD_COLOR)

    cv2.namedWindow('Avatar', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Avatar', 640, 480)
    cv2.moveWindow('Avatar', 640, 0)
    cv2.putText(avatar,msg,(10,280), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('Avatar', avatar)


def azureThread(facetemp):
    print("//////////////////////Enter Thread///////////////////////")
    facetemp._faceAttr, tempFaceId = azureCognitive.getFaceAttr(capturePath)
    if face._faceAttr != None:
        print("//////////////Azure find similar before//////////////")
        similar = azureCognitive.findSimilar(tempFaceId)
                    
        facetemp._faceId = tempFaceId
        print("//////////////Azure open faceids//////////////")
        with open("azureCogServManager/faceids.txt","a") as f:
            f.write(facetemp._faceId+'\n')
            f.close()
        print("//////////////Azure close faceids//////////////")                    
        if similar:
            facetemp._faceId= similar['faceId']
            showAvatar(facetemp._faceAttr, "Hello Again!", facetemp._faceId)
        else:
            showAvatar(facetemp._faceAttr, "Hi, new person!", facetemp._faceId)
    time.sleep(3)
    print("//////////////////////Exit Thread///////////////////////")
    
        
if __name__== "__main__":
    faceDetector, azureCognitive, face = initObjects()
    detectFaceTimes = 0
    while True:
        faceDetector.resetAttr()
        t = threading.Thread(target=faceDetector.detectFace)
        t.start()
        while not faceDetector._faceDetected: pass
        
        faceDetector.stop()
        print("//////////////AFTER facedetecto.stop()//////////////")
        try:            
            if os.path.isfile(capturePath):
                print(str(lockAzureThread))
                if not lockAzureThread:
                    print("//////////////////////Enter if///////////////////////")
                    lockAzureThread = True
                    t2 = threading.Thread(target=azureThread, args=[face])
                    t2.start()
                    detectFaceTimes = 0
                    print("//////////////////////Exit if///////////////////////")
                else:
                    if detectFaceTimes == 9:
                        print("//////////////Lock OFF//////////////")
                        lockAzureThread = False
                    print("//////////////////////Enter ELSE///////////////////////")
                    detectFaceTimes = detectFaceTimes + 1
                        
        except cv2.error as e:
            print(e)
