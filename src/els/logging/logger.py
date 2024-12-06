"""
logging.py -- Logging setup for els

This module contains the setup_logging function, which is used to set up the logging configuration for els.

Example usage
-------------
>>> from els.utils.misc.logging import setup_logging
>>> setup_logging(debug=True)
"""
import logging
import logging.config
from functools import wraps
import os

# Define a log level for evolutionary steps
MILVUS_LEVEL = 43
logging.addLevelName(MILVUS_LEVEL, "MILVUS")

def MILVUS_log(self, message, *args, **kwargs):
    if self.isEnabledFor(MILVUS_LEVEL):
        self._log(MILVUS_LEVEL, message, args, **kwargs)

def add_logger_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        functionName = f"<func {__name__}.{func.__name__}>"

        logger = logging.getLogger(functionName)
        func_globals = func.__globals__
        func_globals['logger'] = logger

        return func(*args, **kwargs)
    return wrapper

logging.Logger.MILVUS = MILVUS_log

# Custom filter to include only logs with level 43
class CustomFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == MILVUS_LEVEL

# Custom filter to exclude logs with level 43
class ExcludeCustomFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != MILVUS_LEVEL

def setup_logging(
        debug: bool = False,
        logName : str = "els.log",
        evolName: str = "els.MILVUS",
        clearFiles : bool = True):
    """
    This function is used to set up the logging configuration for els.

    Parameters
    ----------
    debug : bool, default=False
        If True, sets the logging level to DEBUG. Otherwise, sets the logging level to INFO.
    logName : str, default="els.log"
        The name of the log file.
    evolName : str, default="els.MILVUS"
        The name of the MILVUS log file.
    clearFiles : bool, default=True
        If True, clears the log files before writing to them. Otherwise, appends to the log files.
    """
    if debug:
        ll = "DEBUG"
    else:
        ll = "INFO"

    if clearFiles:
        if os.path.exists(logName):
            os.remove(logName)
        if os.path.exists(evolName):
            os.remove(evolName)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'term': {
                'format': '%(levelname)s: %(message)s',
                }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 30,
                'formatter': 'term',
                'stream': 'ext://sys.stdout',
            },
            'file_all_except_custom': {
                'class': 'logging.FileHandler',
                'level': f'{ll}',
                'formatter': 'standard',
                'filename': f'{logName}',
                'filters': ['exclude_custom'],
            },
            'file_custom': {
                'class': 'logging.FileHandler',
                'level': 'MILVUS',
                'formatter': 'standard',
                'filename': f'{evolName}',
                'filters': ['custom_only'],
            },
        },
        'filters': {
            'custom_only': {
                '()': CustomFilter,
            },
            'exclude_custom': {
                '()': ExcludeCustomFilter,
            },
        },
        'loggers': {
            'my_module': {
                'level': 'DEBUG',
                'handlers': ['console', 'file_all_except_custom', 'file_custom'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file_all_except_custom', 'file_custom'],
        },
    }

    logging.config.dictConfig(logging_config)
    
