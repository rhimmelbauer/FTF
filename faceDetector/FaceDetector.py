import cv2
import sys, os
import json

class FaceDetector:

        def __init__(self, weightsFile,pathToImage):
                with open(weightsFile) as w:
                        weights = json.load(w)
                        w.close()
                self._pathToImage = pathToImage
                self._faceCascade = cv2.CascadeClassifier(weights['frontalFace'])
                self._smileCascade = cv2.CascadeClassifier(weights['smile'])
                self.resetAttr()
                self._cam = None
                self._continue = False
                self.initCam = False

        def __del__(self):
                if self._cam:
                        self._cam.release()
                cv2.destroyAllWindows()
                cv2.waitKey(1)

        def __exit__(self, etype, evalue, traceback):
                if self._cam:
                        self._cam.release()
                cv2.destroyAllWindows()
                cv2.waitKey(1)

        def resetAttr(self):
                self._faceDetected = False
                self._smileDetected = False
                self._capture = None
                try:
                        os.remove(self._pathToImage)
                except:
                        pass

        def _getFacesInFrame(self,frame):
                faces = self._faceCascade.detectMultiScale(
                                                        frame,
                                                        scaleFactor=1.9,
                                                        minNeighbors=5,
                                                        minSize=(60,60),
                                                        flags=cv2.CASCADE_SCALE_IMAGE
                                                        )
                return faces

        def _getSmilesInFrame(self,frame):
                smiles = self._smileCascade.detectMultiScale(
                                                                frame,
                                                                scaleFactor = 1.7,
                                                                minNeighbors = 22,
                                                                minSize = (25,25),
                                                                flags=cv2.CASCADE_SCALE_IMAGE
                                                                )
                return smiles
                
        def stop(self):
                self._continue = False
        
        def detectFace(self):
                
                if self.initCam == False:
                        self.initCam = True
                        self._cam = cv2.VideoCapture(0)
                self._continue = True                
                while self._continue is True:
                        ret, frame = self._cam.read()
                        img = frame.copy()
                        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                        faces = self._getFacesInFrame(gray)
                        for (x,y,w,h) in faces:
                                if self._capture is None:
                                        self._capture = img
                                        cv2.imwrite(self._pathToImage,self._capture)
                                self._faceDetected = True #This has to be done AFTER file has been written
                                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                                roi_gray=gray[y:y+h, x:x+w]
                                roi_color=frame[y:y+h, x:x+w]
                                smiles = self._getSmilesInFrame(roi_gray)
                                for (ex,ey,ew,eh) in smiles:
                                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
                                        self._smileDetected = True
                                        self._capture = img                                                
                        cv2.imshow('Video',frame)
                        cv2.moveWindow('Video',0,0)
                        if cv2.waitKey(30) & 0xff == ord('q'):
                                break
##                self._cam.release()
                if self._faceDetected:
                        cv2.imwrite(self._pathToImage,self._capture)
