from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import MessageError


class AutoRemoveMiddleware(BaseMiddleware):
    """One screen menu - удаляем предыдущие сообщения"""

    def __init__(self):
        super().__init__()

    async def on_post_process_callback_query(self, call: types.CallbackQuery, *arg, **kwargs):
        try:
            await call.message.delete()
        except MessageError:
            pass

    # async def on_post_process_message(self, message: types.Message, *arg, **kwargs):
    #     try:
    #         await message.delete()
    #     except MessageError:
    #         pass
