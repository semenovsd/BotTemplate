from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from tgbot.db.alchemy import Session
from tgbot.db.models import User
from tgbot.loader import dp


@dp.message_handler(CommandStart(), state='*')
async def start_menu_handler(message: types.Message, user: User):
    async with Session.begin() as session:
        count = await user.count(session)
    reply = f'Привет! Кол-во пользователей {count}'
    await message.answer(reply)
