"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:

a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
from pathlib import Path
import datetime
import json


def write_order_to_json(item, quantity, price, buyer, date):
    file_path = Path(__file__).parent.joinpath(f'for_homework_lesson2/orders.json')
    with open(file_path, encoding='utf-8') as file:
        data = json.load(file)
        data['orders'].append({
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date.isoformat(),
        })
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, indent=4))


now_date = datetime.datetime.now().date()
write_order_to_json('test', 2, 100, 'me', now_date)
