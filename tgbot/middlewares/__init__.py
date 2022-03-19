from loguru import logger
from tgbot.loader import dp

from .authentification import AccessMiddleware
from .call_answer import CallCacheTime
from .autoremove import AutoRemoveMiddleware

if __name__ == "tgbot.middlewares":
    dp.middleware.setup(AccessMiddleware())
    dp.middleware.setup(CallCacheTime())
    dp.middleware.setup(AutoRemoveMiddleware())
    logger.info('Middlewares are successfully configured')
