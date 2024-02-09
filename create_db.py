import time

from db.db_query import create_tables
from loader.data_load import load_data
from src.config import config


def created_db_insert_tables():
    params = config(filename='src/database.ini')
    db_hh = 'vacancies_hh'

    # Выбор конкретных 10 компаний
    selected_employers = [
        'Ростех',
        'Яндекс',
        'ООО ИНИТИ',
        'Домклик',
        'VK',
        'Циан',
        'Тинькофф',
        'Литрес',
        'Ostrovok.ru',
        'ООО Скайлайн',
        'ООО ИНТЕХ'
    ]

    # Создание таблиц в БД
    create_tables(db_hh, params)

    time.sleep(2)  # Задержка в 2 секунды

    # Заполнение таблиц данными о выбранных компаниях и их вакансиях
    load_data(selected_employers, db_hh)


if __name__ == '__main__':
    created_db_insert_tables()