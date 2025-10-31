import json
from kivy.core.audio import SoundLoader

class Sound():
    def __init__(self,name,filepath,tags=''):
        self.name = name    # 'big fart in church'
        self.filepath = filepath    # 'C:\big_fart_in_church'
        self.tags = tags # '[fun, fart, xd]'
        self.sound = None
        self.load()

    def saveToStr(self):
        my_dict = {
            "name": self.name,
            "filepath": self.filepath,
            "tags": self.tags,
            }
        return json.dumps(my_dict)
    
    @classmethod
    def loadFromStr(cls,json_str):
        my_dict = json.loads(json_str)  
        return Sound(my_dict["name"],my_dict["filepath"],my_dict["tags"])
    
    def __str__(self):
        return self.saveToStr()
    
    def load(self):
        self.sound = SoundLoader.load(self.filepath)
    
    def play(self,instance=None):
        self.sound.play()
    
    def stop(self,instance=None):
        self.sound.stop()
    

if __name__ == "__main__":
    json_str = '{"name": "soup","filepath": "D:/soup","tags": ["soup","soup can"]}'
    print(Sound.loadFromStr(json_str))