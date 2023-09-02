from models.hh_api import HeadHunterAPI
from models.menu_interaction_mixin import MenuInteractionMixin
from sql_models.db_manager import DBManager
from utils.data_utils import search_employers, get_vacancies_from_employers


class MainMenu(MenuInteractionMixin):
    def __init__(self):
        self.choice = True
        self.main_menu = {'1': ('Поиск компаний и их вакансий', self.search_companies_and_get_vacancies),
                          '2': ('Просмотр компаний и их вакансий', self.view_vacancies_from_db),
                          # '3': ('Очистить старые данные', self.clear_vacancies),
                          '0': ('Выход из программы', self.quit)}
        # self.db_manager = DBManager()

    def __call__(self, *args, **kwargs):
        while self.choice:
            self.choice = self.menu_interaction(self.main_menu)
            self.main_menu[self.choice][1]()

    def search_companies_and_get_vacancies(self):
        # Создаем экземпляр класса для работы по API с сайтом headhunter.ru
        hh_api = HeadHunterAPI()

        employers = search_employers(hh_api)
        if not employers:
            return

        employers_with_vacancies = get_vacancies_from_employers(hh_api, employers)

        DBManager.create_database('head_hunter')
        # self.db_manager.create_database('head_hunter')
        DBManager.save_data_to_database(employers_with_vacancies, 'head_hunter')

    def view_vacancies_from_db(self):
        print('View')

    def clear_vacancies(self):
        if self.confirm('Очистить?'):
            print('yes')

    def quit(self):
        self.choice = False
