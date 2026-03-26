import sqlite3
import os
from config import DB_PATH

def db_connect():
    con = sqlite3.connect(DB_PATH)
    return con


def run_query(command: tuple, fetch=False):

    #Execute a SQL command safely.
    if not isinstance(command, tuple) or len(command) != 2:
        return {"ok": False, "data": None, "error": "Command must be a tuple: (sql, params)"}

    sql, params = command

    con = db_connect()
    try:
        cur = con.cursor()
        cur.execute(sql, params)

        data = cur.fetchall() if fetch else None
        con.commit()
        return {"ok": True, "data": data, "error": None}

    except Exception as e:
        con.rollback()
        return {"ok": False, "data": None, "error": str(e)}

    finally:
        
        con.close()

def is_admin(user_type):
    return user_type == "Admin"