from logging.config import dictConfig
import os

from dotenv import load_dotenv

from apps.api.domain.exceptions import ConfigurationError

load_dotenv()


def get_database_uri():
    database_uri = os.getenv("DATABASE_URI")
    if not database_uri:
        raise ConfigurationError("DATABASE_URI not configured!")
    return database_uri


def configure_logging(log_level: str = "INFO"):
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "app-logger": {"handlers": ["default"], "level": log_level},
        },
    }
    dictConfig(log_config)