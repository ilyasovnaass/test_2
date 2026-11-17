from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)

inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="✅ Выполнить задачу",
            callback_data="done"
        )
    ]
])