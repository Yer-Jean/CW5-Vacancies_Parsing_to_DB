import json

import requests

from models.exceptions import GetRemoteDataException


class HeadHunterAPI:

    def get_employers(self, search_string) -> list[dict] | None:
        """Метод возвращает список вакансий по заданному запросу search_string,
        используя HeadHunter API. Возвращает список словарей с данными о вакансиях"""
        pass

    def get_vacancies(self, search_string) -> list[dict] | None:
        """Метод возвращает список вакансий по заданному запросу search_string,
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
