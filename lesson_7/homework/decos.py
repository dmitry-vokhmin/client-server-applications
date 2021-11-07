import traceback
import datetime
import sys
import logging
from lesson_6.practice.logs import config_client_log, config_server_log


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Функция: {func.__name__} с аргументами {args}, {kwargs},'
                     f'Вызвана из функции {traceback.format_stack()[0].split()[-1]} в {datetime.datetime.now()}')
        return res
    return wrapper
