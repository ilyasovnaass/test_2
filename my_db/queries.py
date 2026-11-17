# USERS
# TASKS


CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT,
        name TEXT
    )
''' 

CREATE_TASKS_TABLE = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        is_done TEXT NOT NULL, 

        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''' 


INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username, name) VALUES (?, ?, ?)'

GET_USER_BY_TG_ID = '''
    SELECT id, telegram_id, username, name
    FROM users 
    WHERE telegram_id = ?
'''


INSERT_TASKS = 'INSERT INTO tasks (user_id, title) VALUES (?, ?)'



GET_TASKS_BY_USER = '''
    SELECT 
        tasks.id,
        tasks.title,
        tasks.is_done
        FROM tasks 
        INNER JOIN users 
            ON tasks.user_id = users.id
        WHERE users.telegram_id = ?
        ORDER BY tasks.id 
'''



GET_TASK_BY_NUM = '''
    SELECT tasks.id, tasks.title, tasks.is_done 
    FROM tasks 
    INNER JOIN users 
        ON tasks.user_id = users.id 
    WHERE users.telegram_id = ? 
    ORDER BY tasks.id 
'''



MARK_TASK_DONE = '''UPDATE tasks SET is_done = 1 WHERE id = ?'''


DELETE_TASK = '''DELETE FROM tasks WHERE id = ? '''



GET_STATS = '''
    SELECT is_done, COUNT(*) FROM tasks 
    INNER JOIN users 
        ON tasks.user_id = users.id 
    WHERE users.telegram_id = ? 
    GROUP BY is_done
'''

