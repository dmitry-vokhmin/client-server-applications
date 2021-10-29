"""Программа-клиент"""

import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, USER_ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT
from common.utils import get_message, send_message


def create_presence(server_port, account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: server_port,
        USER: {
            USER_ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    '''Загружаем параметы коммандной строки'''
    try:
        server_address = sys.argv[2]
        server_port = int(sys.argv[1])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence(server_port)
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
