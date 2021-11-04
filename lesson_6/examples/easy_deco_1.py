"""Простейший декоратор-функция"""

import time
from functools import wraps


def decorator(func):
    """Сам декоратор"""
    @wraps(func)
    def wrapper():
        """Обертка"""
        print('Сейчас выполняется функция-обёртка')
        time.sleep(2)
        print(f'Это просто ссылка на экземпляр оборачиваемой функции: {func.__name__}')
        time.sleep(2)
        print('Выполняем оборачиваемую (исходную) функцию...')
        time.sleep(2)
        f = func()
        time.sleep(2)
        print('Выходим из обёртки')
        return f

    return wrapper


# @decorator
def some_text():
    """Какая-то логика"""
    print('вычисления')


# some_text()

# some_text = decorator(some_text)
# some_text()

# ==========================================
# how to get the function name?
# print(type(some_text), some_text.__name__)
# print(type(some_text), some_text.__doc__)

# ==========================================
# how to get the function result?
print(some_text())

