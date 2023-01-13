import sqlite3

def add_follow(new_follow):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "INSERT INTO follows(user_id, series_id) VALUES(?, ?)"
    
    try:
        cursor.execute(sql, (new_follow["user_id"], new_follow["series_id"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def delete_follow(id):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    sql = "DELETE FROM follows WHERE id = ?"

    try:
        cursor.execute(sql, (id, ))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def is_following(user_id, series_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM follows WHERE user_id = ? AND series_id = ?"
    cursor.execute(sql, (user_id, series_id))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def get_follows(user_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM follows WHERE user_id = ?"
    cursor.execute(sql, (user_id, ))

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res