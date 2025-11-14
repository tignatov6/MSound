from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from sound_class import Sound
from plyer import filechooser
from kivy.properties import ObjectProperty
import save_manager
import time
import os

Window.clearcolor = (0,0,0,0)

SOUND_DIR = "sounds"

def sort_by_attr(objects_list, attribute, ascending=True):
    """
    Сортирует список объектов по указанному атрибуту.
    
    Аргументы:
        objects_list -- список экземпляров класса
        attribute    -- имя атрибута (строка), по которому сортировать
        ascending    -- True: по возрастанию, False: по убыванию
    
    Возвращает:
        Новый отсортированный список
    """
    return sorted(objects_list, key=lambda obj: getattr(obj, attribute), reverse=not ascending)

class Gutton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None
        self.last_press = None
        self.hold_time = 2
        self.stop_all_sounds = None
        self.remove_sound_from_sounds = None

    def on_press(self):
        try:
            self.last_press = time.time()
            self.stop_all_sounds()
        except Exception as e:
            print(f'Ошибка: {e}')
        
    def on_release(self):
        #try:
            hold_time = time.time() - self.last_press
            if hold_time >= self.hold_time:
                self.stop_all_sounds()
                self.remove_sound_from_sounds(self.sound)
                
            else:
                self.sound.play()
        # except Exception as e:
        #     print(f'Ошибка: {e}')


class MSoundApp(App):

    #print(os.listdir(SOUND_DIR))
    # for name in os.listdir(SOUND_DIR):
    #     name_without_ext, extension = os.path.splitext(name)
    #     sounds.append(Sound(name_without_ext,os.path.join(SOUND_DIR,name)))
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.READ_MEDIA_AUDIO])
        except:
            pass

        self.sounds = []
        self.sounds = save_manager.load_sounds()

        root = BoxLayout(orientation='vertical', padding=8, spacing=8)
        
        hl = BoxLayout(spacing=8, size_hint_y=None, height=40)
        settings_button = Button(text='reload', background_color=[0.1, 0, 0.7, 1])
        settings_button.bind(on_press=self.change_buttons)
        hl.add_widget(settings_button)
        root.add_widget(hl)
        
        self.layout = GridLayout(cols=2, spacing=5, size_hint_y=None, size_hint_x=1)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.bind(width=self.update_button_heights)
        
        #self.create_initial_100buttons()
        
        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(self.layout)
        root.add_widget(scrollview)

        self.change_buttons()

        return root

    def create_initial_100buttons(self):
        # Use Window.width for initial creation as layout width is not set yet.
        button_width = (Window.width - 5) / 2
        addsoundbtn = Button(text='add sound', background_color=[0.1, 0.7, 0, 1], size_hint_y=None, height=button_width)
        addsoundbtn.bind(on_press=self.add_sound)
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=button_width)
            self.layout.add_widget(btn)

    def update_button_heights(self, instance, width):
        button_width = (width - 5) / 2
        if button_width <= 0:
            return
        for btn in self.layout.children:
            btn.height = button_width

    def change_buttons(self, instance=None):
        self.layout.clear_widgets()
        
        # Use layout.width as it's already part of the widget tree and has a width
        button_width = (self.layout.width - 5) / 2
        if button_width <= 0:
            return

        addsoundbtn = Button(text='add sound', background_color=[0.1, 0.7, 0, 1], size_hint_y=None, height=button_width)
        addsoundbtn.bind(on_press=self.add_sound)
        self.layout.add_widget(addsoundbtn)
        
        print('Unsorted:',self.sounds)
        self.sounds = sort_by_attr(self.sounds,'pos')
        print('Sorted:',self.sounds)

        for sound in self.sounds:
            btn = Gutton(text=sound.name, size_hint_y=None, height=button_width)
            self.layout.add_widget(btn)
            btn.sound = sound
            btn.stop_all_sounds = self.stop_all_sounds
            btn.remove_sound_from_sounds = self.remove_sound_from_sounds

    def add_sound(self, instance):
        """
        Метод, вызывающий системный диалог выбора файла.
        """
        try:
            self.stop_all_sounds()

            print("📂 Открываю filechooser...")
            try:
                from android.permissions import check_permission, Permission
                has_perm = check_permission(Permission.READ_MEDIA_AUDIO)
                print(f"Разрешение READ_MEDIA_AUDIO: {has_perm}")
            except Exception as e:
                print(f"Не удалось проверить разрешение: {e}")
                import traceback
                traceback.print_exc()

            paths = filechooser.open_file(
                title='Выберите звуковой файл',
                filters=[
                    ('Все файлы', '*')
                ],
                multiple=True,
                use_cache=True
            )

            print(f"📄 Результат filechooser: {paths} (тип: {type(paths)})")

            if paths:
                for path in paths:
                    # Результат — это список, даже если выбран один файл
                    selected_file = path
                    print(f'Выбран файл: {selected_file}')
                    selected_file = save_manager.copy_sound(selected_file, 'sounds')
                    sound = Sound(os.path.basename(selected_file),selected_file,pos=len(self.sounds)+1)
                    for _sound1 in self.sounds:
                        if _sound1.name == sound.name and _sound1.filepath == sound.filepath:
                            self.sounds.remove(_sound1)
                    sound = Sound(os.path.basename(selected_file),selected_file,pos=len(self.sounds)+1)
                    self.sounds.append(sound)
                    self.change_buttons()
                    save_manager.save_sounds(sounds=self.sounds)
                    # Здесь можно добавить логику для работы со звуковым файлом
            else:
                #self.selected_label.text = 'Выбор отменён'
                print('Файл не выбран.')


        except Exception as e:
            print(f'Ошибка: {e}')
            import traceback
            traceback.print_exc()

    def stop_all_sounds(self, instance=None):
        for sound in self.sounds:
            if sound:
                sound.stop()

    def remove_sound_from_sounds(self, sound):
        sound_path = sound.filepath

        self.sounds.remove(sound)
        sound.unload()
        del sound
        for i,sound in enumerate(self.sounds):
            sound.pos = i+1
        self.change_buttons()
        save_manager.delete_sound_by_path(sound_path)
        


app = MSoundApp()
app.run()