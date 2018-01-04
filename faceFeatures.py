import imp, json,cv2,os
import sys, threading, time
from multiprocessing import Queue
from avatar.AvatarBuilder import AvatarBuilder

weightsPath =  "/home/pixiepro/Demos/FTF/faceDetector/weights.txt"
capturePath = "/home/pixiepro/Demos/FTF/faceDetector/img.jpg"
azureKeys = "/home/pixiepro/Demos/FTF/keys/azureKeys.txt"

fd = imp.load_source('FaceDetector','faceDetector/FaceDetector.py')
am = imp.load_source('AzureCognitiveManager','azureCogServManager/AzureCognitiveManager.py')

class Face():
    def _init__():
        self._faceAttr = None
        self._emotion = None
        self._faceId = ""

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

    print(avatarBuilder.avatar.ImagePath)

    displayImage(avatarBuilder.avatar.ImagePath, msg)
    
def displayImage(imagePath, msg):
    avatar = cv2.imread(imagePath,cv2.IMREAD_COLOR)

    cv2.namedWindow('Avatar', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Avatar', 640, 480)
    cv2.moveWindow('Avatar', 640, 0)
    cv2.putText(avatar,msg,(10,280), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('Avatar', avatar)
    
if __name__== "__main__":
	faceDetector, azureCognitive, face = initObjects()

	while True:	
		faceDetector.resetAttr()
		t = threading.Thread(target=faceDetector.detectFace)
		t.start()
		while not faceDetector._faceDetected: pass
		faceDetector.stop()
		try:
			face._faceAttr, tempFaceId = azureCognitive.getFaceAttr(capturePath)
			if not face._faceAttr: pass
			similar = azureCognitive.findSimilar(tempFaceId)
			
			face._faceId = tempFaceId
			with open("azureCogServManager/faceids.txt","a") as f:
                            f.write(face._faceId+'\n')
                            f.close()
                            
			pretty(face._faceAttr)
			if similar:
                            face._faceId= similar['faceId']
                            showAvatar(face._faceAttr, "Hello Again!")
			else:
                            showAvatar(face._faceAttr, "Hi, new person!")
		except cv2.error as e:
			print(e)
