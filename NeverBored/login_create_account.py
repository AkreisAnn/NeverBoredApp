import sqlite3
import json


def create_account(name, email, pwd, sports):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("INSERT INTO user VALUES (:name, :email, :password, :sports)", {
        'name': name,
        'email': email,
        'password': pwd,
        'sports': json.dumps(sports),
    })
    con.commit()


def login_check(nick, pwd):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    for row in c.execute("Select * from user"):
        name = row[0]
        email = row[1]
        password = row[2]
        if (nick == name or nick == email) and pwd == password:
            return name
        print(nick)
        print(name)
    return (-1)


def check_if_available(nick):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    for row in c.execute("Select * from user"):
        name = row[0]
        if nick == name:
            return -1
    return 1