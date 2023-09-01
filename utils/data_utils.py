from models.hh_api import HeadHunterAPI
from settings import REQUESTS_PARAMS, HH_API_EMPLOYERS_URL


def search_employers(hh_api: HeadHunterAPI) -> list[dict] | None:
    search_string = input('\nВведите запрос для поиска компаний (одно или несколько слов)\n'
                          'Поиск осуществляется в названии компании и в её описании\n')
    employers_request_params = REQUESTS_PARAMS['employers']
    employers_request_params.update({'text': search_string})
    employers = hh_api.get_data(url=HH_API_EMPLOYERS_URL, **employers_request_params)
    # Выводим статистику по запросу
    if employers:
        print(f'\nПо запросу "{search_string}" найдено {len(employers)} компаний'
              f'\nПоказаны компании с открытыми вакансиями:\n')
        return employers
    print(f'\nПо запросу "{search_string}" ничего не найдено')
    return None


def get_vacancies_from_employers(hh_api: HeadHunterAPI, employers: list[dict]) -> list[dict] | None:
    employers_with_vacancies = []  # Список, в который поместим все найденные компании и их вакансии
    vacancies_request_params = REQUESTS_PARAMS['vacancies']
    for i in range(len(employers)):
        open_vacancies = employers[i]["open_vacancies"]
        if open_vacancies > 0:
            vacancies = hh_api.get_data(url=employers[i]['vacancies_url'], **vacancies_request_params)
            # Выводим статистику по запросу
            print(f'{employers[i]["name"]}: вакансий - {open_vacancies} ')
            employers_with_vacancies.append({
                'employers': employers[i],
                'vacancies': vacancies
            })
    return employers_with_vacancies
