from my_db.db import get_db
from my_db.queries import INSERT_TASKS, GET_TASKS_BY_USER, GET_TASK_BY_NUM, MARK_TASK_DONE, DELETE_TASK, GET_STATS



def add_tasks(user_id: int, title: int, is_done=0):
    conn = get_db()
    conn.execute('INSERT INTO tasks (user_id, title, is_done) VALUES (?, ?,?)', (user_id, title, is_done))
    conn.commit()
    conn.close()


def get_tasks(telegram_id: int):
    conn = get_db()
    tasks = conn.execute(GET_TASKS_BY_USER, (telegram_id, )).fetchall()
    conn.commit()
    conn.close()
    return [dict(task) for task in tasks]


def get_task_by_num(telegram_id: int, num: int):
    conn = get_db()
    task = conn.execute(GET_TASK_BY_NUM, (telegram_id, )).fetchall()
    conn.commit()
    conn.close()
    if 1 <= num <= len(task):
        return dict(task[num - 1])
    return None


def mark_task_done(task_id: int):
    conn = get_db()
    conn.execute(MARK_TASK_DONE, (task_id, ))
    conn.commit()
    conn.close()


def delete_task(task_id: int):
    conn = get_db()
    conn.execute(DELETE_TASK, (task_id, ))
    conn.commit()
    conn.close()


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




