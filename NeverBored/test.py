import sqlite3
import json


def test(us_sports, name):
    sports = []
    con = sqlite3.connect('database.db')
    c = con.cursor()
    for row in c.execute("Select * from sports"):
        requirements = json.loads(row[1])
        id = row[2]
        check = 0
        for el in requirements:
            if us_sports[check] > requirements[check]:
                check += 1
            else:
                break
            if check == 7:
                sports.append(id)

    sports = json.dumps(sports)
    c.execute("""Update user set sports=? where name=?""", (sports, name))
    con.commit()


