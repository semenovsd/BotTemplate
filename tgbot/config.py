import os
from pathlib import Path

from decouple import config, Csv

@dataclass
class Telegram:
    # Telegram settings
    TGBOT_TOKEN: str = config('TGBOT_TOKEN', cast=str)
    TG_ADMINS_ID: list = config('TG_ADMINS_ID', cast=Csv(delimiter=':'), default='395415524')
    # Telegram webhook
    DOMAIN_NAME_OR_IP: str = config('DOMAIN_NAME_OR_IP', cast=str, default='127.0.0.1')
    WEBHOOK_PORT: str = config('WEBHOOK_PORT', cast=str, default='8443')
    WEBHOOK_PATH: str = config('WEBHOOK_PATH', cast=str, default='/bottemplate')
    WEBHOOK_URL: str = f'{DOMAIN_NAME_OR_IP}:{WEBHOOK_PORT}{WEBHOOK_PATH}'
    # Webhost
    TGBOT_HOST: str = config('TGBOT_HOST', cast=str, default='0.0.0.0')
    TGBOT_PORT: str = config('TGBOT_PORT', cast=str, default='8443')


@dataclass
class PostgresConfig:
    POSTGRES_HOST = config('POSTGRES_HOST', cast=str, default='127.0.0.1')
    POSTGRES_PORT = config('POSTGRES_PORT', cast=str, default='5432')
    POSTGRES_USER = config('POSTGRES_USER', cast=str, default='postgres')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=str, default='postgres')
    POSTGRES_DB = config('POSTGRES_DB', cast=str, default='tgbot_db')
    POSTGRES_URI = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


@dataclass
class Misc:
    # Environment
    ENV_STAGE = config('ENV_STAGE', cast=str, default='local')
    BASE_DIR: os.path = Path(__file__).resolve().parent
    # SSL
    SSL_DIR: str = config('SSL_DIR', cast=str, default='./.ssl')
    SSL_CERT: str = config('SSL_CERT', cast=str, default='url_cert.pem')
    SSL_PRIV: str = config('SSL_PRIV', cast=str, default='url_private.key')
    SSL_CERT_PATH: str = os.path.join(BASE_DIR, f'tgbot/{SSL_DIR}{SSL_CERT}')
    SSL_PRIV_PATH: str = os.path.join(BASE_DIR, f'tgbot/{SSL_DIR}{SSL_PRIV}')


@dataclass
class Config:
    DB: PostgresConfig = PostgresConfig()
    MISC: Misc = Misc()
    TELEGRAM: Telegram = Telegram()


def load_config() -> Config:
    conf = Config()
    # Clean env vars
    os.environ.clear()
    return conf

config = load_config()
