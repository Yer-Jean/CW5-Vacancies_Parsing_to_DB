import psycopg2

from models.menu_interaction_mixin import MenuInteractionMixin
from settings import DATABASE_NAME
from sql_models.db_manager import DBManager
from utils.output_utils import print_companies_and_vacancies_count, print_all_vacancies, print_avg_salary


class ViewMenu(MenuInteractionMixin):
    def __init__(self):
        self.choice = True
        self.view_menu = {'1': ('Просмотр компаний и количество их вакансий', self.show_companies_and_vacancies_count),
                          '2': ('Просмотр всех вакансий', self.show_all_vacancies),
                          '3': ('Просмотр средней зарплаты по вакансиям', self.show_avg_salary),
                          '4': ('Просмотр вакансий с зарплатой выше средней', self.show_vacancies_with_higher_salary),
                          '5': ('Просмотр вакансий по ключевому слову', self.show_vacancies_with_keyword),
                          '0': ('Переход в предыдущее меню', self.back)}

    def __call__(self, *args, **kwargs):
        self.connection = psycopg2.connect(dbname=DATABASE_NAME, **DBManager.get_db_parameters())
        self.cursor = self.connection.cursor()
        while self.choice:
            self.choice = self.menu_interaction(self.view_menu)
            self.view_menu[self.choice][1]()
        self.cursor.close()
        self.connection.close()

    def show_companies_and_vacancies_count(self):
        data: list = DBManager.get_companies_and_vacancies_count(self.cursor)
        print_companies_and_vacancies_count(data)

    def show_all_vacancies(self):
        data: list = DBManager.get_all_vacancies(self.cursor)
        print_all_vacancies(data)

    def show_avg_salary(self):
        data: int = DBManager.get_avg_salary(self.cursor)
        print_avg_salary(data)


    def show_vacancies_with_higher_salary(self):
        data: list = DBManager.get_vacancies_with_higher_salary(self.cursor)
        print_all_vacancies(data)

    def show_vacancies_with_keyword(self):
        search_string = input('\nВведите запрос для поиска вакансий (одно или несколько слов)\n'
                              'Поиск осуществляется в названии вакансии и в её требованиях\n')
        data: list = DBManager.get_vacancies_with_keyword(self.cursor, search_string)
        if data:
            print_all_vacancies(data)
        else:
            print(f'По запросу "{search_string}" ничего не найдено')

    def back(self):
        self.choice = False
