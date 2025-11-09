import json
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.logger import Logger

class CustomSoundLoader(SoundLoader):
    @staticmethod
    def load(filename):
        '''Load a sound, and return a Sound() instance.'''
        # file_path = filename
        rfn = resource_find(filename)
        if rfn is not None:
            filename = rfn
        ext = filename.split('.')[-1].lower()
        if '?' in ext:
            ext = ext.split('?')[0]
        for classobj in SoundLoader._classes:
            if ext in classobj.extensions():
                return classobj(source=filename)
        #Logger.warning('Audio: Unable to find a loader for <%s>' %
        #               filename)
        
        # video = VideoFileClip(file_path)
        # #print(video.duration)
        # audio = video.audio
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # audio_dir = os.path.join(base_dir,'sounds','temp')
        # audio_file = os.path.join(audio_dir,'temp.mp3')
        # os.makedirs(os.path.dirname(audio_dir), exist_ok=True)
        
        # # Сохранение аудио в новый файл (например, в формате mp3)
        # audio.write_audiofile(audio_file)

        # rfn = resource_find(audio_file)
        # if rfn is not None:
        #     filename = rfn
        # ext = filename.split('.')[-1].lower()
        # if '?' in ext:
        #     ext = ext.split('?')[0]
        # for classobj in SoundLoader._classes:
        #     if ext in classobj.extensions():
        #         return classobj(source=filename)
        Logger.warning('Audio: Unable to find a loader for <%s>' %
                       filename)

        return None

class Sound():
    def __init__(self,name,filepath,tags='',pos=0):
        self.name = name    # 'big fart in church'
        self.filepath = filepath    # 'C:\big_fart_in_church'
        self.tags = tags # '[fun, fart, xd]'
        self.sound = None
        self.pos = pos
        self.load()

    def saveToStr(self):
        my_dict = {
            "name": self.name,
            "filepath": self.filepath,
            "tags": self.tags,
            "pos": self.pos
            }
        return json.dumps(my_dict)
    
    @classmethod
    def loadFromStr(cls,json_str):
        my_dict = json.loads(json_str)  
        return Sound(my_dict["name"],my_dict["filepath"],my_dict["tags"],my_dict["pos"])
    
    def __str__(self):
        return self.saveToStr()
    
    def load(self):
        self.sound = CustomSoundLoader.load(self.filepath)
        
    def unload(self):
        if self.sound:
            self.sound.unload()

    def play(self,instance=None):
        if self.sound:
            self.sound.play()
    
    def stop(self,instance=None):
        if self.sound:
            self.sound.stop()

    def __del__(self):
        self.unload()
    

if __name__ == "__main__":
    json_str = '{"name": "soup","filepath": "D:/soup","tags": ["soup","soup can"]}'
    print(Sound.loadFromStr(json_str))