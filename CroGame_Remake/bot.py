from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import logging

logging.basicConfig(level=logging.INFO)
from config import BOT_TOKEN
from db import connect, create_tables
from services.game_manager import game_manager
from keyboards.inline import game_keyboard
from utils.user import user_link

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


def is_group(message: Message):
    return message.chat.type in ["group", "supergroup"]


# 🎮 СТАРТ ИГРЫ
@dp.message(Command("game"))
async def cmd_game(message: Message):
    if not is_group(message):
        return await message.answer("В КроКодила можно поиграть только в группе!")

    game = game_manager.start_game(message.chat.id, message.from_user.id)

    if not game:
        return await message.answer(
            "❌Текущий раунд ещё не закончился!\nПодождите 5 минут."
        )

    user = user_link(message.from_user)

    await message.answer(
        f"🤔<b>{user} объясняет слово!</b>",
        reply_markup=game_keyboard(),
        disable_web_page_preview=True
    )


# 🔎 ПОКАЗАТЬ СЛОВО
@dp.callback_query(lambda c: c.data == "show_word")
async def show_word(callback: CallbackQuery):
    game = game_manager.get_game(callback.message.chat.id)

    if not game:
        return await callback.answer("Нет активной игры", show_alert=True)

    if callback.from_user.id != game.leader_id:
        return await callback.answer("Это слово предназначено не для тебя!", show_alert=True)

    word = game_manager.get_word(callback.message.chat.id)

    await callback.answer(
        f"📝Загаданное слово:\n<b>{word}</b>",
        show_alert=True
    )


# 🗂 НОВОЕ СЛОВО
@dp.callback_query(lambda c: c.data == "new_word")
async def new_word(callback: CallbackQuery):
    game = game_manager.get_game(callback.message.chat.id)

    if not game:
        return await callback.answer("Нет активной игры", show_alert=True)

    if callback.from_user.id != game.leader_id:
        return await callback.answer("Это слово предназначено не для тебя!", show_alert=True)

    word = game_manager.get_word(callback.message.chat.id)

    await callback.answer(
        f"🗞Обновленное слово:\n<b>{word}</b>",
        show_alert=True
    )