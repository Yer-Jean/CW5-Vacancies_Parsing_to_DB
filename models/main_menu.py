from models.hh_api import HeadHunterAPI
from models.menu_interaction_mixin import MenuInteractionMixin


class MainMenu(MenuInteractionMixin):
    def __init__(self):
        self.choice = True
        self.main_menu = {'1': ('Поиск компаний и их вакансий', self.search_companies),
                          '2': ('Просмотр компаний и их вакансий', self.view_vacancies),
                          '3': ('Очистить старые данные', self.clear_vacancies),
                          '0': ('Выход из программы', self.quit)}

    def __call__(self, *args, **kwargs):
        while self.choice:
            self.choice = self.menu_interaction(self.main_menu)
            self.main_menu[self.choice][1]()

    def search_companies(self):
        hh_api = HeadHunterAPI()
        search_string = input('Введите запрос для поиска компаний (одно или несколько слов)\n'
                              'Поиск осуществляется в названии компании и в её описании\n')
        hh_api.get_employers(search_string)
        # if self.confirm('Сохранить в базу данных?'):
            # todo: Написать вызов функции сохранения данных из класса DBManager
            # print('сохранить')

    def view_vacancies(self):
        print('View')

    def clear_vacancies(self):
        if self.confirm('Очистить?'):
            print('yes')

    def quit(self):
        self.choice = False
        return
