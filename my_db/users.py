from my_db.db import get_db
from my_db.queries import INSERT_USER, GET_USER_BY_TG_ID

def get_user(telegram_id: int):
    conn = get_db()
    user = conn.execute(GET_USER_BY_TG_ID, (telegram_id,)).fetchone()
    conn.close()
    return dict(user) if user else None



def create_user(telegram_id: int, username: str, name: str):
    conn = get_db()
    conn.execute(INSERT_USER, (telegram_id, username, name))
    conn.commit()
    conn.close()
    return get_user(telegram_id)



