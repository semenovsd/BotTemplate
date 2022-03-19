from aiogram import Dispatcher
from aiogram.dispatcher.filters import IsReplyFilter

from .is_auth_code import IsAuthCode


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsReplyFilter, event_handlers=dp.message_handlers)
    dp.filters_factory.bind(IsAuthCode)
