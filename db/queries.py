# Создаем запросы для создания таблиц:
# USERS
# QUESTIONS
# RESULTS



CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
'''     # CREATE_USERS_TABLE -- создаем переменную с тройными кавычками, потому что запрос будет длинным, на несколько строк
# CREATE TABLE IF NOT EXISTS users -- создать таблицу users, если ее еще не создавали (IF NOT EXISTS -- если не существует)
# id - имя колонки; INTEGER - тип данных (целое число); PRIMARY KEY -- главный ключ, уникальный номер каждой строки
# AUTOINCREMENT -- SQLite сам будет ставить id, не надо писать вручную
# telegram_id -- id человека в Телеграме. приходит от message.from_user.id; NOT NULL -- поле не может быть пустым, без него строку не сохранить
# UNIQUE -- в таблице не может быть двух одинаковых telegram_id. Один человек = одна строка
# username TEXT -- useraname человека в текстовом порядке, также тут нет NOT NULL значит поле может быть пустым, если у человек нет username
# ЭТА ТАБЛИЦА -- СПИСОК ВСЕХ, КТО ХОТЬ РАЗ НАЖАЛ /start



CREATE_QUESTIONS_TABLE = '''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        correct_answer TEXT NOT NULL
    )
'''



CREATE_RESULTS_TABLE = '''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_correct BOOLEAN NOT NULL DEFAULT 0,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    )
'''
# user_id -- это id человека в таблице users, а question_id -- это id вопроса из таблицы questions
# BOOLEAN -- в SQLite это на самом деле 0 или 1; DEFAULT 0 -- если не указать по умолчанию будет 0, то есть "неправильно"
# FOREIGN KEY -- внешний ключ, связывает одну таблицу с другой
# FOREIGN KEY (user_id) REFERENCES userd(id) ON DELETE CASCADE -- гарантирует, что результат нельзя записать для несуществующего пользователя.
# REFERENCES -- отсылается на колонку id из таблицы users или questions
# Если пользователя удалят из users, все его ответы в results удалятся автоматически (ON DELETE CASCADE)



# CRUD -- CREATE-READ-UPDATE-DELETE -- это 4 базовые операции с базой


#1 Read (ключевое слово - SELECT):

GET_USER_BY_TG_ID = 'SELECT * FROM users WHERE telegram_id = ?'    # находит  и возвращает данные пользователя

#2 Create (ключевое слово - INSERT):

INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)'   # добавляет нового пользователя в таблицу

# -- Домашка --

#3 Update (ключевое слово - UPDATE): 

UPDATE_USER_USERNAME = 'UPDATE users SET username = ? WHERE telegram_id = ?'   # меняет данные существуещего пользователя, например его ник

#4 Delete (ключевое слово DELETE):

DELETE_USER = 'DELETE FROM users WHERE telegram_id = ?'    # удаляет запись пользователя из базы



# --QUESTIONS--

GET_ALL_QUESTIONS = 'SELECT * FROM questions'   # взять/выбрать все вопросы
GET_QUESTION_BY_ID = 'SELECT FROM * questions WHERE id = ?'     # взять один вопрос по его id
UPDATE_QUESTION = 'UPDATE questions SET question_text = ?'      # изменить/обновить текст вопроса
DELETE_QUESTION = 'DELETE FROM questions WHERE id = ?'      # удалить вопрос
INSERT_QUESTION = 'INSERT INTO questions (question_text, correct_answer) VALUES (?, ?)'     # добавить новый вопрос, параметры: текст + правильный ответ




# -- RESULTS --

INSERT_RESULT = 'INSERT INTO results (user_id, question_id, is_correct) VALUES (?, ?, ?)'   # добавить/записать как пользователь ответил (его результат)
GET_ALL_RESULTS = 'SELECT * FROM results'   # выбрать все результаты
UPDATE_RESULT = 'UPDATE results SET is_correct = ? WHERE user_id = ? AND question_id = ?'   # исправить ответ
DELETE_RESULTS = 'DELETE FROM results WHERE user_id = ? AND question_id = ?'    # удалить результат
GET_SCORE_BY_USER_ID = 'SELECT COUNT(*) as total, SUM(is_correct) as correct FROM results WHERE user_id = ?'    # подчитывает количество всех ответов, суммирует (правильных) конкретного пользователя



# -- STATS --

GET_HISTORY = '''
    SELECT questions.question_text, results.is_correct
    FROM results
    INNER JOIN users 
        ON users.id = results.user_id
    INNER JOIN questions
        ON questions.id = results.question_id
    WHERE users.telegram_id = ?
    ORDER BY results.id 
    LIMIT 10
'''



GET_TOP = '''
    SELECT u.username,
        COUNT(*) AS total,
        SUM(is_correct) AS correct
    FROM results AS r
    INNER JOIN users AS u
        ON u.id = r.user_id
    GROUP BY r.user_id
    ORDER BY correct DESC
    LIMIT 1
'''



GET_HARDEST = '''
    SELECT q.question_text,
            ROUND(AVG(r.is_correct)*100, 1) AS success_rate
    FROM results AS r
    INNER JOIN questions AS q 
        ON q.id = r.question_id
    GROUP BY r.question_id
    ORDER BY success_rate ASC
    LIMIT 1
'''


# Фильтрация, группировка (GROUP BY), HAVING 

# AS -- используется для назначения временного имени колонке или таблице 
# синтаксис: SELECT column_name AS c FROM table_name 

# ROUND() -- используется для округления чисел до указанного количества знаков после запятой или до ближайшего целого числа 
# синтаксис: ROUND(число, точность)

# ORDER BY() -- используется для сортировки результатов запроса одному или нескольким колонкам. По умолчанию данные сортируются по возрастанию(ASC)
# существует таже сортировка по убыванию (DESC)

# enumerate() -- В Python эта функция используется для одновременного получения индекса и значения элемента при переборе списка, строки или любого другого итерируемого объекта в цикле
# синтаксис: enumerate(iterable, start=0) start -- число с которого начинается подсчет индексов


# -- Агрегатные функции --

# COUNT(*) -- считает количество строк 
# SUM() -- складывает, суммирует все числа в колонке
# AVG() -- находит среднее арифметическое
# MIN() -- ищет минимальное значение 
# MAX() -- ищет максимальное значение


# GROUP BY() --  делит таблицу на группы по какому то признаку

# HAVING() -- фильтрирует уже готовые группы

