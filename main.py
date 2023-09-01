from models.main_menu import MainMenu
from sql_models.db_manager import DBManager


def main() -> None:
    print('\nЭта программа получает список компаний и их вакансии с HeadHunter.ru\n')

    # todo: Сделать запрос в БД и вытащить количество компаний и их вакансий
    print('Сейчас в базе данных сохранены {N} компаний, которые разместили {M} вакансий\n')
    db_manager = DBManager()
    main_menu = MainMenu()
    main_menu()


if __name__ == '__main__':
    main()
