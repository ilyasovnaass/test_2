from my_db.db import get_db
from my_db.queries import GET_STATS


def get_stats(telegram_id: int):
    conn = get_db()
    rows = conn.execute(GET_STATS, (telegram_id, )).fetchall()
    conn.close()

    stats = {'total': 0, 'done': 0, 'not_done': 0}
    for is_done, count in rows:
        if is_done == 1:
            stats['done'] = count
        else:
            stats['not_done'] = count
        stats['total'] += count
    return stats

