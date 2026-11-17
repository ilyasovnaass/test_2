import sqlite3  

from db.queries import CREATE_USERS_TABLE, CREATE_QUESTIONS_TABLE, CREATE_RESULTS_TABLE 
from config import DATABASE
from db.queries import GET_ALL_QUESTIONS, INSERT_QUESTION
from src.questions import QUESTIONS


# импортируем из папки db и из его файла queries.py SQL-запросы на создание таблиц 



def get_db():   # это функция, которая отвечает за подключение к базе данных
    conn = sqlite3.connect(DATABASE)    # в переменной conn  хранится объект подключения, sqlite3.connect(DATABASE) -- sqlite3 соединяется с базой данных
    conn.row_factory = sqlite3.Row      # обычный результат sqlite возвращает в виде кортежа (1, 'Амина', 19) и  
                                        # чтобы вывести результат пришлось бы обращаться к кортежу по индексу, но если данных много это метод вызывает неудобства
                                        # но благодаря row можно обращаться к данным по названиям столбцов (колонок)
    return conn     # возвращает объект подключения


def init_db():   # эта функция отвечает за инициализацию базы данных, тоесть создание необходимых таблиц
    conn = get_db()
    conn.execute(CREATE_USERS_TABLE)    # через метод execute() в sqlite создаются таблицы
    conn.execute(CREATE_QUESTIONS_TABLE)
    conn.execute(CREATE_RESULTS_TABLE)

    # заполняем вопросы если таблица пустая
    
    if not conn.execute(GET_ALL_QUESTIONS).fetchall():
        for q_text, q_answer in QUESTIONS:
            conn.execute(INSERT_QUESTION, (q_text, q_answer))
    conn.commit()   
    conn.close()    

