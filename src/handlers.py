from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from my_db.users import get_user, create_user
from my_db.task import add_task, get_tasks, get_task_by_num, mark_task_done, delete_task, get_stats
from source.state import AddTask, DoneTask, DeleteTask
from source.keyboards import inline_buttons



router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(telegram_id=message.from_user.id, 
                       username=message.from_user.username or 'Аноним')
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот!\nВот твой резульатат который возвращается с SQL: \n{user}',
        reply_markup=reply_buttons
    )
    print(f'Пользователь {message.from_user.full_name} написал команду start.')



@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        '/start - команда для запуска\n/help - список комманд',
        reply_markup=inline_buttons
        )

    

@router.message(F.text.lower() == 'группа')
async def group(message: Message):
    await message.answer(
        'Твоя группа 71-1!'
    )



@router.callback_query(F.data == 'quiz_start')
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем игру!', show_alert=True)
    questions = get_all_questions()
    if not questions:
        await callback.message.answer('Вопросов нет в базе!')

    await state.update_data(questions=questions, index=0, score=0)   # сохраняем прогресс
    await state.set_state(Quiz.waiting_answer)  # переводим в состояние
    await callback.message.answer(f'Вопрос 1: {questions[0]['question_text']}')



@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data['index']
    score = data['score']
    questions = data['questions']
    user = get_user(telegram_id=message.from_user.id)
    q = questions[index]

    is_correct = message.text.lower() == q['correct_answer']
    save_result(
        user_id=user['id'],
        question_id=q['id'],
        is_correct=is_correct
    )
        
    
    if is_correct:
        score += 1
        await message.answer('Правильно! +1')
        
    else:
        await message.answer(f'Неверно! Правильный ответ: {q['correct_answer']}')

    index += 1
    
    if index >= len(questions):
        await message.answer(
            f'Конец! Счет: {score}/{len(questions)}',
            reply_markup=inline_buttons
            ),
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f'Вопрос {index + 1}: {questions[index]['question_text']}')



@router.callback_query(F.data == 'repeat')
async def repeat(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем заново!', show_alert=True)
    questions = get_all_questions()
    await state.update_data(questions=questions,index=0, score=0)
    await state.set_state(Quiz.waiting_answer)
    await callback.message.answer(f'Вопрос 1: {questions[0]['question_text']}')



@router.message(Command('update'))
async def update(message: Message):
    update_user(message.from_user.id, 'new_username')
    await message.answer('Имя обновлено!')



@router.message(Command('delete'))
async def delete(message: Message):
    delete_user(message.from_user.id)
    await message.answer('Вы удалены из базы данных!')



@router.message(Command('add_question'))
async def add_question(message: Message, state: FSMContext):
    await state.set_state(AddQuestion.question)
    await message.answer('Напишите свой вопрос:')



@router.message(AddQuestion.question)
async def get_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(AddQuestion.correct_answer)
    await message.answer('Введите правильный ответ на свой вопрос:')
    


@router.message(AddQuestion.correct_answer) 
async def add_question_finish(message: Message, state: FSMContext): 
    data = await state.get_data() 
    create_question(data['question'], message.text) 
    await message.answer("Вопрос добавлен!") 
    await state.clear()


@router.message(Command('history'))
async def cmd_history(message: Message):
    history = get_history(telegram_id=message.from_user.id)
    if not history:
        await message.answer('Ответов нету в базе!')
    text = 'Последние ответы:\n\n'
    for i, row in enumerate(history, 1):
        mark = 'Верно' if row['is_correct'] else 'Неверно'
        text += f'{i}. {mark} - {row['question_text']}\n'
    await message.answer(text)



@router.message(Command('top'))
async def cmd_top(message: Message):
    players = get_top()
    if not players:
        message.answer('Ответов нет в базе!')
        return
    text = 'Топ игроков:\n\n'
    for i, p in enumerate(players, 1):
        text += f'{i}. {p['username']} - {p['correct']:{p['total']}}\n'
    await message.answer(text)



@router.message(Command('hardest'))
async def cmd_hardest(message: Message):
    q = get_hardest()
    if not q:
        await message.answer('Вопросов нет в базе!')
        return
    await message.answer(f'Самый сложный вопрос:\n'
                         f'{q['question_text']}\n'
                         f'Правильных: {q['success_rate']}')
    



# @dp.message(F.from_user.id == 5667531193)
# async def user(message: Message):
#     await message.answer(
#         'Привет мой создатель!'
#     )



# Домашка:


@router.message(Command('about'))
async def about(message: Message):
    await message.answer(
        'Я бот-ассистент группы 71-1.\n' \
        'Я умею отвечать на комманды и реагировать на слова.'
    )



@router.message(F.text.lower() == 'пока')
async def echo(message: Message):
    await message.answer(
        f'Пока-пока!'
    )

