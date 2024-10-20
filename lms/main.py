import importlib
from flask import app
import kivy

from kivy.app import App
from kivy.lang import Builder
import requests

class MyApp(App):
    def build(self):
        Builder.load_file('main.kv')
        return super().build()

if __name__ == '_main_':
    MyApp().run()


from kivy.uix.button import Button
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical') # type: ignore
        label = Label(text='Hello from Kivy!')
        button = Button(text='Fetch Data')
        button.bind(on_press=self.fetch_data)
        layout.add_widget(label)
        layout.add_widget(button)
        return layout

    def fetch_data(self, instance):
        response = requests.get('http://localhost:5000/data')
        data = response.json()
        self.root.ids.label.text = f"Data from backend: {data}"

if __name__ == '_main_':
    MyApp().run()