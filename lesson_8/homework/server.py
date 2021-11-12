"""Программа-сервер"""

import socket
import sys
import argparse
import logging
import select
import logs.config_server_log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, MAX_CONNECTIONS, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION
from common.utils import get_message, send_message
from lesson_6.practice.decos import log

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages, client, clients, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, возвращает словарь-ответ для клиента
    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message:
        if message[USER][ACCOUNT_NAME] not in names:
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, {RESPONSE: 200})
        else:
            send_message(client, {RESPONSE: 400, ERROR: 'Имя занято'})
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages.append(message)
        return
    return send_message(client, {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    })


@log
def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')
    return listen_address, listen_port


@log
def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию
    :return:
    """
    listen_address, listen_port = create_arg_parser()
    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)
    transport.listen(MAX_CONNECTIONS)

    clients = set()
    messages = []
    names = {}

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.add(client)

        receive_data_lst = []
        send_data_lst = []

        try:
            if clients:
                receive_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if receive_data_lst:
            for client_with_message in receive_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message, clients, names)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message} отключился от сервера')
                    clients.remove(client_with_message)
        for message in messages:
            try:
                process_message(message, names, send_data_lst)
            except:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {message[DESTINATION]} была потеряна')
                clients.remove(names[message[DESTINATION]])
                del names[message[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
