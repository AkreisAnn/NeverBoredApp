import sqlite3


def conn_to_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE if not exists user(
            			name text,
            			email text,
            			password text,
            			sports data json
            			)
            		 """)
    conn.commit()
    conn.close()
