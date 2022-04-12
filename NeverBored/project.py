from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.spinner import SpinnerOption, Spinner
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import sqlite3


class WelcomeScreen(Screen):
    pass


class LogInScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.email.text != '':
            con = sqlite3.connect('database.db')
            c = con.cursor()
            for row in c.execute("Select * from user"):
                name = row[0]
                email = row[1]
                pwd = row[2]
            if (self.email.text == name or self.email.text == email) and self.password.text == pwd:
                print("Hello ", self.email.text)
                ref_to_main = self.manager.get_screen("main")
                ref_to_main.ids.account_spinner.text = name
                self.email.text = ''
                self.password.text = ''
                sm.current = "main"
        else:
            pass


class CreateAccountScreen(Screen):
    email = ObjectProperty(None)
    nickname = ObjectProperty(None)
    password = ObjectProperty(None)

    def create(self):
        if self.email.text != '' and self.nickname.text != '' and self.password.text != '':
            if len(self.password.text) <6:
                print("Password must be at least 6 characters long ")
            elif len(self.nickname.text) <3:
                print("Name must be at least 3 characters long ")
            elif len(self.email.text)==0:
                print("You must enter an email")
            else:
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                cur.execute("INSERT INTO user VALUES (:name, :email, :password)", {
                    'name': self.nickname.text,
                    'email': self.email.text,
                    'password': self.password.text,
                })
                con.commit()

                print("Accounnt created")
                self.email.text = ''
                self.password.text = ''
                self.nickname.text = ''
                sm.current = 'welcome'
        else:
            pass


class MainAppScreen(Screen):
    def spinner_account(self,value):
        if value =="Settings":
            pass
        elif value =="Log Out":
            print("Successfully logged out")
            self.ids.account_spinner.text = "Name"
            sm.current = 'welcome'


class WindowManager(ScreenManager):
    pass


sm = Builder.load_file('NeverBored.kv')


class NeverBoredApp(App):
    def build(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists user(
        			name text,
        			email text,
        			password text
        			)
        		 """)
        conn.commit()
        conn.close()
        return sm


if __name__ == "__main__":
    NeverBoredApp().run()

