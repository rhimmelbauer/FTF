import FaceDetector as fd
import threading,cv2

d = fd.FaceDetector("/Users/robertohimmelbauer/Desktop/ftf-iot-demo/faceDetector/weightsTest.txt",'img.jpg')
t = threading.Thread(target=d.detectFace)
t.start()
