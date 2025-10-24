from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
class MSoundApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical',padding=8,spacing=8)
        hl = BoxLayout(spacing=8)
        settings_button = Button(text='settings', background_color=[0.1, 0, 0.7, 1])
        settings_button.bind(on_press=self.change_buttons) # Привязка события
        hl.add_widget(settings_button)
        root.add_widget(hl)
        #root.add_widget(Button(text='add sound',background_color=[0.1, 0.7, 0, 1]))
        self.layout = GridLayout(cols=2, spacing=5, size_hint_y=None,size_hint_x=None,size=(Window.width, Window.height))
        # Make sure the height is such that there is something to scroll.
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.add_widget(Button(text='add sound',background_color=[0.1, 0.7, 0, 1]))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            self.layout.add_widget(btn)
        scrollview = ScrollView(size_hint=(None, None), size=(Window.width, Window.height*0.85))
        scrollview.add_widget(self.layout)
        root.add_widget(scrollview)
      
        return root
   
    def change_buttons(self, instance):
        """
        Эта функция вызывается при нажатии на кнопку "settings".
        Она очищает все кнопки и добавляет новые с буквами.
        """
        # 1. Очищаем все старые виджеты (кнопки) из self.layout
        self.layout.clear_widgets()
        
        # 2. Снова добавляем кнопку "add sound", так как она тоже удалилась
        self.layout.add_widget(Button(text='add sound', background_color=[0.1, 0.7, 0, 1], size_hint_y=30, height=40))
        
        # 3. Добавляем новые кнопки с буквами
        letters = ['a', 'b', 'c', 'd', 'e', 'f']
        for letter in letters:
            btn = Button(text=letter, size_hint_y=30, height=40)
            self.layout.add_widget(btn)

app = MSoundApp()
app.run()
