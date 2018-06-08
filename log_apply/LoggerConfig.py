import logging
from log_mongodb_handler import MongoHandler

# filter log level
class LevelFilter(logging.Filter):
    def __init__(self, low: int, high: int):
        """ logger level 0 - 50 """
        self._low = low
        self._high = high
        logging.Filter.__init__(self)

    def filter(self, record):
        if self._low <= record.levelno <= self._high:
            return True
        return False


dictConfig = {
    'version': 1,
    "disable_existing_loggers": False,  # 是否禁用现有的记录器
    "loggers": {
        # "dbLog": {
        #     "handlers": ["mongoH"],
        #     "level": "DEBUG"
        # },
        "infoLog": {
            "handlers": ["infoH", "errorH"],
            "level": "DEBUG",
            "propagate": True  # 是否传递给父记录器
        },
        "debugLog": {
            "handlers": ["consoleH", "infoH"],
            "level": "DEBUG",
            "propagate": True
        }
    },
    "handlers": {
        "errorH": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "error.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 10,
            "encoding": "utf8",
            "filters": ["errorFilter", ]
        },
        "infoH": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "info.log",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 10,
            "encoding": "utf8",
            "filters": ["infoFilter", ]
        },
        "consoleH": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["debugFilter", ]  # DEBUG=True时生效
        },
        # "mongoH": {
        #     "class": "log_mongodb_handler.MongoHandler",
        #     "host": "localhost",
        #     "port": 27017,
        #     "database_name": "cms",
        #     "collection": "logs",
        #     "level": "DEBUG",
        # }
    },
    # 过滤器
    "filters": {
        "debugFilter": {
            '()': LevelFilter,
            "low": 0,
            "high": 10
        },
        "infoFilter": {
            "()": LevelFilter,
            "low": 10,
            "high": 30
        },
        "errorFilter": {
            "()": LevelFilter,
            "low": 30,
            "high": 50
        }
    },
    "formatters": {
        "standard": {"format": '[%(asctime)s][%(thread)d-%(levelname)s][%(funcName)s(%(lineno)d)]:%(message)s'},
        "short": {"format": '%(levelname)s %(message)s'}
    }
}