from sound_class import Sound
import json
import os

def save_sounds(sounds, save_name = "save.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, save_name)
    save_data = [str(sound) for sound in sounds]
    print(save_data)
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(save_data, file, ensure_ascii=False, indent=4)
    
    with open(save_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print(data)

def load_sounds(save_name = "save.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, save_name)
    with open(save_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        sounds = []
        for pice in data:
            sounds.append(Sound.loadFromStr(pice))
        for sound in sounds:
            print(str(sound))
    return sounds