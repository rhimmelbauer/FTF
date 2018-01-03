import FaceDetector as fd
import threading,cv2

d = fd.FaceDetector("/home/pixiepro/Demos/FTF/faceDetector/weightsTest.txt",'img.jpg')
t = threading.Thread(target=d.detectFace)
t.start()
