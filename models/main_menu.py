from models.hh_api import HeadHunterAPI
from models.view_menu import ViewMenu
from models.menu_interaction_mixin import MenuInteractionMixin
from sql_models.db_manager import DBManager
from models.exceptions import SQLDataException
from utils.data_utils import search_employers, get_vacancies_from_employers


class MainMenu(MenuInteractionMixin):
    """
    Класс MainMenu выводит на экран главное меню, получает выбор пользователя
    и, в соответствии с ним, запускает методы класса
    """
    def __init__(self):
        self.choice = True
        self.main_menu = {'1': ('Поиск компаний и их вакансий', self.search_companies_and_get_vacancies),
                          '2': ('Просмотр компаний и их вакансий', self.view_vacancies_from_db),
                          '0': ('Выход из программы', self.quit)}

    def __call__(self, *args, **kwargs):
        # Отображаем меню и ожидаем выбор пользователя
        while self.choice:
            self.choice = self.menu_interaction(self.main_menu)
            self.main_menu[self.choice][1]()

    @staticmethod
    def search_companies_and_get_vacancies():
        """
        Метод получает через API сайта hh.ru найденные компании и их вакансии
        и записывает эту информацию в базу данных. При этом ранее сохраненные
        данные удаляются
        """
        # Создаем экземпляр класса для работы по API с сайтом hh.ru
        hh_api = HeadHunterAPI()

        # Получаем список компаний
        employers: list = search_employers(hh_api)
        if not employers:  # Если список пустой, то возвращаемся назад
            return
        # Получаем все вакансии ранее полученных компаний
        employers_with_vacancies: list = get_vacancies_from_employers(hh_api, employers)

        try:
            # Создаем базу данных
            DBManager.create_database()
            # Записываем в нее сведения о компаниях и их вакансиях
            DBManager.save_data_to_database(employers_with_vacancies)
        except SQLDataException as err:
            print(err.message)

    @staticmethod
    def view_vacancies_from_db():
        """Метод создает экземпляр класса ViewMenu
        (меню просмотра компаний и их вакансий) и запускает его"""
        view_menu = ViewMenu()
        view_menu()

    def quit(self):
        """Выход из программы"""
        self.choice = False
