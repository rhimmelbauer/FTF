import FaceDetector as fd
import threading,cv2

d = fd.FaceDetector("/home/pixiepro/Demos/FTF/faceDetector/weights.txt",'img.jpg')
t = threading.Thread(target=d.detectFace)
t.start()
