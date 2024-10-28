from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Customizable themes, transitions, and page settings
        self.theme = {
            'background_color': (0.1, 0.1, 0.1, 1),  # Dark background
            'button_color': (0.2, 0.6, 0.9, 1),      # Custom button color
            'text_color': (1, 1, 1, 1),              # White text
            'transition': 'fade',  # Options: 'fade', 'slide'
        }
        self.levels = ['Beginner', 'Intermediate', 'Advanced']  # Dynamic level names

    def build(self):
        Window.clearcolor = self.theme['background_color']
        
        # Choose transition dynamically
        transition_type = FadeTransition() if self.theme['transition'] == 'fade' else SlideTransition()
        
        sm = ScreenManager(transition=transition_type)
        sm.add_widget(RegistrationPage(name='registration', theme=self.theme))
        sm.add_widget(HomePage(name='home', levels=self.levels, theme=self.theme))
        
        # Add pages dynamically from the levels
        for level in self.levels:
            sm.add_widget(LevelPage(name=level.lower(), level_name=level, theme=self.theme))

        return sm

class CustomButton(Button):
    """Custom button to allow more styling."""
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.background_color = theme['button_color']
        self.color = theme['text_color']
        self.font_size = 18

class RegistrationPage(Screen):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Adjusted TextInput properties for smaller size
        self.username_input = TextInput(
            hint_text='Username', 
            multiline=False,
            size_hint=(1, 0.15),  # Smaller height
            font_size=18  # Reduced font size
        )

        self.password_input = TextInput(
            hint_text='Password', 
            password=True, 
            multiline=False,
            size_hint=(1, 0.15),  # Smaller height
            font_size=18  # Reduced font size
        )

        # Custom button for registration
        register_button = CustomButton(
            text='Register', 
            theme=theme, 
            size_hint=(1, 0.15)  # Button height matches input fields
        )
        register_button.bind(on_press=self.register)

        # Add widgets to layout
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            print(f"User {username} registered with password {password}")
            self.manager.current = 'home'
        else:
            print("Please enter a username and password.")

class HomePage(Screen):
    def __init__(self, levels, theme, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        for level in levels:
            button = CustomButton(text=level, theme=theme)
            button.bind(on_release=lambda instance, lvl=level: self.go_to_level(lvl.lower()))
            layout.add_widget(button)

        back_button = CustomButton(text='Logout', theme=theme, on_press=self.logout)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_level(self, level):
        self.manager.current = level

    def logout(self, instance):
        self.manager.current = 'registration'

class LevelPage(Screen):
    """Reusable page for different learning levels."""
    def __init__(self, level_name, theme, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text=f"Welcome to the {level_name} Page!", color=theme['text_color']))

        back_button = CustomButton(text='Back to Home', theme=theme, on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

if __name__ == '__main__':
    MyApp().run()
