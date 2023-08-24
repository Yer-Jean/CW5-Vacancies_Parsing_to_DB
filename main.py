from models.menu import MainMenu


def main() -> None:
    print('\nЭта программа получает список компаний и их вакансии с HeadHunter.ru:')
    main_menu = MainMenu()
    main_menu()


if __name__ == '__main__':
    main()
