from sound_class import Sound
import json
import os

def save_sounds(sounds):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for sound in sounds:
        print(str(sound))
        name, ext = os.path.splitext(os.path.basename(sound.filepath))
        save_path = os.path.join(base_dir,'sounds', name+'.json')
        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(str(sound), file, ensure_ascii=False, indent=4)


def load_sounds(load_dir = "sounds"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_path = os.path.join(base_dir, load_dir)
    sounds = []
    for filename in os.listdir(load_path):
        if filename.endswith(".json"):
            with open(os.path.join(load_path,filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                sounds.append(Sound.loadFromStr(data))
                print(str(sounds[0]))
    return sounds

def copy_file_as(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    
    chunk_size = 1024 * 1024  # 1 MB
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            while True:
                chunk = fsrc.read(chunk_size)
                if not chunk:
                    break
                fdst.write(chunk)

def copy_sound(scr,dst):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, dst,os.path.basename(scr))
    copy_file_as(scr,save_path)
    return save_path