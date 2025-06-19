import sqlite3

DB_PATH = "./test.sqlite"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # enables dict-like rows
    return conn


def query_db(query, args=(), one=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return dict(rows[0]) if one and rows else [dict(r) for r in rows]
