from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import AUTH_PHONE_HOLDER_TG_ID


class IsAuthCode(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == AUTH_PHONE_HOLDER_TG_ID and message.text.isdigit()
