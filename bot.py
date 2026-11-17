import asyncio      # asyncio -- встроенная библиотека python, которая позволяет выполнять асинхронные операции
import logging  # Логи - это информация о работе программы, которая помогает разработчику понять, что происходит внутри программы


from aiogram import Bot, Dispatcher     # Мы импортируем два основных класса из библиотеки aiogram
from source.handlers import router     # импортируем роутер из файла handlers.py, который находится внутри папки src
from aiogram.fsm.storage.memory import MemoryStorage    # MemoryStorage -- это хранилище данных в оперативной памяти
from my_db.db import init_db
from config import TOKEN

# FSM(FiniteStateMachine) -- конечный автомат состояний. Он позволяет боту запоминать, на каком этапе диалога находится пользователь


bot = Bot(token=TOKEN)  # Мы создаем экземпляр класса Bot(), сохраняем созданный объект в переменную и через нее мы можем управлять ботом
dp = Dispatcher(storage=MemoryStorage())    # Через диспетчер мы создаем функции, которыми обладает бот, и управляем 


async def main():   # main -- это общепринятое название главной функции программы
    init_db()
    dp.include_router(router)   # Подключаем наш роутер к диспетчеру
    await dp.start_polling(bot)     # отправляет запросы на тг-сервер, также это команда для запуска бота

# Polling -- способ получения обновлений от тг, при котором бот регулярно запрашивает новые события


if __name__ == '__main__':      # это защита от случайного запуска и бот запускается лишь в папке main
    logging.basicConfig(level=logging.INFO)     # у логирования есть уровни ( INFO, DEBUG, WARNING, ERROR, CRITICAL )
    asyncio.run(main())     # Запускает асинхронную функцию main()
    
