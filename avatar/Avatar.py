class Avatar(object):
    Emotion = ''
    Gender = ''
    Age = ''
    Glasses = ''
    Bald = ''
    HairColor = ''
    FacialHair = ''
    ImagePath = ''
    HairColorValue = ''
    FacialHairValue = ''
    BaldValue = ''
    Anger = ''
    Contempt = ''
    Disgust = ''
    Fear = ''
    Happiness = ''
    Neutral = ''
    Sadness = ''
    Surprise = ''

    def __init__(self):
        self.name = 'rob'
        
    def setEmotion(self,emotion):
        self.Emotion = emotion
    def setGender(self, gender):
        self.Gender = gender
    def setAge(self, age):
        self.Age = age
    def setGlasses(self, glasses):
        self.Glasses = glasses
    def setBald(self, bald):
        self.Bald = bald
    def setHairColor(self, hairColor):
        self.HairColor = hairColor
    def setFacialHair(self, facialHair):
        self.FacialHair = facialHair
    def setImagePath(self, imagePath):
        self.ImagePath = imagePath
