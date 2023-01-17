import sqlite3

def post_comment(comment):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT date FROM podcasts WHERE id = ? AND date <= ?"
    cursor.execute(sql, (comment["podcast_id"], comment["date"]))
    allowed = cursor.fetchone()

    if allowed:    
        sql = "INSERT INTO comments(comment, date, user_id, podcast_id) VALUES(?, ?, ?, ?)"
        
        try:
            cursor.execute(sql, (comment["comment"], comment["date"], comment["user_id"], comment["podcast_id"]))
            conn.commit()
            success = True
        except Exception as e:
            print("ERROR", e)
            conn.rollback()

        cursor.close()
        conn.close()

    return success

def update_comment(comment):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "UPDATE comments SET comment=?, date=? WHERE id=?"
        
    try:
        cursor.execute(sql, (comment["comment"], comment["date"], comment["id"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

        cursor.close()
        conn.close()

    return success

def get_comments(podcast_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM comments WHERE podcast_id = ?"
    cursor.execute(sql, (podcast_id, ))

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_comment(comment_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM comments WHERE id = ?"
    cursor.execute(sql, (comment_id, ))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def del_comment(comment_id):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    sql = "DELETE FROM comments WHERE id = ?"

    try:
        cursor.execute(sql, (comment_id, ))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success
