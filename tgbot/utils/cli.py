import ssl

from aiogram import Dispatcher
from aiogram.utils import executor
from loguru import logger

from tgbot import config
from tgbot.db.alchemy import setup_db
from tgbot.loader import scheduler
from tgbot.utils import send_messages, setup_default_commands, scheduler_jobs


async def on_startup_webhook(dp: Dispatcher):
    logger.debug('Start on webhook mode')

    # Check webhook
    webhook_info = await dp.bot.get_webhook_info()
    # If URL is bad
    if webhook_info.url != config.WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        await dp.bot.delete_webhook()
    # Set new URL for webhook
    await dp.bot.set_webhook(config.WEBHOOK_URL, certificate=open(config.SSL_CERT_PATH, 'rb').read())

    await on_startup(dp)


async def on_startup_polling(dp: Dispatcher):
    logger.debug('Start on polling mode')
    # Delete webhook
    await dp.bot.delete_webhook()
    await on_startup(dp)


async def on_startup(dp: Dispatcher):
    # Send message to admin
    await send_messages(config.TG_ADMINS_ID[0], f'Bot startup in {config.ENV_STAGE} environment!')
    # Setup bot commands
    await setup_default_commands(dp)
    # Create connection to db
    await setup_db()
    scheduler_jobs()


async def on_shutdown(dp: Dispatcher):
    # Send message to admin
    await send_messages(config.TG_ADMINS_ID[0], f'Bot shutdown in {config.ENV_STAGE} environment!')
    # Shutdown Scheduler
    scheduler.shutdown()
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
    context.load_cert_chain(config.SSL_CERT_PATH, config.SSL_PRIV_PATH)

    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup_webhook,
        on_shutdown=on_shutdown,
        skip_updates=skip_updates,
        host=config.TGBOT_HOST,
        port=config.TGBOT_PORT,
        ssl_context=context
    )


def cli(argv):
    # Import dp from all handlers
    from tgbot.handlers import dp

    if argv.mode == 'webhook':
        webhook(dp)
    elif argv.mode == 'polling':
        polling(dp)
    else:
        raise AttributeError('Please set correct start mode - webhook or polling')
