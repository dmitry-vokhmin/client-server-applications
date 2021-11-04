"""
Задание №1
Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV. Для этого:

a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений
извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список для хранения
данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить
в файл main_data (также для каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

c. Проверить работу программы через вызов функции write_to_csv().
"""
from pathlib import Path
import re
import csv


def str_strip(reg_result):
    return [item.strip() for item in reg_result]


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for num in range(1, 4):
        with open(Path(__file__).parent.joinpath(f'for_homework_lesson2/info_{num}.txt')) as file:
            open_file = file.read()
            os_prod_list.extend(str_strip(re.findall("(?<=Изготовитель ОС:).+(?=\\n)", open_file)))
            os_name_list.extend(str_strip(re.findall("(?<=Название ОС:).+(?=\\n)", open_file)))
            os_code_list.extend(str_strip(re.findall("(?<=Код продукта:).+(?=\\n)", open_file)))
            os_type_list.extend(str_strip(re.findall("(?<=Тип системы:).+(?=\\n)", open_file)))
    main_data.extend(zip(os_prod_list, os_name_list, os_code_list, os_type_list))
    return main_data


def write_to_csv():
    main_data = get_data()
    with open('new_data.csv', 'w', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for row in main_data:
            csv_writer.writerow(row)


write_to_csv()
