import sqlite3
gulds = ["SIR", "KGM","OSO","7NT","TOG","TRB","OOH", "RFR"]

def update_hero(info, ids):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE heros SET name = ?, guild = ?, atk_stat = ? , def_stat = ? , level = ? WHERE id = ?', (info[0], info[1], info[2], info[3], info[4], ids))
    conn.commit()
    cursor.close()
    conn.close()

def try_get_hero(ids):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM heros WHERE id=?', (ids,))
    a = cursor.fetchone()
    cursor.close()
    conn.close
    return a
     
def new_hero(info, ids):
    if info[1] in gulds:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO heros VALUES (?,?,?,?,?,?)', (ids, info[0],info[1],info[2], info[3], info[4]))
        conn.commit()
        cursor.close()
        conn.close()


def addguild(name, ids):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO guilds VALUES (?,?)', (name, ids))
    cursor.close()
    conn.commit()
    conn.close()

def getchat(name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT tg_id FROM guilds WHERE name = ?', (name, ))
    a = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return a

def insert_report(info, ids):
    conn = sqlite3.connect('data.db')
    cur  = conn.cursor()
    cur.execute('INSERT INTO reports VALUES (?,?,?,?,?,?)', (ids, info[0],info[1],info[2], info[3], info[4]))
    conn.commit()
    cur.close()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect('data.db')
    cur  = conn.cursor()
    cur.execute('SELECT * FROM reports')
    reports = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return(reports)

def get_reports(guild):
    conn = sqlite3.connect('data.db')
    cur  = conn.cursor()
    cur.execute('SELECT * FROM reports WHERE guild = ?',(guild,))
    reports = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return(reports)


def clear():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reports')
    cursor.close()
    conn.commit()

def get_all_chats():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM guilds')
    a = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return a

def new_loc(info, ids):
    conn = sqlite3.connect('data.db')
    cur  = conn.cursor()
    cur.execute('INSERT INTO locations VALUES (?,?)', (info, ids))
    conn.commit()
    cur.close()
    conn.close()

def get_loc(name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    print('db loc')
    cursor.execute('SELECT code FROM locations WHERE name = ?', (name, ))
    a = cursor.fetchone()
    print(a)
    conn.commit()
    cursor.close()
    conn.close()
    return a

def get_all_loc():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM locations')
    a = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return a

def clear_loc(name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM locations WHERE name =?',(name,))
    cursor.close()
    conn.commit()