from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.alchemy import Session
from tgbot.db.models import User


class AccessDenied:
    def __init__(self):
        raise CancelHandler()


class AccessMiddleware(BaseMiddleware):
    """
    Аутентификация пользователей — получаем или создаём пользователя по телеграмм ID в бд или отказываем в доступе.
    """

    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict, *arg, **kwargs):
        async with Session.begin() as session:
            user = await User.get_or_create(session, types.User.get_current())
        data['user'] = user or AccessDenied()

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict, *arg, **kwargs):
        async with Session.begin() as session:
            user = await User.get_or_create(session, types.User.get_current())
        data['user'] = user or AccessDenied()
