import csv
import os
import datetime

class FaceCSVInfoWriter(object):
    HEADER = ("GENDER",
              "AGE",
              "GLASSESS",
              "FACIAL_HAIR",
              "HAIR_COLOR",
              "BALDNESS",
              "ANGER",
              "CONTEMPT",
              "DISGUST",
              "FEAR",
              "HAPPINESS",
              "NEUTRAL",
              "SADNESS",
              "SURPRISE",
              "DATE_TIME")

    FilePath = 'captureStats/dbFaces.csv'
    
    def __init__(self):
        if not os.path.isfile(self.FilePath):
            self.createFile()
            
    def createFile(self):
        with open(self.FilePath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            
    def getAvatarData(self, avatar):
        self.data = (avatar.Gender,
                avatar.Age,
                avatar.Glasses,
                avatar.FacialHairValue,
                avatar.HairColorValue,
                avatar.Bald,
                avatar.Anger,
                avatar.Contempt,
                avatar.Disgust,
                avatar.Fear,
                avatar.Happiness,
                avatar.Neutral,
                avatar.Sadness,
                avatar.Surprise,
                str(datetime.datetime.now()))
        
    def writeData(self):
        with open(self.FilePath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.data)
