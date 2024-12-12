import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

def outputDeliveries():
    cursor.execute('''
SELECT * FROM deliveries
    ''')
    deliveries = cursor.fetchall()
    for delivery in deliveries:
        print(delivery)

def output():
    cursor.execute('''
PRAGMA table_info(deliveries);
        ''')
    columns = cursor.fetchall()

    for column in columns:
        print(column)
def delete():
    cursor.execute('''
DROP TABLE IF EXISTS deliveries
    ''')
    db.commit()

def create():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deliveries (
        id INTEGER PRIMARY KEY,
        sender_name TEXT NOT NULL,
        sender_address TEXT NOT NULL,
        getter_name TEXT NOT NULL,
        getter_address TEXT NOT NULL,
        info TEXT NOT NULL,
        status TEXT NOT NULL,
        track TEXT NOT NULL
    )
    ''')

create()

db.commit()
db.close()