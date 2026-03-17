from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def game_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔎Посмотреть слово", callback_data="show_word"),
            InlineKeyboardButton(text="🗂Новое слово", callback_data="new_word")
        ]
    ])