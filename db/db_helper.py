import sqlite3
import os
from config import DB_PATH

def db_connect():
    con = sqlite3.connect(DB_PATH)
    return con