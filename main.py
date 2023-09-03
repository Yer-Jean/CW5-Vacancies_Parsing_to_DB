from models.main_menu import MainMenu


def main() -> None:
    print('\n' + '─' * 60)
    print('Эта программа получает список компаний и их вакансии с HeadHunter.ru')
    print('Полученные данные сохраняются в базу данных')
    print('─' * 62)

    main_menu = MainMenu()
    main_menu()


if __name__ == '__main__':
    main()
