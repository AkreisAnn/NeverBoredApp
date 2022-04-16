from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from test import test
from choose_sport import choose_sport, check_if_suggest
from login_create_account import create_account, login_check, check_if_available
from conn_to_database import conn_to_database


class WelcomeScreen(Screen):
    pass


class LogInScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def set_default(self):
        self.email.text = ''
        self.password.text = ''

    def invalid_pwd(self):
        popup = Popup(title='Invalid name/email/password',
                      content=Label(text="Enter valid name/email and password."),
                      size_hint=(None, None), size=(400, 300), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()

    def submit(self):
        name = login_check(self.email.text, self.password.text)
        if name == -1:
            self.invalid_pwd()
        else:
            ref_to_main = self.manager.get_screen("main")
            ref_to_main.ids.account_spinner.text = name
            ref_to_main.ids.hello_user.text = "Hello "+name+"!"
            sm.current = "main"


class CreateAccountScreen(Screen):
    email = ObjectProperty(None)
    nickname = ObjectProperty(None)
    password = ObjectProperty(None)

    def set_default(self):
        self.email.text = ''
        self.nickname.text = ''
        self.password.text = ''

    def show_requirements(self):
        popup = Popup(title='Invalid name/email/password',
                      content=Label(text="Requirements:\n -password must be at least 6 characters long\n"
                                         " -name must be at least 3 characters long\n -you must enter an email"),
                      size_hint=(None, None), size=(400, 300), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()

    def create_success(self):
        sm.current = 'welcome'
        popup = Popup(title='Account created',
                      content=Label(text="Your account has been successfully created.\nYou can Log In now."),
                      size_hint=(None, None), size=(400, 300), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()

    def not_available(self):
        popup = Popup(title='Name not available',
                      content=Label(text="This name is already taken."),
                      size_hint=(None, None), size=(400, 300), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()

    def create(self):
        if len(self.password.text) < 6 or len(self.nickname.text) < 3 or len(self.email.text) == 0:
            self.show_requirements()
        else:
            check = check_if_available(self.nickname.text)
            if check == 1:
                create_account(self.nickname.text, self.email.text, self.password.text, [])
                self.create_success()
            else:
                self.not_available()


class MainAppScreen(Screen):
    def log_out_success(self):
        popup = Popup(title='Logged Out',
                      content=Label(text="Your have successfully logged out."),
                      size_hint=(None, None), size=(400, 300), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()
        self.ids.account_spinner.text = "Name"
        sm.current = 'welcome'

    def take_a_test(self):
        sm.current = 'main'
        popup = Popup(title='Take a test',
                      content=Label(text="You have to take a test first so we can propose\nthe best sport for you."),
                      size_hint=(None, None), size=(450, 350), background_color=(0.35, 0.9, 0.9, 1))
        popup.open()

    def check_if_suggest(self):
        check = check_if_suggest(self.ids.account_spinner.text)
        if check == -1:
            self.take_a_test()
        else:
            sm.current = 'suggest'

    def spinner_account(self, value):
        if value =="Settings":
            pass
        elif value == "Log Out":
            self.log_out_success()


class TestScreen(Screen):
    group = NumericProperty(0.0)
    joints = NumericProperty(0.0)
    out = NumericProperty(0.0)
    winter = NumericProperty(0.0)
    shoulder = NumericProperty(0.0)
    animal = NumericProperty(0.0)
    water = NumericProperty(0.0)

    def set_default(self):
        self.ids.group_slider.value = 0.0
        self.ids.joints_slider.value = 0.0
        self.ids.out_slider.value = 0.0
        self.ids.winter_slider.value = 0.0
        self.ids.shoulder_slider.value = 0.0
        self.ids.animal_slider.value = 0.0
        self.ids.water_slider.value = 0.0

    def send_success(self):
        popup = Popup(title='Sending successful',
                    content=Label(text="Your answers have been sent.\nYou can go back and see what we propose for you."),
                    size_hint=(None, None), size=(450, 350), background_color=(99/255, 48/255, 128/255, 0.9))
        popup.open()

    def set_sports(self):
        ref_to_main = self.manager.get_screen("main")
        name = ref_to_main.ids.account_spinner.text
        sports = [self.group, self.joints, self.out, self.winter, self.shoulder, self.animal, self.water]
        test(sports, name)
        print(self.group)
        print(self.joints)
        print(self.out)
        print(self.winter)
        print(self.shoulder)
        print(self.animal)
        print(self.water)
    pass


class SuggestSportScreen(Screen):

    def set_default(self):
        self.ids.sport_name.text = "Calculating..."
        self.ids.sport_desc.text = 'Calculating...'

    def choose_sport(self):
        ref_to_main = self.manager.get_screen("main")
        name = ref_to_main.ids.account_spinner.text
        sport = choose_sport(name)
        self.ids.sport_name.text = sport[0]
        self.ids.sport_desc.text = sport[1]


class WindowManager(ScreenManager):
    pass


sm = Builder.load_file('NeverBored.kv')


class NeverBoredApp(App):
    def build(self):
        conn_to_database()
        return sm


if __name__ == "__main__":
    NeverBoredApp().run()

