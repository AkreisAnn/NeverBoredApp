import sqlite3


def change_pass(name, pwd):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    #print(name)
    #print(pwd)
    c.execute("""Update user set password=? where name=?""", (pwd, name))
    con.commit()


#moze pomoc w rozwiazaniu zadania
#dodanie do klasy MainAppScreen
#    nick = ''
#    def set_name(self):
#        self.nick = self.ids.account_spinner.text
# i wywolanie przy każdym wejściu na ten ekran (mainapp)