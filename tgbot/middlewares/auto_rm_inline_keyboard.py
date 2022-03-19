from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import MessageError, MessageCantBeDeleted, InlineKeyboardExpected, BadRequest
from loguru import logger


class AutoRemoveInlineKeyboardMiddleware(BaseMiddleware):
    """One screen menu - удаляем нажатые кнопки"""

    def __init__(self):
        super().__init__()

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, *arg, **kwargs):
        with suppress(MessageError, BadRequest):
            await call.message.edit_reply_markup()
