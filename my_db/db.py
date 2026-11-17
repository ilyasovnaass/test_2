import sqlite3

from my_db.queries import CREATE_USERS_TABLE, CREATE_TASKS_TABLE
from config import DATA_BASE

def get_db():
    conn = sqlite3.connect(DATA_BASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)
    conn.execute(CREATE_TASKS_TABLE)
    conn.commit()
    conn.close()