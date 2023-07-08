'''
create the GUI 
'''

from fuzzy import *
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_file('Fuzzy_project/style.kv')


class Page1(FloatLayout):
    def __init__(self, **kwargs):
        super(Page1, self).__init__(**kwargs)
        # 設置背景圖片
        self.background = Image(source='Fuzzy_project/bg1.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # 新增一個按鈕
        button = Button(text='Start', size_hint=(None, None), size=(150, 50),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button.bind(on_press=self.switch_screen)  # 綁定按鈕按下事件

        # 新增一個README按鈕
        button_readme = Button(text='Readme', size_hint=(None, None), size=(150, 50),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.4})
        button_readme.bind(on_press=self.open_readme)  # 綁定按鈕按下事件


        
        # 將按鈕添加到 Page1 中
        self.add_widget(button)
        self.add_widget(button_readme)
        
    def switch_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'page2'  # 切換到 'page2'
        
    def open_readme(self, instance):
        # 在這裡處理打開 README 的邏輯
        message_box = MessageBox(message='')
        message_box.open()


class Page2(FloatLayout):
    def __init__(self, **kwargs):
        super(Page2, self).__init__(**kwargs)

        self.background = Image(source='Fuzzy_project/bg2.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # 新增一個時鐘顯示區域
        self.label_clock = Label(text='', font_size=45, pos_hint={'center_x': 0.2, 'center_y': 0.9}, color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.label_clock)
        
        # 新增一個文字顯示區域
        self.label_cpu = Label(text='', font_size=45, pos_hint={'center_x': 0.2, 'center_y': 0.8}, color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.label_cpu)
        self.label_ram = Label(text='', font_size=45, pos_hint={'center_x': 0.2, 'center_y': 0.7}, color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.label_ram)
        self.label_battery = Label(text='', font_size=45, pos_hint={'center_x': 0.2, 'center_y': 0.6}, color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.label_battery)
        self.label_demand = Label(text='', font_size=45, pos_hint={'center_x': 0.2, 'center_y': 0.5}, color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.label_demand)
        
        
        # 新增一個返回按鈕
        back_button = Button(text='Home', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1})
        back_button.bind(on_press=self.switch_screen)
        self.add_widget(back_button)
        
        # 設定定時更新畫面，每秒更新一次
        Clock.schedule_interval(self.update_labels, 1)
        Clock.schedule_interval(self.update_clock, 1)
        
    def update_labels(self, dt):
        cpu, ram, battery = PCsensor()
        demand = Fuzzy(cpu, ram, battery)
        # 在這裡更新文字顯示
        # 可以從其他資料源取得數據並更新到Label中
        cpu_value = cpu  # 假設從資料源取得 CPU 數值
        ram_value = ram  # 假設從資料源取得 RAM 數值
        battery_value = battery  # 假設從資料源取得電池數值
        demand_value = demand  # 假設從資料源取得需求數值

        self.label_cpu.text = f'CPU: {cpu_value:2.2f}'
        self.label_ram.text = f'RAM: {ram_value:2.2f}'
        self.label_battery.text = f'Battery: {battery_value:2.2f}'
        self.label_demand.text = f'Demand: {demand_value:2.2f}'

    def update_clock(self, dt):
        # 更新時鐘顯示
        current_time = datetime.now().strftime('%H:%M:%S')
        self.label_clock.text = f'Time: {current_time}'

    def switch_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'page1'  # 切換到 'page2'



class MessageBox(Popup):
    def __init__(self, message, **kwargs):
        super(MessageBox, self).__init__(**kwargs)
        self.title = 'Read Me'
        self.auto_dismiss = True
        message = "After pressing the start button,\n the program automatically \ndetects the values of CPU, \nRAM, and Battery, and then \nuses fuzzy control to convert \nthem into a charging demand \nlevel ranging from 0 to 10.\nA higher level indicates a \ngreater need for charging."

        # 訊息內容
        label = Label(text=message, font_size=30)

        
        # 關閉按鈕
        button = Button(text='Home', size_hint=(None, None), size=(150, 50))
        button.bind(on_release=self.dismiss)
        
        # 將內容和按鈕添加到視窗中
        self.content = FloatLayout()
        self.content.add_widget(label)
        self.content.add_widget(button)


class MyApp(App):
    def build(self):
        # 設定視窗大小
        Window.size = (500, 300)
        Window.minimum_size = (500, 300)
        Window.size_hint = (None, None)
        # 建立 ScreenManager
        sm = ScreenManager()

        # 設定視窗標題
        self.title = 'Fuzzy Monitor'
        self.icon = "Fuzzy_project/icon.png"
        
        
        
        
        # 建立兩個 Screen
        page1 = Screen(name='page1')
        page2 = Screen(name='page2')
        
        # 在每個 Screen 中添加對應的 Widget
        page1.add_widget(Page1())
        page2.add_widget(Page2())
        
        # 將兩個 Screen 添加到 ScreenManager 中
        sm.add_widget(page1)
        sm.add_widget(page2)
        
        
        
        return sm

if __name__ == '__main__':
    MyApp().run()