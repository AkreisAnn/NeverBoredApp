import sqlite3
import json
import random


def check_if_suggest(name):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    for row in c.execute("Select * from user"):
        us_name = row[0]
        if us_name == name:
            sports = json.loads(row[3])
            if len(sports) == 0:
                return -1
    return 1


def choose_sport(name):
    con = sqlite3.connect('database.db')
    c = con.cursor()
    for row in c.execute("Select * from user"):
        us_name = row[0]
        if us_name == name:
            sports = json.loads(row[3])
            break
    n = random.randint(0, len(sports)-1)
    ind = sports[n]
    for row in c.execute("Select * from sports"):
        id = row[2]
        if id == ind:
            sport = [row[0], row[3]]
            break
    return sport