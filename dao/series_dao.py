import sqlite3
from datetime import date

def get_series(creator_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM series WHERE date <= ? OR creator_id = ? ORDER BY date DESC"
    curr_date = date.today()
    cursor.execute(sql, (curr_date, creator_id))

    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return res

def get_series_titles():
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT title FROM series"
    curr_date = date.today()
    cursor.execute(sql)

    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return res

def get_series_by_category(category):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM series WHERE category = ? AND date <= ? ORDER BY date DESC"
    curr_date = date.today()
    cursor.execute(sql, (category, curr_date))

    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return res

def get_categories():
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT DISTINCT category FROM series WHERE date <= ?"
    curr_date = date.today()
    cursor.execute(sql, (curr_date, ))

    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return res

def get_series_by_id(id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM series WHERE id = ?"
    cursor.execute(sql, (id, ))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def add_series(new_series):
    success = False
    id = 0

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "INSERT INTO series(title, category, date, text, creator_id) VALUES(?, ?, ?, ?, ?)"
    
    try:
        cursor.execute(sql, (new_series["title"], new_series["category"], new_series["date"], new_series["text"], new_series["creator_id"]))
        conn.commit()
        success = True
        id = cursor.lastrowid
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return (success, id)

def update_series(series_updated):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "UPDATE series SET title=?, category=?, date=?, text=? WHERE id=?"
    
    try:
        cursor.execute(sql, (series_updated["title"], series_updated["category"], series_updated["date"], series_updated["text"], series_updated["id"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def del_series(series_id):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    sql = "DELETE FROM series WHERE id = ?"
    
    try:
        cursor.execute(sql, (series_id, ))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success
