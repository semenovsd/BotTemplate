from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class CallCacheTime(BaseMiddleware):
    """Добавляет кэш тайм при ответе на инлайн кнопки."""

    def __init__(self):
        super().__init__()

    async def on_post_process_callback_query(self, call: types.CallbackQuery, *arg, **kwargs):
        await call.answer(cache_time=5)
