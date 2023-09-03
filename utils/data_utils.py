from typing import Any

from models.hh_api import HeadHunterAPI
from settings import REQUESTS_PARAMS, HH_API_EMPLOYERS_URL


def search_employers(hh_api: HeadHunterAPI) -> list[dict] | None:
    """Метод получает список компаний с сайта hh.ru, найденных
     по запросу пользователя и возвращает его"""
    search_string = input('\nВведите запрос для поиска компаний (одно или несколько слов)\n'
                          'Поиск осуществляется в названии компании и в её описании\n')
    # Добавляем к параметрам запроса на сайт hh.ru строку поиска по компаниям
    employers_request_params = REQUESTS_PARAMS['employers']
    employers_request_params.update({'text': search_string})
    employers = hh_api.get_data(url=HH_API_EMPLOYERS_URL, **employers_request_params)
    # Выводим статистику по запросу
    print('\n' + '─' * 60)
    if employers:
        print(f'По запросу "{search_string}" найдено {len(employers)} компаний'
              f'\nПоказаны компании с открытыми вакансиями:\n')
        return employers
    print(f'\nПо запросу "{search_string}" ничего не найдено')
    return None


def get_vacancies_from_employers(hh_api: HeadHunterAPI, employers: list[dict]) -> list[dict] | None:
    """Метод получает все вакансии компаний из списка employers,
    объединяет оба списка в общий список и возвращает его"""
    employers_with_vacancies = []  # Список, в который поместим все найденные компании и их вакансии
    vacancies_request_params = REQUESTS_PARAMS['vacancies']
    for i in range(len(employers)):
        open_vacancies = employers[i]["open_vacancies"]
        if open_vacancies > 0:
            vacancies = hh_api.get_data(url=employers[i]['vacancies_url'], **vacancies_request_params)
            # Выводим статистику по запросу
            print(f'{employers[i]["name"]}: вакансий - {open_vacancies}')
            employers_with_vacancies.append({
                'employers': employers[i],
                'vacancies': vacancies
            })
    print('─' * 60)
    return employers_with_vacancies


def validate_key(data: list, value_type: str, key: str, sub_key: str) -> Any:
    """
    В принимаемом словаре data проверяется наличие значений по
    ключу key. Если значение не пустое, то проверяется наличие значений
    по подключу sub_key. Если таких значений нет, то возвращаем пустое
    значение в соответствии с типом ожидаемых данных value_type,
    если есть, то - значение находящееся по ключу subkey.

    (За отсутствием необходимости, в данной задаче не рассматриваем
    бОльшую вложенность словарей: data[key][sub_key1][sub_key2]...итд)

    :param data: словарь с данными
    :param value_type: тип возвращаемого значения
    :param key: ключ
    :param sub_key: подключ
    :return: значение, полученное по цепочке ключей
    """
    value: Any = None

    if data[key] is not None and data[key][sub_key] is not None:
        value = data[key][sub_key]
    else:
        match value_type:
            case 'int':
                value = 0
            case 'float':
                value = 0.0
            case 'str':
                value = ''
            case 'bool':
                value = False
            case 'list':
                value = []
            case 'dict':
                value = {}
            case 'tuple':
                value = ()
    return value
