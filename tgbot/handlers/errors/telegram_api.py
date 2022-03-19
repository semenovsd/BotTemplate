from aiogram.utils import exceptions
from loguru import logger

from tgbot.loader import dp
from tgbot.utils import send_messages
from tgbot.config import TG_ADMINS_ID


@dp.errors_handler(exception=exceptions.TelegramAPIError)
async def telegram_exceptions_handler(update, exception):

    if isinstance(exception, exceptions.CantDemoteChatCreator):
        exception_message = "Can't demote chat creator"
    elif isinstance(exception, exceptions.MessageNotModified):
        exception_message = 'Message is not modified'
    elif isinstance(exception, exceptions.MessageCantBeDeleted):
        exception_message = 'Message cant be deleted'
    elif isinstance(exception, exceptions.MessageToDeleteNotFound):
        exception_message = 'Message to delete not found'
    elif isinstance(exception, exceptions.MessageTextIsEmpty):
        exception_message = 'MessageTextIsEmpty'
    elif isinstance(exception, exceptions.Unauthorized):
        exception_message = f'Unauthorized: {exception}'
    elif isinstance(exception, exceptions.InvalidQueryID):
        exception_message = f'InvalidQueryID: {exception} \nUpdate: {update}'
    elif isinstance(exception, exceptions.TelegramAPIError):
        exception_message = f'TelegramAPIError: {exception} \nUpdate: {update}'
    elif isinstance(exception, exceptions.RetryAfter):
        exception_message = f'RetryAfter: {exception} \nUpdate: {update}'
    elif isinstance(exception, exceptions.CantParseEntities):
        exception_message = f'CantParseEntities: {exception} \nUpdate: {update}'
    else:
        exception_message = f'Update: {update} \n{exception}'
    logger.exception(f'\n\n WARNING TG Exception: {exception} \nUpdate: {update}\n\n')
    await send_messages(TG_ADMINS_ID[0], exception_message)
    return True
