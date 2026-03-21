import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from services.game_manager import game_manager
from keyboards.inline import game_keyboard
from utils.user import user_link

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()


# ✅ Проверка на группу
def is_group(message: Message):
    return message.chat.type in ["group", "supergroup"]


# ⏱ формат времени
def format_time(seconds: int):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes}:{sec:02d}"


# 🎮 СТАРТ ИГРЫ
@dp.message(Command("game"))
async def cmd_game(message: Message):
    if not is_group(message):
        return await message.answer("В КроКодила можно поиграть только в группе!")

    game = game_manager.start_game(message.chat.id, message.from_user.id)

    if not game:
        time_left = game_manager.time_left(message.chat.id)

        return await message.answer(
            f"❌Текущий раунд ещё не закончился!\n"
            f"Подождите {format_time(time_left)}.",
            disable_web_page_preview=True
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


# 🧪 ТЕСТ (ВСЕГДА ВНИЗУ!)
@dp.message()
async def test(message: Message):
    await message.answer("Я жив!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
