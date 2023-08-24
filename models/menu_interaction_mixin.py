class MenuInteractionMixin:

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
                print('\nНеправильный выбор. Выберите один из доступных вариантов.')
                continue
            return choice

    @staticmethod
    def confirm(question: str) -> bool:
        while True:
            choice: str = input(f'{question} (yes/no)').lower()
            match choice:
                case 'yes':
                    return True
                case 'no':
                    return False
                case _:
                    print('\nНеправильный выбор. Выберите "yes" или "no"')
