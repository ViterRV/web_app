import sqlite3 as sq

db = sq.connect('emoji.db')
cur = db.cursor()

async def db_start():

    cur.execute('''CREATE TABLE if not EXISTS emoji(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_name text,
    time int,
    emoji text,
    emoji1 text,
    value text,
    what_heppend text)
    ''')
    db.commit()


async def create_profile(user_id,user_name,time):
    cur.execute("INSERT INTO emoji VALUES(?,?,?,?,?,?,?)",(user_id,user_name,time,'','','',''))
    db.commit()

async def edit_profile(state, user_id,user_name,time):
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO emoji (user_id, user_name, time, emoji, emoji1, value, what_heppend) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, user_name, time, data['emoji'], data['emoji1'], data['value'], data['what_heppend'])
        )
        db.commit()

async def read_db(user_id=None):
    if user_id:
        cur.execute(
            "SELECT * FROM emoji WHERE user_id = ?", (user_id,)
        )
        rows = cur.fetchall()
        info = ''
        for row in rows:
            info += (
                f"ID: {row[0]}\n"
                f"Час: {row[3][:19]}\n"
                f"Емоція: {row[4]}, {row[5]}\n"
                f"Бал: {row[6]}\n"
                f"Що сталось: {row[7]}\n\n"
            )
        return info
    else:
        cur.execute("SELECT * FROM emoji ORDER BY user_name")
        rows = cur.fetchall()
        info = ''
        for row in rows:
            info += (
                f"ID: {row[0]}\n"
                f"Ім'я: {row[2]}\n"
                f"Час: {row[3][:19]}\n"
                f"Емоція: {row[4]}, {row[5]}\n"
                f"Бал: {row[6]}\n"
                f"Що сталось: {row[7]}\n\n"
            )

        return info



async def check_record(id,user_id=None):
    if user_id:
        cur.execute("SELECT * FROM emoji WHERE user_id=?",(user_id,))
        rows = cur.fetchall()
    else:
        cur.execute("SELECT * FROM emoji")
        rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(row[0])

    if id in data:
        return True
    else:
        return False







"""async def update(user_id=None):
    records = {}
    if user_id:
        cur.execute(
            "SELECT * FROM emoji WHERE user_id = ?", (user_id,)
        )
        rows = cur.fetchall()

        for row in rows:
            id = row[0]
            info = {
                "ID": row[0],
                "Ім'я": row[2],
                "Час": row[3][:19],
                "Емоція": f"{row[4], row[5]}",
                "Бал": row[6],
                "Що сталось": row[7]
            }
            records[id] = info
        return records
    else:
        cur.execute("SELECT * FROM emoji ORDER BY user_name")
        rows = cur.fetchall()
        for row in rows:
            id = row[0]
            info = {
                "Ім'я": row[2],
                "Час": row[3][:19],
                "Емоція": f"{row[4], row[5]}",
                "Бал": row[6],
                "Що сталось": row[7]
            }
            records[id] = info
        return records

"""

'''records = {}

    if user_id:
        cur.execute(
            "SELECT * FROM emoji WHERE user_id = ?", (user_id,)
        )
        rows = cur.fetchall()
        for row in rows:
            record_id = row[0]
            record_info = {
                "time": row[2][:19],
                "emoji": f"{row[3]}, {row[4]}",
                "value": row[5],
                "what_happened": row[6]
            }
            records[record_id] = record_info
    else:
        cur.execute("SELECT * FROM emoji ORDER BY user_name")
        rows = cur.fetchall()
        for row in rows:
            record_id = row[0]
            record_info = {
                "name": row[1],
                "time": row[2][:19],
                "emoji": f"{row[3]}, {row[4]}",
                "value": row[5],
                "what_happened": row[6]
            }
            records[record_id] = record_info

    return records'''


"""async def update_profile(state,id,user_id,user_name,time):
    async with state.proxy() as data:
        cur.execute("UPDATE emoji SET user_name= '{}',time= '{}', emoji= '{}',emoji1= '{}',value= '{}',what_heppend= '{}' WHERE id = '{}'".format(
            user_id,user_name,time,data['emoji'],data['emoji1'],data['value'],data['what_heppend'],id))
        db.commit()"""

async def update_profile(state, id, user_id, user_name, time):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE emoji SET user_name=?, time=?, emoji=?, emoji1=?, value=?, what_heppend=? WHERE id=?",
            (user_name, time, data['emoji'], data['emoji1'], data['value'], data['what_heppend'], id)
        )
        db.commit()

async def delete_profile(id):
    cur.execute(
            "DELETE FROM emoji WHERE id=?",(id,)
    )
    db.commit()

"""async def create_profile(user_id,user_name,time):
    user = cur.execute("SELECT 1 FROM emoji WHERE user_id =='{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO emoji VALUES(?,?,?,?,?,?,?)",(user_id,user_name,time,'','','',''))
        db.commit()"""
