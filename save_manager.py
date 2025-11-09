from sound_class import Sound
import json
import shutil
import os

def save_sounds(sounds):
    create_sound_dir()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for sound in sounds:
        print(str(sound))
        name, ext = os.path.splitext(os.path.basename(sound.filepath))
        save_path = os.path.join(base_dir,'sounds', name+'.json')
        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(str(sound), file, ensure_ascii=False, indent=4)


def load_sounds(load_dir = "sounds"):
    create_sound_dir()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_path = os.path.join(base_dir, load_dir)
    sounds = []
    for i,filename in enumerate(os.listdir(load_path)):
        if filename.endswith(".json"):
            with open(os.path.join(load_path,filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                sound = Sound.loadFromStr(data)
                sounds.append(sound)
                #print(sound)
    return sounds

def copy_sound(src_path, dst_folder):
    """
    Копирует файл в папку назначения, если он еще не там.
    Возвращает новый путь к файлу.
    """
    create_sound_dir()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Полный путь к папке назначения
    full_dst_folder_path = os.path.join(base_dir, dst_folder)
    os.makedirs(full_dst_folder_path, exist_ok=True)

    # Путь, куда будет скопирован файл
    dst_path = os.path.join(full_dst_folder_path, os.path.basename(src_path))

    # Сравниваем реальные пути к файлам, чтобы быть уверенными
    if os.path.realpath(src_path) == os.path.realpath(dst_path):
        print("Файл уже находится в целевой папке. Копирование не требуется.")
        return src_path

    # Используем безопасное копирование из shutil
    print(f"Копирование файла из '{src_path}' в '{dst_path}'")
    shutil.copy2(src_path, dst_path) # copy2 сохраняет метаданные
    
    return dst_path

def delete_sound(sound_to_delete):
    """
    Удаляет медиафайл и связанный с ним .json файл.
    
    Аргументы:
        sound_to_delete -- объект класса Sound, который нужно удалить.
    """
    create_sound_dir()
    if not isinstance(sound_to_delete, Sound):
        print("Ошибка: в функцию delete_sound был передан неверный объект.")
        return

    sound_path = sound_to_delete.filepath
    
    # --- Удаление медиафайла ---
    try:
        if os.path.exists(sound_path):
            os.remove(sound_path)
            print(f"Медиафайл удален: {sound_path}")
        else:
            print(f"Медиафайл не найден, удаление не требуется: {sound_path}")
    except OSError as e:
        print(f"Ошибка при удалении медиафайла {sound_path}: {e}")

    # --- Удаление .json файла ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Получаем имя файла без расширения
    name, _ = os.path.splitext(os.path.basename(sound_path))
    # Формируем путь к .json файлу
    json_path = os.path.join(base_dir, 'sounds', name + '.json')
    
    try:
        if os.path.exists(json_path):
            os.remove(json_path)
            print(f"JSON файл удален: {json_path}")
        else:
            print(f"JSON файл не найден, удаление не требуется: {json_path}")
    except OSError as e:
        print(f"Ошибка при удалении JSON файла {json_path}: {e}")


def delete_sound_by_path(sound_path):
    """
    Удаляет медиафайл и связанный с ним .json файл.
    
    Аргументы:
        sound_to_delete -- path до звука, который нужно удалить.
    """
    create_sound_dir()
    # --- Удаление медиафайла ---
    try:
        if os.path.exists(sound_path):
            os.remove(sound_path)
            print(f"Медиафайл удален: {sound_path}")
        else:
            print(f"Медиафайл не найден, удаление не требуется: {sound_path}")
    except OSError as e:
        print(f"Ошибка при удалении медиафайла {sound_path}: {e}")

    # --- Удаление .json файла ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Получаем имя файла без расширения
    name, _ = os.path.splitext(os.path.basename(sound_path))
    # Формируем путь к .json файлу
    json_path = os.path.join(base_dir, 'sounds', name + '.json')
    
    try:
        if os.path.exists(json_path):
            os.remove(json_path)
            print(f"JSON файл удален: {json_path}")
        else:
            print(f"JSON файл не найден, удаление не требуется: {json_path}")
    except OSError as e:
        print(f"Ошибка при удалении JSON файла {json_path}: {e}")

def create_sound_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(base_dir, 'sounds')
    os.makedirs(dir, exist_ok=True)