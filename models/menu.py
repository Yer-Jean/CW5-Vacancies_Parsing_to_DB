class MainMenu:
    def __init__(self):
        self.main_menu = {'1': ('Поиск компаний и их вакансий', self.search_companies),
                          '2': ('Просмотр компаний и их вакансий', self.view_vacancies),
                          '3': ('Очистить старые данные', self.clear_vacancies),
                          '0': ('Выход из программы', self.quit)}
    def __call__(self, *args, **kwargs):
        choice =  self.menu_interaction(self.main_menu)
        self.main_menu[choice][1]()

    def search_companies(self):
        print('Search')

    def view_vacancies(self):
        print('View')

    def clear_vacancies(self):
        print('Clear')

    def quit(self):
        return

    @staticmethod
    def menu_interaction(menu: dict) -> str:
        """Печатает доступные опции меню выбора в консоль.
        :param menu: Пункты меню.
        :return: Выбранная опция меню.
        """
        # print('\n')
        print('\n'.join([f"({key}) {value[0]}" for key, value in menu.items()]))

        while True:
            choice: str = input('\nВыберите пункт меню: ')
            if choice not in menu:
                print("\nНеправильный выбор. Выберите один из доступных вариантов.")
                continue
            return choice
