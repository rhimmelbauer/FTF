import AzureCognitiveManager as az
import json

with open("/home/pixiepro/Demos/FTF/keys/azureKeys.txt","r") as f:
#with open("/Users/robertohimmelbauer/Desktop/keys/azureKeys.txt","r") as f:
    sub = json.load(f)
    f.close() 

urlImage = "/home/pixiepro/Demos/FTF/faceDetector/img5.jpg"
with open( urlImage, 'rb' ) as f:
    img = f.read()

def pretty(d,indent=0):
    for k,v in d.items():
        print('\t' * indent + str(k))
        if isinstance(v,list):
            v=v[0]
        if isinstance(v,dict):
                    pretty(v, indent+1)
        else:
            print ('\t' * (indent+1) + str(v))

acm = az.AzureCognitiveManager(sub)
faceAttr, faceId = acm.getFaceAttr(urlImage)
pretty(faceAttr)
similar = acm.findSimilar(faceId)
print(similar)
emotion = acm.getEmotion(urlImage)
print(emotion)


