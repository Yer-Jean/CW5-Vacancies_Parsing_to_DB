DATABASE_NAME = 'head_hunter'

HH_API_VACANCIES_URL = 'https://api.hh.ru/vacancies'
HH_API_EMPLOYERS_URL = 'https://api.hh.ru/employers'

EMPLOYERS_RESULTS_PER_PAGE = 10
VACANCIES_RESULTS_PER_PAGE = 100

REQUESTS_PARAMS = {'employers': {'per_page': EMPLOYERS_RESULTS_PER_PAGE,
                                 'page': 0,
                                 'type': 'company',
                                 'sort_by': 'by_vacancies_open'},
                   'vacancies': {'per_page': VACANCIES_RESULTS_PER_PAGE,
                                 'page': 0}}
