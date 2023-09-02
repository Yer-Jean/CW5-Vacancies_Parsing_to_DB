from models.menu_interaction_mixin import MenuInteractionMixin


class ViewMenu(MenuInteractionMixin):
    def __init__(self):
        self.choice = True
        self.view_menu = {'1': ('Просмотр компаний и количество их вакансий', self.get_companies_and_vacancies_count),
                          '2': ('Просмотр всех вакансий', self.get_all_vacancies),
                          '3': ('Просмотр средней зарплаты по вакансиям', self.get_avg_salary),
                          '4': ('Просмотр вакансий с зарплатой выше средней', self.get_vacancies_with_higher_salary),
                          '5': ('Просмотр вакансий по ключевому слову', self.get_vacancies_with_keyword),
                          '0': ('Переход в предыдущее меню', self.back)}

    def __call__(self, *args, **kwargs):
        while self.choice:
            self.choice = self.menu_interaction(self.view_menu)
            self.view_menu[self.choice][1]()

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

    def back(self):
        self.choice = False