import imp, json,cv2,os
import sys, threading, time
from multiprocessing import Queue
from avatar.AvatarBuilder import AvatarBuilder
from captureStats.DisplayInfo import DisplayInfo
import time

weightsPath =  "faceDetector/weights.txt"
capturePath = "faceDetector/img.jpg"
azureKeys = "keys/azureKeys.txt"

fd = imp.load_source('FaceDetector','faceDetector/FaceDetector.py')
am = imp.load_source('AzureCognitiveManager','azureCogServManager/AzureCognitiveManager.py')

lockAzureThread = False

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

def showAvatar(dic, msg):

    avatarBuilder = AvatarBuilder()

    avatarBuilder.cycleDictionary(dic)
    avatarBuilder.setImageToAvatar()

    displayImage(avatarBuilder.avatar.ImagePath, msg)

    displayInfo = DisplayInfo()
    displayInfo.writeLine("Gender: " + str(avatarBuilder.avatar.Gender))
    displayInfo.writeLine("Age: " + str(avatarBuilder.avatar.Age))
    displayInfo.writeLine("Glasses: " + str(avatarBuilder.avatar.Glasses))
    displayInfo.writeLine("Facial Hair: " + str(avatarBuilder.avatar.FacialHairValue))
    displayInfo.writeLine("Hair Color: " + str(avatarBuilder.avatar.HairColorValue))
    displayInfo.writeLine("Baldness: " + str(avatarBuilder.avatar.Bald*100) + "%")
    displayInfo.writeLine("Anger: " + str(avatarBuilder.avatar.Anger*100) + "%")
    displayInfo.writeLine("Contempt: " + str(avatarBuilder.avatar.Contempt*100) + "%")
    displayInfo.writeLine("Disgust: " + str(avatarBuilder.avatar.Disgust*100) + "%")
    displayInfo.writeLine("Fear: " + str(avatarBuilder.avatar.Fear*100) + "%")
    displayInfo.writeLine("Happiness: " + str(avatarBuilder.avatar.Happiness*100) + "%")
    displayInfo.writeLine("Neutral: " + str(avatarBuilder.avatar.Neutral*100) + "%")
    displayInfo.writeLine("Sadness: " + str(avatarBuilder.avatar.Sadness*100) + "%")
    displayInfo.writeLine("Surprise: " + str(avatarBuilder.avatar.Surprise*100) + "%")
    displayInfo.showInfo()
    
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
        similar = azureCognitive.findSimilar(tempFaceId)
                    
        facetemp._faceId = tempFaceId
        with open("azureCogServManager/faceids.txt","a") as f:
            f.write(facetemp._faceId+'\n')
            f.close()
                            
        if similar:
            facetemp._faceId= similar['faceId']
            showAvatar(facetemp._faceAttr, "Hello Again!")
        else:
            showAvatar(facetemp._faceAttr, "Hi, new person!")
    time.sleep(3)
    print("//////////////////////Exit Thread///////////////////////")
    lockAzureThread = False
        
if __name__== "__main__":
    faceDetector, azureCognitive, face = initObjects()
    detectFaceTimes = 0
    while True:
        faceDetector.resetAttr()
        t = threading.Thread(target=faceDetector.detectFace)
        t.start()
        while not faceDetector._faceDetected: pass
##        faceDetector.stop()
		
        try:
            
            if os.path.isfile(capturePath):
                if not lockAzureThread:
                    print("//////////////////////Enter if///////////////////////")
                    lockAzureThread = True
                    t2 = threading.Thread(target=azureThread, args=[face])
                    t2.start()
                    print("//////////////////////Exit if///////////////////////")
                else:
                    print("//////////////////////Enter ELSE///////////////////////")
                        
        except cv2.error as e:
            print(e)
