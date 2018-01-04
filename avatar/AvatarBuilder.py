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

    HAPPY = 'Happy'
    NEUTRAL = 'Neutral'
    
    def __init__(self):
        self.avatar = Avatar()

    def cycleDictionary(self,d,indent=0):
        for k,v in d.items():
            if str(k) == self.SMILE_KEY:
                self.avatar.setEmotion(v)
            elif str(k) == self.GENDER_KEY:
                self.avatar.setGender(v)
            elif str(k) == self.GLASSES_KEY:
                self.avatar.setGlasses(v)
            elif str(k) == self.BALD_KEY:
                self.avatar.setBald(v)
            elif str(k) == self.HAIR_COLOR_KEY:
                self.avatar.setHairColor(v)
            elif str(k) == self.AGE_KEY:
                self.avatar.setHairColor(v)
            elif str(k) == self.FACIAL_HAIR_KEY:
                self.avatar.setFacialHair(v)
            
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
        if(self.avatar.Emotion > 0.52):
            return self.HAPPY
        else:
            return self.NEUTRAL

    def defineHairColor(self):
        if self.avatar.Bald > 0.8:
            return self.BALD
        hairColorDictionary = {}
        print(str(len(self.avatar.HairColor)))
        for item in self.avatar.HairColor:
            if str(item['color']) == self.BLOND_VALIDATION:
                hairColorDictionary[self.BLOND] = item['confidence']
            elif str(item['color']) == self.BRUNETTE_VALIDATION:
                hairColorDictionary[self.BRUNETTE] = item['confidence']
            elif str(item['color']) == self.DARK_VALIDATION:
                hairColorDictionary[self.DARK] = item['confidence']
            elif str(item['color']) == self.RED_VALIDATION:
                hairColorDictionary[self.RED] = item['confidence']
        print(str(hairColorDictionary))
        highest = max(hairColorDictionary, key=lambda key: hairColorDictionary[key])
        print(str(highest))
        return highest

    def defineFacialHair(self):
        print(str(self.avatar.FacialHair))
        if (self.avatar.FacialHair['moustache'] < 0.35) & (self.avatar.FacialHair['beard'] < 0.35):
            return ''
        elif (self.avatar.FacialHair['moustache'] > 0.5) & (self.avatar.FacialHair['beard'] < 0.45):
            return self.MOUSTACHE
        elif (self.avatar.FacialHair['moustache'] > 0.4) & (self.avatar.FacialHair['beard'] > 0.4):
            return self.BEARD
        else:
            return ''
    def setImageToAvatar(self):
        print(self.defineHairColor())
        print(self.defineGender())
        print(self.defineEmotion())
        print(self.defineGlasses())
        self.avatar.setImagePath(self.IMAGE_BASE
                                 + self.defineGender()
                                 + self.defineHairColor()
                                 + self.defineEmotion()
                                 + self.defineGlasses()
                                 + self.defineFacialHair()
                                 + '.png')
        
            

