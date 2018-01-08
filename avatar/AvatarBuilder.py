from .Avatar import Avatar

class AvatarBuilder(object):
    IMAGE_BASE = 'avatar/images/'
    
    SMILE_KEY = 'smile'
    GENDER_KEY = 'gender'
    AGE_KEY = 'age'
    GLASSES_KEY = 'glasses'
    HAIR_KEY = 'hair'
    BALD_KEY = 'bald'
    HAIR_COLOR_KEY = 'hairColor'
    COLOR_KEY = 'color'
    BALD_KEY = 'bald'
    FACIAL_HAIR_KEY = 'facialHair'
    ANGER_KEY = 'anger'
    CONTEMPT_KEY = 'contempt'
    DISGUST_KEY = 'disgust'
    FEAR_KEY = 'fear'
    HAPPINESS_KEY = 'happiness'
    NEUTRAL_KEY = 'neutral'
    SADNESS_KEY = 'sadness'
    SURPRISE_KEY = 'surprise'
    EMOTION_KEY = 'emotion'
    
    FEMALE_VALIDATION = 'female'
    MALE_VALIDATION = 'male'
    BLOND_VALIDATION = 'blond'
    BRUNETTE_VALIDATION = 'brown'
    DARK_VALIDATION = 'black'
    RED_VALIDATION = 'red'

    NO_GLASSES = 'NoGlasses'
    GLASSES = 'Glasses'
    
    FEMALE = 'Female'
    MALE = 'Male'
    BALD = 'Blad'
    BLOND = 'Blond'
    BRUNETTE = 'Brunette'
    DARK = 'Dark'
    RED = 'Red'
    BEARD = 'Beard'
    MOUSTACHE = 'Moustache'
    ANGRY = 'Angry'
    SURPRISE = 'Surprise'

    HAPPY = 'Happy'
    NEUTRAL = 'Neutral'
    
    def __init__(self):
        self.avatar = Avatar()

    def cycleDictionary(self,d,indent=0):
        for k,v in d.items():
            if str(k) == self.EMOTION_KEY:
                self.avatar.setEmotion(v)
                print(self.avatar.Emotion)
            elif str(k) == self.GENDER_KEY:
                self.avatar.setGender(v)
            elif str(k) == self.GLASSES_KEY:
                self.avatar.setGlasses(v)
            elif str(k) == self.BALD_KEY:
                self.avatar.setBald(v)
            elif str(k) == self.HAIR_COLOR_KEY:
                self.avatar.setHairColor(v)
            elif str(k) == self.AGE_KEY:
                self.avatar.setAge(v)
            elif str(k) == self.FACIAL_HAIR_KEY:
                self.avatar.setFacialHair(v)
            elif str(k) == self.ANGER_KEY:
                self.avatar.Anger = v
            elif str(k) == self.CONTEMPT_KEY:
                self.avatar.Contempt = v
            elif str(k) == self.DISGUST_KEY:
                self.avatar.Disgust = v
            elif str(k) == self.FEAR_KEY:
                self.avatar.Fear = v
            elif str(k) == self.HAPPINESS_KEY:
                self.avatar.Happiness = v
            elif str(k) == self.NEUTRAL_KEY:
                self.avatar.Neutral = v
            elif str(k) == self.SADNESS_KEY:
                self.avatar.Sadness = v
            elif str(k) == self.SURPRISE_KEY:
                self.avatar.Surprise = v
            
            if isinstance(v,dict):
                self.cycleDictionary(v)

    def defineGender(self):
        if(self.avatar.Gender == self.MALE_VALIDATION):
            return self.MALE
        else:
            return self.FEMALE

    def defineGlasses(self):
        if(self.avatar.Glasses == self.NO_GLASSES):
            return ''
        else:
            return self.GLASSES

    def defineEmotion(self):
        if self.avatar.Anger > 0.1:
            return self.ANGRY
        elif self.avatar.Surprise > 0.1:
            return self.SURPRISE
        elif self.avatar.Happiness > 0.6:
            return self.HAPPY
        else:
            return self.NEUTRAL

    def defineHairColor(self):
        if self.avatar.Bald > 0.8:
            self.avatar.HairColorValue = "No Hair"
            return self.BALD
        hairColorDictionary = {}
        for item in self.avatar.HairColor:
            if str(item['color']) == self.BLOND_VALIDATION:
                hairColorDictionary[self.BLOND] = item['confidence']
            elif str(item['color']) == self.BRUNETTE_VALIDATION:
                hairColorDictionary[self.BRUNETTE] = item['confidence']
            elif str(item['color']) == self.DARK_VALIDATION:
                hairColorDictionary[self.DARK] = item['confidence']
            elif str(item['color']) == self.RED_VALIDATION:
                hairColorDictionary[self.RED] = item['confidence']
                
        highest = max(hairColorDictionary, key=lambda key: hairColorDictionary[key])
        
        self.avatar.HairColorValue = highest
        return highest

    def defineFacialHair(self):
        if (self.avatar.FacialHair['moustache'] < 0.15) & (self.avatar.FacialHair['beard'] < 0.15):
            self.avatar.FacialHairValue = "None"
            return ''
        elif (self.avatar.FacialHair['moustache'] > 0.7) & (self.avatar.FacialHair['beard'] < 0.15):
            self.avatar.FacialHairValue = self.MOUSTACHE
            return self.MOUSTACHE
        elif (self.avatar.FacialHair['moustache'] > 0.2) & (self.avatar.FacialHair['beard'] > 0.2):
            self.avatar.FacialHairValue = self.BEARD
            return self.BEARD
        else:
            self.avatar.FacialHairValue = "None"
            return ''
        
    def defineAdPath(self):
        if (self.avatar.Gender == self.FEMALE_VALIDATION) & (self.avatar.Glasses == self.NO_GLASSES):
            self.avatar.setAdPath('imgAds/revlonAd.jpg')
        else:
            self.avatar.setAdPath('imgAds/glassesAd.jpg')
        if (self.avatar.Gender == self.MALE_VALIDATION) & (self.avatar.Glasses == self.NO_GLASSES) & (self.avatar.FacialHairValue == "None"):
            self.avatar.setAdPath('imgAds/nikeAd.jpg')
        elif (self.avatar.Gender == self.MALE_VALIDATION) & (self.avatar.Glasses != self.NO_GLASSES) & (self.avatar.FacialHairValue == "None"):
            self.avatar.setAdPath('imgAds/MaleGlassesAd.jpg')
        elif (self.avatar.Gender == self.MALE_VALIDATION) & (self.avatar.Glasses != self.NO_GLASSES) & (self.avatar.FacialHairValue == self.BEARD):
            self.avatar.setAdPath('imgAds/MaleGlassesBeardAd.jpg')
        elif (self.avatar.Gender == self.MALE_VALIDATION) & (self.avatar.Glasses == self.NO_GLASSES) & (self.avatar.FacialHairValue == self.BEARD):
            self.avatar.setAdPath('imgAds/beardAd.jpg')
            
            
            
        
    def setImageToAvatar(self):
        self.avatar.setImagePath(self.IMAGE_BASE
                                 + self.defineGender()
                                 + self.defineHairColor()
                                 + self.defineEmotion()
                                 + self.defineGlasses()
                                 + self.defineFacialHair()
                                 + '.png')
        self.defineAdPath()
        
            

