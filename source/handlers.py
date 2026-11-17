from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from my_db.users import get_user, create_user 
from my_db.task import add_tasks, get_tasks, get_task_by_num, mark_task_done, delete_task, get_stats 
from source.state import AddTask, DoneTask, DeleteTask
from source.keyboards import inline_buttons


router = Router()


@router.message(CommandStart()) 
async def cmd_start(message: Message): 
    user = get_user(message.from_user.id)
    if not user:
        create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )
    await message.answer(f'Привет, {message.from_user.first_name}! Я ваш бот для задач.\n\nНапишите /add, чтобы добавить задачу.')
    print(f'Пользователь {message.from_user.first_name} написал команду start.')



@router.message(Command('add')) 
async def cmd_add(message: Message, state: FSMContext): 
    await message.answer('Напишите название задачи:') 
    await state.set_state(AddTask.waiting_title)


@router.message(AddTask.waiting_title) 
async def save_task(message: Message, state: FSMContext): 
    user = get_user(message.from_user.id) 
    add_tasks(user['id'], message.text) 
    await message.answer(f'Задача добавлена: {message.text}') 
    await state.clear()


@router.message(Command('tasks')) 
async def cmd_tasks(message: Message): 
    tasks = get_tasks(message.from_user.id)
    if not tasks:
        await message.answer('У вас пока нет задач. Напишите /add')
        return


    text = 'Ваши задачи:\n\n'
    for num, task in enumerate(tasks, start=1):
        icon = '✅' if task['is_done'] else '⬜️'
    text += f'{num}. {icon} {task['title']}\n'
    await message.answer(text, 
                         reply_markup=inline_buttons
                         )

@router.callback_query(F.data == 'done') 
async def callback_done(callback: CallbackQuery): 
    await callback.answer('Отмечено как выполненное ✅') 
    await callback.message.answer('Задача выполнена! Посмотрите обновленный список: /tasks')

@router.message(Command('done')) 
async def cmd_done(message: Message, state: FSMContext): 
    await message.answer('Напишите номер задачи, которую выполнили:') 
    await state.set_state(DoneTask.waiting_num)


@router.message(DoneTask.waiting_num) 
async def done_task(message: Message, state: FSMContext): 
    task = get_task_by_num(message.from_user.id, int(message.text))
    if not task:
        await message.answer('Такой задачи нет')
    else:
        mark_task_done(task['id'])
    await message.answer(f'Задача выполнена: {task['title']} ✅')
    await state.clear()


@router.message(Command('delete')) 
async def cmd_delete(message: Message, state: FSMContext): 
    await message.answer('Напишите номер задачи, которую  хотите удалить:') 
    await state.set_state(DeleteTask.waiting_num)


@router.message(DeleteTask.waiting_num)
async def delete_task_handler(message: Message, state: FSMContext): 
    if not message.text.isdigit(): 
        await message.answer('Нужно ввести число, например: 1') 
        return
    
    task = get_task_by_num(message.from_user.id, int(message.text))

    if not task:
        await message.answer('Такой задачи нет')
    else:
        delete_task(task['id'])
    await message.answer('Задача удаленa!')

    await state.clear()

@router.message(Command('stats')) 
async def cmd_stats(message: Message): 
    stats = get_stats(message.from_user.id) 
    await message.answer( 
        f'Статистика:\n\nВсего: {stats['total']}\nВыполнено: {stats['done']}\nНе выполнено: {stats['not_done']}' 
    )