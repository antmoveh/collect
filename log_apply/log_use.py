import logging
import logging.config
from log_apply import LoggerConfig


logging.config.dictConfig(LoggerConfig.dictConfig)


