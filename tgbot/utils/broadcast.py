import asyncio
import datetime
import logging
from typing import Union

from aiogram.utils import exceptions

from tgbot.loader import dp


async def send_messages(users_id: Union[list, str], message: str, keyboard=None, disable_web_page_preview=False,
                        retry=False):
    log = logging.getLogger('broadcast')
    count = 0
    start_time = datetime.datetime.now()
    users_id = users_id if isinstance(users_id, list) else [users_id]
    for user_id in users_id:
        try:
            await dp.bot.send_message(user_id, message,
                                      disable_web_page_preview=disable_web_page_preview,
                                      reply_markup=keyboard)
            await asyncio.sleep(0.05)  # Telegram limit 30 message per second, here set 20 msg per second
        except exceptions.BotBlocked:
            log.info(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.info(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.info(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            if not retry:
                await send_messages(user_id, message, keyboard, disable_web_page_preview, retry=True)
        except exceptions.UserDeactivated:
            log.info(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.error(f"Target [ID:{user_id}]: failed")
        else:
            count += 1
            log.info(f"Target [ID:{user_id}]: success")
    # if not retry:
    #     finish_time = datetime.datetime.now()
    #     total_time = (finish_time - start_time).total_seconds()
    #     msg = f'Время начала рассылки - {start_time.time()}\n' \
    #           f'Всего пользователей - {len(users_id)}\n' \
    #           f'Отправлено сообщений - {count}\n' \
    #           f'Время окончания рассылки - {finish_time}' \
    #           f'Итоговое время рассылки, в сек. - {total_time}'
    #     return await send_messages(msg, TG_ADMINS_ID[0])


async def send_photo(users_id: Union[list, str], message: str, photo, keyboard=None, retry=False):
    log = logging.getLogger('broadcast')
    count = 0
    start_time = datetime.datetime.now()
    users_id = users_id if isinstance(users_id, list) else [users_id]
    for user_id in users_id:
        try:
            await dp.bot.send_photo(chat_id=user_id, photo=photo, caption=message, reply_markup=keyboard)
            await asyncio.sleep(0.05)  # Telegram limit 30 message per second, here set 20 msg per second
        except exceptions.BotBlocked:
            log.info(f"Target [ID:{user_id}]: blocked by user")
        except exceptions.ChatNotFound:
            log.info(f"Target [ID:{user_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            log.info(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
            await asyncio.sleep(e.timeout)
            if not retry:
                await send_photo(user_id, message, photo, keyboard=keyboard, retry=True)
        except exceptions.UserDeactivated:
            log.info(f"Target [ID:{user_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            log.error(f"Target [ID:{user_id}]: failed")
        else:
            count += 1
            log.info(f"Target [ID:{user_id}]: success")
    # if not retry:
    #     finish_time = datetime.datetime.now()
    #     total_time = (finish_time - start_time).total_seconds()
    #     msg = f'Время начала рассылки - {start_time.time()}\n' \
    #           f'Всего пользователей - {len(users_id)}\n' \
    #           f'Отправлено сообщений - {count}\n' \
    #           f'Время окончания рассылки - {finish_time}' \
    #           f'Итоговое время рассылки, в сек. - {total_time}'
    #     return await send_messages(msg, TG_ADMINS_ID[0])
