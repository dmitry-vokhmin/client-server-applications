"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse
import logging
import threading
import logs.config_client_log
from errors import ReqFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, ERROR, DEFAULT_IP_ADDRESS, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION
from common.utils import get_message, send_message
from lesson_6.practice.decos import log

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


@log
def message_from_server(sock, username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and MESSAGE_TEXT in message\
                    and message[DESTINATION] == username:
                print(f'Получено сообщение от пользователя '
                      f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                                   f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except Exception:
            break


@log
def message_for_user(sock, client_name):
    print_help_messages()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, client_name)
        elif command == 'help':
            print_help_messages()
        elif command == 'exit':
            print('Отключение')
            break
        else:
            print('Повторите ввод команды')


def print_help_messages():
    print('message - отправить сообщение.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def create_message(sock, account_name='Guest'):
    user = input('Введите получателя: ')
    message = input('Введите сообщение: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    try:
        send_message(sock, message_dict)
    except:
        sys.exit(1)
    return message_dict


@log
def create_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def create_arg_parser():
    """
    Создаём парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.n

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    return server_address, server_port, client_name


@log
def main():
    """
    Загружаем параметы коммандной строки
    :return:
    """
    server_address, server_port, client_name = create_arg_parser()

    print(f'Имя пользователя: {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence(client_name)
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        mess_receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        mess_receiver.daemon = True
        mess_receiver.start()

        user_interface = threading.Thread(target=message_for_user, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()

        while True:
            time.sleep(1)
            if mess_receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
