from models.hh_api import HeadHunterAPI
from models.menu_interaction_mixin import MenuInteractionMixin
from settings import HH_API_EMPLOYERS_URL, REQUESTS_PARAMS
from sql_models.db_manager import DBManager


class MainMenu(MenuInteractionMixin):
    def __init__(self):
        self.choice = True
        self.main_menu = {'1': ('Поиск компаний и их вакансий', self.search_companies_and_get_vacancies),
                          '2': ('Просмотр компаний и их вакансий', self.view_vacancies),
                          # '3': ('Очистить старые данные', self.clear_vacancies),
                          '0': ('Выход из программы', self.quit)}
        self.db_manager = DBManager()

    def __call__(self, *args, **kwargs):
        while self.choice:
            self.choice = self.menu_interaction(self.main_menu)
            self.main_menu[self.choice][1]()

    def search_companies_and_get_vacancies(self):
        data = []
        hh_api = HeadHunterAPI()

        search_string = input('Введите запрос для поиска компаний (одно или несколько слов)\n'
                              'Поиск осуществляется в названии компании и в её описании\n')
        employers_request_params = REQUESTS_PARAMS['employers']
        employers_request_params.update({'text': search_string})
        employers = hh_api.get_data(url=HH_API_EMPLOYERS_URL, **employers_request_params)
        print(f'Найдено {len(employers)} компаний')

        vacancies_request_params = REQUESTS_PARAMS['vacancies']
        for i in range(len(employers)):
            vacancies = hh_api.get_data(url=employers[i]['vacancies_url'], **vacancies_request_params)
            data.append({
                'employers': employers[i],
                'vacancies': vacancies
            })
        print(data)

        # if self.confirm('Сохранить в базу данных?'):
        #     self.db_manager.create_database('head_hunter')
        #     # db_manager.save_to_database('head_hunter')
        #     # todo: Написать вызов функции сохранения данных из класса DBManager
        #     print('сохранить')

    def view_vacancies(self):
        print('View')

    def clear_vacancies(self):
        if self.confirm('Очистить?'):
            print('yes')

    def quit(self):
        self.choice = False
