from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.config import Config

import json
import string
from random import choice, shuffle, randint
from os.path import exists
from sys import exit

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '350')
Config.set('graphics', 'resizable', 'False')



class View(Screen):
    website_input = ObjectProperty(None)
    email_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    new_data = None
    file = None
    file_exists = None
    path = "log.json"
    color = 1,1,1, 0.1
    btn_color = 1,1,1, 0.3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_pw(self):
        letters = string.ascii_uppercase + string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation
        # print(letters)
        pw_letters = [choice(letters) for _ in range(randint(8,10))]
        pw_numbers = [choice(numbers) for _ in range(randint(1,2))]
        pw_symbols = [choice(symbols) for _ in range(randint(1,2))]

        password_list = pw_letters + pw_numbers + pw_symbols
        shuffle(password_list)
        self.password_input.text = "".join(password_list)
    def save_profile(self):
        website_text = self.website_input.text
        email_text = self.email_input.text
        password_text = self.password_input.text
        # print(website_text, email_text)
        if email_text != '' and website_text != '' and password_text != '':
            self.new_data = {
                website_text: {
                    'email': email_text,
                    'password': password_text
                }
            }
            # print(self.new_data)
            self.save_to_file()

    def save_to_file(self):
        self.load_file()
        self.file = open(self.path, "r")
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            self.file = open(self.path, "w+")
            json.dump(self.new_data, self.file, indent=4)
        else:
            self.file = open(self.path, mode="w")
            data.update(self.new_data)
            json.dump(data, self.file, indent=4)
        finally:
            self.file.close()

    def create_file(self):
        self.file = open(self.path, "x")

    def load_file(self):
        self.file_exists = exists(self.path)
        if not self.file_exists:
            self.create_file()

    def load_profile(self):
        self.load_file()
        keyword = self.website_input.text
        if keyword != '':
            self.file = open(self.path, mode='r')
            try:
                data = json.load(self.file)
            except json.decoder.JSONDecodeError:
                exit()
            else:
                if keyword in data:
                    self.email_input.text = data[keyword]['email']
                    self.password_input.text = data[keyword]['password']
                    # p = BoxLayout(orientation="vertical")
                    p = PasswordPopup()
                    a = Popup(title='YOUR LOGIN INFO', content=p, size_hint=(None, None), size=(450, 200))
                    p.email_value = self.email_input.text
                    p.pass_value = self.password_input.text
                    p.close_btn.bind(on_press=a.dismiss)
                    a.open()

                else:
                    print('keyword is not in the log.')

class PasswordPopup(BoxLayout):
    close_btn = ObjectProperty(None)
    email_value = StringProperty('')
    pass_value = StringProperty('')
    pass

class PassManagerApp(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(View(name='profiles'))











PassManagerApp().run()
