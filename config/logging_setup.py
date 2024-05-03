import os
from datetime import datetime
from jdatetime import datetime as JDateTime
from pathlib import Path
import queue
import logging
import logging.handlers
import logging.config
from concurrent_log_handler import ConcurrentRotatingFileHandler
from logging.handlers import RotatingFileHandler
import atexit
from persiantools.jdatetime import JalaliDateTime


BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
XML_LOG_DIR = os.path.join(LOGGING_DIR, 'xml')
DEBUG_LOG_DIR = os.path.join(LOGGING_DIR, 'debug')
ERROR_LOG_DIR = os.path.join(LOGGING_DIR, 'error')
WARNING_LOG_DIR = os.path.join(LOGGING_DIR, 'warning')
DB_LOG_DIR = os.path.join(LOGGING_DIR, 'db_log')

log_directories = [
    LOGGING_DIR,
    XML_LOG_DIR,
    DEBUG_LOG_DIR,
    ERROR_LOG_DIR,
    WARNING_LOG_DIR,
    DB_LOG_DIR
]

MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB

for directory in log_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)


q = queue.Queue()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error/error.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'warning/warning.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug/debug.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        #     'sql_file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(LOGGING_DIR, 'db_log/db_sql.log'),
        #     'formatter': 'verbose',
        #     'maxBytes': 10485760,  # 10MB
        #     'backupCount': 5,
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'error_file', 'warning_file', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'handlers': ['sql_file'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
}

logging.config.dictConfig(LOGGING)

error_listener = logging.handlers.QueueListener(
    q, logging.FileHandler('error.log')
)
warning_listener = logging.handlers.QueueListener(
    q, logging.FileHandler('warning.log')
)
debug_listener = logging.handlers.QueueListener(
    q, logging.FileHandler('debug.log')
)

error_listener.start()
warning_listener.start()
debug_listener.start()

def stop_listeners():
    error_listener.stop()
    warning_listener.stop()
    debug_listener.stop()

atexit.register(stop_listeners)

logger = logging.getLogger('xml_file_validation')

if not logger.hasHandlers():
    file_handler = RotatingFileHandler(os.path.join(LOGGING_DIR, 'xml/xml_file_validation.log'), maxBytes=MAX_LOG_SIZE, backupCount=100)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.ERROR)

def log_error(error_message):
    try:
        current_time = JDateTime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = error_message.split('-')[-1].strip()
        logger.error(f"{current_time} - {error_message}")
    except Exception as e:
        print(f"Error logging the message: {e}")