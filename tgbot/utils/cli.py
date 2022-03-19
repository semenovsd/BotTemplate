import ssl
import time

from aiogram import Dispatcher
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from tgbot.config import config
from tgbot.db.database import create_db
from tgbot.utils import send_messages, setup_default_commands, scheduler_jobs


async def on_startup_webhook(dp: Dispatcher):
    logger.debug('Start on webhook mode')
    # Check webhook
    webhook_info = await dp.bot.get_webhook_info()

    # If URL is bad
    if webhook_info.url != config.TELEGRAM.WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        await dp.bot.delete_webhook()
    logger.debug(f'SET WEBHOOK_URL: {config.TELEGRAM.WEBHOOK_URL}')
    # Set new URL for webhook
    # if cert_type == 'verified':
    #     # For verified cert
    await dp.bot.set_webhook(config.TELEGRAM.WEBHOOK_URL)
    # else:
    #     # For self-singer cert
    # await dp.bot.set_webhook(config.WEBHOOK_URL, certificate=open(config.SSL_CERT_PATH, 'rb').read())

    await on_startup(dp)


async def on_startup_polling(dp: Dispatcher):
    logger.debug('Start on polling mode')
    # Delete webhook
    await dp.bot.delete_webhook()
    await on_startup(dp)


async def on_startup(dp: Dispatcher):
    # Send message to admin
    await send_messages(f'Bot startup in {config.MISC.ENV_STAGE} environment!', config.TELEGRAM.TG_ADMINS_ID[0])
    # Setup bot commands
    await setup_default_commands(dp)
    # Create connection to db
    await create_db()
    # Setup scheduler
    scheduler = AsyncIOScheduler()
    scheduler_jobs(scheduler)
    scheduler.start()


async def on_shutdown(dp: Dispatcher):
    # Send message to admin
    await send_messages(f'Bot shutdown in {config.MISC.ENV_STAGE} environment!', config.TELEGRAM.TG_ADMINS_ID[0])
    # Shutdown Scheduler
    # scheduler.shutdown()
    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


def polling(dp: Dispatcher, skip_updates: bool = True):
    """
    Start application in polling mode
    """
    executor.start_polling(dp, skip_updates=skip_updates, on_startup=on_startup_polling, on_shutdown=on_shutdown)


def webhook(dp: Dispatcher, skip_updates: bool = True):
    """
    Run application in webhook mode
    """
    # Generate SSL context.
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    logger.debug(f'LOAD SSL CONTEXT: {config.MISC.SSL_CERT_PATH} and {config.MISC.SSL_PRIV_PATH}')
    context.load_cert_chain(config.MISC.SSL_CERT_PATH, config.MISC.SSL_PRIV_PATH)
    logger.debug(f'WEBHOOK_PATH: {config.TELEGRAM.WEBHOOK_PATH}')

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.TELEGRAM.WEBHOOK_PATH,
        on_startup=on_startup_webhook,
        on_shutdown=on_shutdown,
        skip_updates=skip_updates,
        host=config.TELEGRAM.TGBOT_HOST,
        port=config.TELEGRAM.TGBOT_PORT,
        ssl_context=context
    )


def cli(argv):
    # Import dp from all handlers
    from tgbot.handlers import dp
    logger.debug(f'########### ARGS: {argv}')
    if argv.mode == 'webhook':
        webhook(dp)
    elif argv.mode == 'polling':
        polling(dp)
    elif argv.mode == 'fake_start':
        while True:
            try:
                logger.debug(f'\n\n ### SERVICE START IN FAKE MODE ###\n\n')
                time.sleep(60)
            except KeyboardInterrupt:
                break
    else:
        raise AttributeError('Please set correct start mode - webhook or polling')
