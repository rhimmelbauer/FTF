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

TIME_FOR_AZURE = 50

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

def showAvatar(avatarBuilder):
    
    
    avatarBuilder.setImageToAvatar()

    print('//////////////// Avatar///////////////')
    displayImage(avatarBuilder.avatar.ImagePath, avatarBuilder.avatar.Msg)

    print('////////////////////INFO/////////////////')
    displayInfo(avatarBuilder.avatar)

    print('///////////////////Ad///////////////////')
    displayAd(avatarBuilder.avatar)
    print('/////////////////finish//////////////')

    
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
    print(str(avatar.AdPath))
    cv2.namedWindow('SmartAdvertisement', cv2.WINDOW_NORMAL)
    cv2.destroyWindow('SmartAdvertisement')
    smartAd = cv2.imread(avatar.AdPath,cv2.IMREAD_COLOR)

    cv2.namedWindow('SmartAdvertisement', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('SmartAdvertisement', 640, 550)
    cv2.moveWindow('SmartAdvertisement', 640, 480)
    cv2.imshow('SmartAdvertisement', smartAd)
    
    
def displayImage(imagePath, msg):
    avatar = cv2.imread(imagePath,cv2.IMREAD_COLOR)

    cv2.namedWindow('Avatar', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Avatar', 640, 480)
    cv2.moveWindow('Avatar', 640, 0)
    cv2.putText(avatar,msg,(10,280), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('Avatar', avatar)

class AzureThread(object):
    def __init__(self):
        self._azureDic = None
        self._avatarBuilder = None
        
    def callAzureThread(self, facetemp):
        facetemp._faceAttr, tempFaceId = azureCognitive.getFaceAttr("faceDetector/imgAzure.jpg")
        if face._faceAttr != None:
            
            similar = azureCognitive.findSimilar(tempFaceId)
                        
            facetemp._faceId = tempFaceId
            
            with open("azureCogServManager/faceids.txt","a") as f:
                f.write(facetemp._faceId+'\n')
                f.close()
            
            if similar:
                facetemp._faceId= similar['faceId']
                self._avatarBuilder = AvatarBuilder(facetemp._faceId, "Hello Again!")
                self._avatarBuilder.cycleDictionary(facetemp._faceAttr)
            else:
                self._avatarBuilder = AvatarBuilder(facetemp._faceId, "Hello, New Person!")
                self._avatarBuilder.cycleDictionary(facetemp._faceAttr)
                
        print("Finishing Thread")
        
if __name__== "__main__":
    faceDetector, azureCognitive, face = initObjects()
    azureThread = AzureThread()
    detectFaceTimes = TIME_FOR_AZURE
    t = threading.Thread(target=faceDetector.detectFace)
    t.start()
    while True:
        faceDetector.resetAttr()
        if azureThread._avatarBuilder != None:
            showAvatar(azureThread._avatarBuilder)
            azureThread._avatarBuilder = None

        while not faceDetector._faceDetected: pass
        
        try:
            if os.path.isfile(capturePath):
                if not lockAzureThread:
                    lockAzureThread = True
                    t2 = threading.Thread(target=azureThread.callAzureThread, args=[face])
                    print("Staring Thread")
                    t2.start()
                    detectFaceTimes = TIME_FOR_AZURE
                else:
                    if detectFaceTimes == 0:
                        lockAzureThread = False
                    if detectFaceTimes == 5:
                        faceDetector.writeImage()
                    print("Azure Snapshot in: " + str(detectFaceTimes))
                    detectFaceTimes = detectFaceTimes - 1

                        
        except cv2.error as e:
            print(e)
