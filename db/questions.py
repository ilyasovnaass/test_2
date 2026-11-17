from db.database import get_db
from db.queries import GET_ALL_QUESTIONS, GET_QUESTION_BY_ID, CREATE_QUESTION, DELETE_QUESTION


# execute() -- (в переводе - выполнить), он выполняет определенные функции в базе данных: окрывает(для чтения), удаляет, добавляет, обновляет/изменяет
# eсть два вида использования execute(), это с параметрами и без (в функции get_all_questions() без параметров, тоесть только для чтения, а в функции
# create_question() - с параметрами, тоесть для введения изменений в базу данных, напрмер добавить или удалить таблицу или колонку)

# commit() -- сохраняет изменения в базе данных, если функция execute() было использована c параметрами, после нее нужно объязательно сохранять изменения,

# функция и метод. в чем отличие? функция работает сам по себе например: commit(), close(), а метод, он функция но только принадлежит чему то, например:
# conn.commit(), conn.close() итд.

# функции fetchone(), fetchall(), fetchmany() -- в чем разница и какава их роль в коде? Они вытаскивают данные в базе по определенному количеству
# fetch в переводе означает "пойти за ...", в нашем случаем fetchone - "пойти за одним" - т.е вытаскивает из базы одну колонку в виде кортежа 
# fetchmany() -- он вытаскивает опреденное количество информации, у него есть один параметр size, если в базе миллион данных и не вариант вытаскивать
# всех сразу (fetchall()), но и по одному не вариант (fetchone()), тут пригодиться fetchmany() к которому можно передавать количество нужных нам колонок



def get_all_questions():    # создаем синхронную функцию 
    conn = get_db()     # открываем базу и сохраняем ее в переменную conn
    rows = conn.execute(GET_ALL_QUESTIONS).fetchall()   # создаем таблицу в базе и сохраняем ее в переменную rows
    conn.close()    # закрываем базу
    return [dict(r) for r in rows]  # вернуть результат, превратив ее в обычный словарь


def get_question(question_id: int):     
    conn = get_db()     
    row = conn.execute(GET_QUESTION_BY_ID, (question_id, )).fetchone()  
    conn.close()    
    return dict(row) if row else None   


def create_question(question_text, correct_answer):    
    conn = get_db()     
    conn.execute(CREATE_QUESTION, (question_text, correct_answer))  
    conn.commit()    # здесь commit() нужен потому что мы ввели изменения в таблицу
    conn.close()

def delete_question(question_id):   
    conn = get_db()
    conn.execute(DELETE_QUESTION, (question_id, ))  
    conn.commit()
    conn.close()