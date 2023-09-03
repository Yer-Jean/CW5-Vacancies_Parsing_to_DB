import json

import requests

from models.exceptions import GetRemoteDataException


class HeadHunterAPI:
    """Класс для получения данных с сайта hh.ru используя API"""
    def get_data(self, url: str, **params) -> list[dict] | None:
        """Метод возвращает список записей в зависимости от параметров params
        используя HeadHunter API. Возвращает список словарей с полученными записями"""
        data: list[dict] = []
        current_page: int = 0
        start: bool = True

        while True:
            try:  # Получаем данные о компаниях, используя HeadHunter API
                response = self.get_remote_data(url=url, params=params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('Попробуйте немного позже или измените параметры запроса\n')
                return None

            if start:
                num_of_pages: int = response['pages']  # Получаем количество страниц найденных записей
                num_of_items: int = response['found']  # Получаем общее количество найденных записей
                if num_of_items == 0:  # Если не найдена ни одна компаний, то возвращаем None
                    return None
                start = False

            # Из полученного ответа забираем только список записей
            data.extend(response.get('items'))

            current_page += 1  # Переходим к следующей странице результатов
            params.update({'page': current_page})
            if current_page == num_of_pages + 1:    # Когда достигли последней страницы с записями
                return data                         # возвращаем их список

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
