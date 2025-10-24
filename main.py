from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from sound_class import Sound
from plyer import filechooser
from kivy.properties import ObjectProperty
import os

SOUND_DIR = "sounds"

class MSoundApp(App):
    sounds = []
    print(os.listdir(SOUND_DIR))
    for name in os.listdir(SOUND_DIR):
        name_without_ext, extension = os.path.splitext(name)
        sounds.append(Sound(name_without_ext,os.path.join(SOUND_DIR,name)))
    def build(self):
        root = BoxLayout(orientation='vertical', padding=8, spacing=8)
        
        hl = BoxLayout(spacing=8, size_hint_y=None, height=40)
        settings_button = Button(text='reload', background_color=[0.1, 0, 0.7, 1])
        settings_button.bind(on_press=self.change_buttons)
        hl.add_widget(settings_button)
        root.add_widget(hl)
        
        self.layout = GridLayout(cols=2, spacing=5, size_hint_y=None, size_hint_x=1)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.bind(width=self.update_button_heights)
        
        self.create_initial_buttons()
        
        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(self.layout)
        root.add_widget(scrollview)

        self.change_buttons(0)
        
        return root

    def create_initial_buttons(self):
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

    def change_buttons(self, instance):
        """
        Эта функция вызывается при нажатии на кнопку "settings".
        Она очищает все кнопки и добавляет новые с буквами.
        """
        self.layout.clear_widgets()
        
        # Use layout.width as it's already part of the widget tree and has a width
        button_width = (self.layout.width - 5) / 2
        if button_width <= 0:
            return

        addsoundbtn = Button(text='add sound', background_color=[0.1, 0.7, 0, 1], size_hint_y=None, height=button_width)
        addsoundbtn.bind(on_press=self.add_sound)
        self.layout.add_widget(addsoundbtn)
        
        for sound in self.sounds:
            btn = Button(text=sound.name, size_hint_y=None, height=button_width)
            self.layout.add_widget(btn)
            btn.bind(on_press=sound.play)

    def add_sound(self, instance):
        """
        Метод, вызывающий системный диалог выбора файла.
        """
        try:
            path = filechooser.open_file(
                title='Выберите звуковой файл',
                filters=[
                    ('Все файлы', '*')
                ],
                multiple=False # Запрещает выбор нескольких файлов
            )

            if path:
                # Результат — это список, даже если выбран один файл
                selected_file = path[0]
                print(f'Выбран файл: {selected_file}')
                self.sounds.append(Sound(os.path.basename(selected_file),selected_file))
                self.change_buttons(0)
                # Здесь можно добавить логику для работы со звуковым файлом
            else:
                self.selected_label.text = 'Выбор отменён'
                print('Файл не выбран.')

        except Exception as e:
            print(f'Ошибка: {e}')

app = MSoundApp()
app.run()