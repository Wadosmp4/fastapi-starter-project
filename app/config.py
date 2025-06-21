from typing import Any

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_PORT: int = 5432
    POSTGRES_PASSWORD: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_DB: str = ''
    POSTGRES_HOST: str = 'localhost'


class RedisSettings(BaseSettings):
    REDIS_PASSWORD: str = ''
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379


class AppSettings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()

    class Config:
        env_file = './.env'
        extra = 'allow'


class LogConfig(BaseSettings):
    LOGGER_NAME: str = 'app'
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'DEBUG'

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict[str, Any] = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers: dict[str, Any] = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers: dict[str, Any] = {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }


config = AppSettings()
