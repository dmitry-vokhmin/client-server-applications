"""Модуль json_write"""

import json

DICT_TO_JSON = {
    "action": "msg",
    "to": "account_name",
    "from": "account_name",
    "encoding": "ascii",
    "message": "message"
    }

print('----- преобразование python-объекта (словаря) в строку в формате json -----')
with open('mes_example_write_1.json', 'w', encoding='utf-8') as f_n:
    f_n.write(json.dumps(DICT_TO_JSON))

with open('mes_example_write_1.json') as f_n:
    print(f_n.read())

print()
print('----- запись python-объекта в файл в формате json -----')
with open('mes_example_write_2.json', 'w', encoding='utf-8') as f_n:
    json.dump(DICT_TO_JSON, f_n)

with open('mes_example_write_2.json') as f_n:
    print(f_n.read())

print()
print('----- использование дополнительных параметров записи -----')
with open('mes_example_write_3.json', 'w', encoding='utf-8') as f_n:
    json.dump(DICT_TO_JSON, f_n, sort_keys=True, indent=4)

with open('mes_example_write_3.json') as f_n:
    print(f_n.read())

print()
print('----- запись символов вместо записи кодовых точек -----')

DICT_TO_JSON_2 = {
    "action": "msg",
    "to": "Иванову И.И.",
    "from": "Петрова П.П.",
    "encoding": "ascii",
    "message": "Привет!"
    }

with open('mes_example_write_3.json', 'w', encoding='utf-8') as f_n:
    # json.dump(DICT_TO_JSON_2, f_n, sort_keys=True, indent=4)
    json.dump(DICT_TO_JSON_2, f_n, sort_keys=True, indent=4, ensure_ascii=False)

with open('mes_example_write_3.json') as f_n:
    print(f_n.read())
