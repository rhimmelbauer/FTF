import numpy as np
import cv2

class DisplayInfo(object):
    HEIGHT = 550
    WIDTH = 640
    FONT = cv2.FONT_HERSHEY_PLAIN
    WINDOW_NAME = 'Capture Info'
    OFFSET = 26
    MULTIPLIER = 4

    LineNumber = 1
    
    def __init__(self):
        self.image = np.zeros((self.HEIGHT*3, self.WIDTH*3, 1), np.uint8)
        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.WINDOW_NAME, self.WIDTH, self.HEIGHT)
        cv2.moveWindow(self.WINDOW_NAME,0, 480)
        cv2.putText(self.image, "Information Captured", (10, (self.OFFSET*self.MULTIPLIER)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2)

    def writeLine(self, msg):
        y = (self.LineNumber * 26) + self.OFFSET
        x = 10
        cv2.putText(self.image, msg, (x, (y*self.MULTIPLIER)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2)
        self.LineNumber = self.LineNumber + 1
        
    def showInfo(self):
        cv2.imshow(self.WINDOW_NAME, self.image)
        
