import os
import sqlite3
import sys

import pytest


# Ensure project root is importable when running `pytest` from anywhere.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def create_schema(con: sqlite3.Connection) -> None:
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
    con.commit()


@pytest.fixture()
def temp_db_path(tmp_path, monkeypatch):
    db_path = tmp_path / "ims_test.db"
    con = sqlite3.connect(db_path)
    create_schema(con)
    con.close()

    monkeypatch.setattr("db.db_helper.DB_PATH", str(db_path))
    return db_path


@pytest.fixture()
def temp_bills_dir(tmp_path, monkeypatch):
    bills_dir = tmp_path / "bills"
    bills_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("modules.sales.BILL_DIR", str(bills_dir))
    return bills_dir

