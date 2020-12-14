# -*- coding: utf-8 -*-
# Python 3.8.6


from threading import Thread
from sqlalchemy import create_engine
import logging
import logging.config


TOKEN = '1431183102:AAF95F0wUZovGBGsgg4tePQzbw69Fef0d6o'
# engine = create_engine('postgres://mwlcvjxc:Ir0o3E7CvAKaLbckEjyH8J6YdKo48c1I@dumbo.db.elephantsql.com:5432/mwlcvjxc')
engine = create_engine('postgres://apaqfcniqplrtl:772da4c736d7b3ff509f0b3c3e108988ca5d90ed7d60cecfeca6207a431ec24b'
                       '@ec2-54-76-215-139.eu-west-1.compute.amazonaws.com:5432/ddog5vctn9v5p6')

log_config = {
    'version': 1,
    'formatters': {
        'main_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'debug_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'main_formatter',
            'filename': 'bot_debug.log',
            'encoding': 'UTF-8',
        },
        'error_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'main_formatter',
            'filename': 'bot_error.log',
            'encoding': 'UTF-8',
        },
    },
    'loggers': {
        'debug_logger': {
            'handlers': ['debug_handler'],
            'level': 'DEBUG',
        },
        'error_logger': {
            'handlers': ['error_handler'],
            'level': 'ERROR',
        },
    },
}


logging.config.dictConfig(log_config)
debug_logger = logging.getLogger('debug_logger')
error_logger = logging.getLogger('debug_logger')


def debug_with_thread(message):
    thread = Thread(target=debug_logger.debug, args=(message, ))
    thread.start()


def error_with_thread(message):
    thread = Thread(target=error_logger.exception, args=(message, ))
    thread.start()

