import sqlite3
from datetime import date

def add_podcast(new_podcast):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "INSERT INTO podcasts(title, date, description, series_id) VALUES(?, ?, ?, ?)"
    
    try:
        cursor.execute(sql, (new_podcast["title"], new_podcast["date"], new_podcast["description"], new_podcast["series_id"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_podcast(new_podcast):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "UPDATE podcasts SET title=?, date=?, description=? WHERE id=?"
    
    try:
        cursor.execute(sql, (new_podcast["title"], new_podcast["date"], new_podcast["description"], new_podcast["id"]))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_podcasts(series_id, creator_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT podcasts.*, creator_id FROM podcasts LEFT JOIN series ON podcasts.series_id = series.id WHERE series_id = ? AND ( podcasts.date <= ? OR creator_id = ? ) ORDER BY date ASC"
    curr_date = date.today()
    cursor.execute(sql, (series_id, curr_date, creator_id))

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_podcasts_titles(series_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT title FROM podcasts WHERE series_id = ?"
    cursor.execute(sql, (series_id, ))

    res = cursor.fetchall()

    cursor.close()
    conn.close()

    return res

def get_podcast(podcast_id):
    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM podcasts WHERE id = ?"
    cursor.execute(sql, (podcast_id, ))

    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res

def del_podcast(podcast_id):
    success = False

    conn = sqlite3.connect("db/series.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    sql = "DELETE FROM podcasts WHERE id = ?"

    try:
        cursor.execute(sql, (podcast_id, ))
        conn.commit()
        success = True
    except Exception as e:
        print("ERROR", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success
