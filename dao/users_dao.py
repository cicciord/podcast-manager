import sqlite3

def get_user_by_email(email):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE email = ?"
    cursor.execute(sql, (email, ))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def get_user_by_id(id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE id = ?"
    cursor.execute(sql, (id, ))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def get_user_username_by_id(id):
    user = get_user_by_id(id)
    return user["username"]

def add_user(new_user):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "INSERT INTO users(username, email, password, is_creator) VALUES(?, ?, ?, ?)"
    
    try:
        cursor.execute(sql, (new_user["username"], new_user["email"], new_user["password"], new_user["is_creator"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success
