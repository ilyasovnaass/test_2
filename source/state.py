from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    waiting_title = State()


class DoneTask(StatesGroup):
    waiting_num = State()
    


class DeleteTask(StatesGroup):
    waiting_num = State()
    