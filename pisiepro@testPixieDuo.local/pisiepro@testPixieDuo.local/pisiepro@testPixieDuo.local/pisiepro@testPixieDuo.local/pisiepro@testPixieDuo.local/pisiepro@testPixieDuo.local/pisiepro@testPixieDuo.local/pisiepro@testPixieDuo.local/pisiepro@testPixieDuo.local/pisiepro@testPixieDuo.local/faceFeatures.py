import imp, json,cv2,os
import sys, threading, time
from multiprocessing import Queue

weightsPath =  "/Users/robertohimmelbauer/Desktop/ftf-iot-demo/faceDetector/weights.txt"
capturePath = "/Users/robertohimmelbauer/Desktop/ftf-iot-demo/faceDetector/img.jpg"
azureKeys = "/Users/robertohimmelbauer/Desktop/keys/azureKeys.txt"

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
			if similar:
				face._faceId= similar['faceId']
				print("Hello again!")
			else:
				face._faceId = tempFaceId
				with open("azureCogServManager/faceids.txt","a") as f:
					f.write(face._faceId+'\n')
					f.close()
				print("Hi, new person!")
				pretty(face._faceAttr)
		except:
			print("ERR")
