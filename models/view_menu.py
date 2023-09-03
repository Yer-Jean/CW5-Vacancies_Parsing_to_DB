import psycopg2

from models.exceptions import SQLDataException
from models.menu_interaction_mixin import MenuInteractionMixin
from settings import DATABASE_NAME
from sql_models.db_manager import DBManager
from utils.output_utils import print_companies_and_vacancies_count, print_all_vacancies, print_avg_salary


class ViewMenu(MenuInteractionMixin):
    """
    Класс ViewMenu выводит на экран меню просмотра компаний и их вакансий,
    получает выбор пользователя и, в соответствии с ним, запускает методы класса
    """
    def __init__(self):
        self.choice = True
        self.view_menu = {'1': ('Просмотр компаний и количество их вакансий', self.show_companies_and_vacancies_count),
                          '2': ('Просмотр всех вакансий', self.show_all_vacancies),
                          '3': ('Просмотр средней зарплаты по вакансиям', self.show_avg_salary),
                          '4': ('Просмотр вакансий с зарплатой выше средней', self.show_vacancies_with_higher_salary),
                          '5': ('Просмотр вакансий по ключевому слову', self.show_vacancies_with_keyword),
                          '0': ('Переход в предыдущее меню', self.back)}

    def __call__(self, *args, **kwargs):
        try:  # Создаем подключение к базе данных
            self.connection = psycopg2.connect(dbname=DATABASE_NAME, **DBManager.get_db_parameters())
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка подключения к базе данных')
        self.cursor = self.connection.cursor()
        # Отображаем меню и ожидаем выбор пользователя
        while self.choice:
            self.choice = self.menu_interaction(self.view_menu)
            self.view_menu[self.choice][1]()
        self.cursor.close()
        self.connection.close()

    def show_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании.
         Затем выводит этот список на печать."""
        try:
            data: list = DBManager.get_companies_and_vacancies_count(self.cursor)
        except SQLDataException as err:
            print(err.message)
            return
        print_companies_and_vacancies_count(data)

    def show_all_vacancies(self):
        """Метод получает список всех вакансий с указанием названия компании, названия
        вакансии и зарплаты и ссылки на вакансию. Затем выводит этот список на печать."""
        try:
            data: list = DBManager.get_all_vacancies(self.cursor)
        except SQLDataException as err:
            print(err.message)
            return
        print_all_vacancies(data)

    def show_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям и печатает её."""
        try:
            data: int = DBManager.get_avg_salary(self.cursor)
        except SQLDataException as err:
            print(err.message)
            return
        print_avg_salary(data)

    def show_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше
        средней по всем вакансиям. Затем выводит этот список на печать."""
        try:
            data: list = DBManager.get_vacancies_with_higher_salary(self.cursor)
        except SQLDataException as err:
            print(err.message)
            return
        print_all_vacancies(data)

    def show_vacancies_with_keyword(self):
        """Метод получает список всех вакансий, в названии которых содержатся слова
        из запроса введенного пользователем. Затем выводит этот список на печать."""
        search_string = input('\nВведите запрос для поиска вакансий\n'
                              'Поиск осуществляется в названии вакансии и в требованиях для неё\n')
        try:
            data: list = DBManager.get_vacancies_with_keyword(self.cursor, search_string)
        except SQLDataException as err:
            print(err.message)
            return
        if data:
            print_all_vacancies(data)
        else:
            print(f'По запросу "{search_string}" ничего не найдено')

    def back(self):
        """Возврат в предыдущее меню"""
        self.choice = False
