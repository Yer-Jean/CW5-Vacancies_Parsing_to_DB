import json

import requests

from models.exceptions import GetRemoteDataException


class HeadHunterAPI:

    __hh_api_url = 'https://api.hh.ru/employers'
    RESULTS_PER_PAGE = 10

    def get_employers(self, search_string) -> list[dict] | None:
        """Метод возвращает список вакансий по заданному запросу search_string,
        используя HeadHunter API. Возвращает список словарей с данными о вакансиях"""
        employers = []
        current_page = 0
        request_params = {'type': 'company',
                          'text': search_string,
                          'per_page': self.RESULTS_PER_PAGE,
                          'page': current_page,
                          'sort_by': 'by_vacancies_open'}
        # num_of_pages = 0
        # num_of_employers = 0

        try:  # Получаем данные о вакансиях используя HeadHunter API
            data = self.get_remote_data(url=self.__hh_api_url, params=request_params)
        except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
            print(err.message)
            print('Попробуйте немного позже или измените параметры запроса\n')
            return None

        num_of_employers = data["found"]
        if num_of_employers == 0:
            print(f'По запросу "{search_string}" компании не найдены')
            return None

        print(f'Найдено {num_of_employers} компаний')
        return data['items']

    def get_vacancies(self, vacancies_url) -> list[dict] | None:
        """Метод возвращает список вакансий по указанному URL,
        используя HeadHunter API. Возвращает список словарей с данными о вакансиях"""
        pass

    @staticmethod
    def get_remote_data(**kwargs) -> dict | None:
        """Метод получает ответ сайта по API в формате JSON.
        В случае успеха возвращает словарь с данными.
        В случае ошибки возвращает None, при этом обрабатываются
        как сетевые(web) исключения, так и ошибки ответа сайта.
        Кроме того, проверяется корректность JSON-формата.
        Все исключения обрабатываются в классе GetRemoteDataException
        """
        try:
            response = requests.get(**kwargs)
        except requests.exceptions.ConnectionError:
            raise GetRemoteDataException('\nНе найден сайт или ошибка сети')
        except requests.exceptions.HTTPError:
            raise GetRemoteDataException('\nНекорректный HTTP ответ')
        except requests.exceptions.Timeout:
            raise GetRemoteDataException('\nВышло время ожидания ответа')
        except requests.exceptions.TooManyRedirects:
            raise GetRemoteDataException('\nПревышено максимальное значение перенаправлений')

        if response.status_code != 200:  # Все ответы сайта, кроме - 200, являются ошибочными
            raise GetRemoteDataException(f'\nОшибка {response.status_code} - {response.reason}')

        # Пытаемся декодировать JSON
        try:
            data: dict = response.json()
        except json.decoder.JSONDecodeError:
            raise GetRemoteDataException('\nОшибка в формате данных')

        # Возвращаем словарь с данными, если не возникло каких-либо ошибок
        return data


if __name__ == '__main__':
    pass
