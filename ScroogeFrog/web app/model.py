import sqlite3 as sq
db = sq.connect('db.db')
cur = db.cursor()
def db_start():

    cur.execute('''CREATE TABLE if not EXISTS contact(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_name text,
    email int,
    phone_number text)
    ''')
    db.commit()

def create_profile(contact_name,email,phone_number):
    cur.execute('''INSERT INTO contact (contact_name, email, phone_number) VALUES(?,?,?)''',
                (contact_name,email,phone_number))
    db.commit()

def read_db(order_by=None):
    if order_by:
        if order_by == 'name':
            cur.execute("SELECT * FROM contact ORDER BY contact_name")
        elif order_by == 'email':
            cur.execute("SELECT * FROM contact ORDER BY email")
    else:
        cur.execute("SELECT * FROM contact")
    profiles = cur.fetchall()
    return profiles


def delete(id):
    cur.execute("DELETE FROM contact WHERE id=?",(id,))
    db.commit()

def update(id, contact_name, email, phone_number):
    cur.execute('''UPDATE contact SET contact_name=?, email=?, phone_number=? WHERE id=?''',
                (contact_name, email, phone_number, id))
    db.commit()
