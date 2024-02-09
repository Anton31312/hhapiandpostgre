from src.hhru_api import HeadHunterAPI
from db.db_manager import DBManager


def load_data(selected_employers, db_name):
    """
    Функция для загрузки данных полученных из API в db созданную на Postgre
    """

    hh = HeadHunterAPI()
    db_manager = DBManager(db_name)

    for employer_name in selected_employers:
        vacancies_json = hh.get_vacancies_by_employer_name(employer_name)

        employers = hh.created_employer(vacancies_json)
        vacancies = hh.created_vacancy(vacancies_json)

        db_manager.insert_employers(employers)
        db_manager.insert_vacancies(vacancies)

    db_manager.close_connection()