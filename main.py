from models.main_menu import MainMenu


def main() -> None:
    print('\n' + '─' * 76)
    print(' Эта программа получает список компаний и их вакансии с сайта HeadHunter.ru')
    print(' Полученные данные сохраняются в базу данных')
    print('─' * 76)

    main_menu = MainMenu()
    main_menu()


if __name__ == '__main__':
    main()
