import requests
from typing import Any, List, Dict

from db.employer import Employer
from db.vacancy import Vacancy

class HeadHunterAPI:
    """
    Класс для реализации подключения по API к сайту HH.ru
    """

    vacancies_url = 'https://api.hh.ru/vacancies'
    employers_url = 'https://api.hh.ru/employers'

    def __init__(self, keyword: str = None) -> None:
        self.params: Dict[str, Any] = {
            'area': '113',
            'text': keyword,
            'search_field': 'company_name',
            'per_page': 100,
            'page': 0,
            'only_with_vacancies': True
        }
        
        self._headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}
        self.list_of_vacancies: List[Vacancy] = []
        self.list_of_employers: List[Employer] = []

    def get_request(self, url: str) -> List[Dict[str, Any]]:
        """
        Функция принимает ссылку и возвращает список-JSON

        :param: url - str

        :return: response - jsonList
        """

        response = requests.get(url, params=self.params, headers=self._headers)
        return response.json()['items']

    def created_vacancy(self, vacancies: list):
        """
        Функция заполняет значения у вакансии и возвращает список вакансий

        :param: vacancies - List

        :return: list_of_vacancies - List
        """

        self.list_of_vacancies = [
            Vacancy(
                id=vacancy['id'],
                employer_id=vacancy.get('employer', {}).get('id'),
                name=vacancy['name'],
                salary_from=vacancy['salary']['from'] if vacancy['salary'] else None,
                salary_to=vacancy['salary']['to'] if vacancy['salary'] else None,
                description=vacancy['snippet']['responsibility'] if vacancy['snippet']['responsibility'] else 'no data',
                requirement=vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] else 'no data',
                area=vacancy['area']['name'],
                alternate_url=vacancy['alternate_url']
            )
            for vacancy in vacancies
        ]

        return self.list_of_vacancies

    def created_employer(self, vacancies: list):
        """
        Функция заполняет значения у работодателя и возвращает список из работодателей

        :param: vacancies - List

        :return: list_of_employers - List
        """

        ids = []
        for employer in vacancies:
            if employer['employer']['id'] not in ids:
                ids.append(employer['employer']['id'])
                self.list_of_employers.append(
                    Employer(
                        id=int(employer['employer']['id']),
                        name=employer['employer']['name'],
                        url=employer['employer']['alternate_url']
                    )
                )

        return self.list_of_employers

    def get_vacancies_by_employer_name(self, employer_name: str):
        """
        Функция для получения вакансии по наименованию работодателя

        :param: employer_name - str

        :return: vacancies_json - jsonList
        """

        self.params['text'] = employer_name
        vacancies_json = self.get_request(self.vacancies_url)

        return vacancies_json