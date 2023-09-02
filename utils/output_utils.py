def print_companies_and_vacancies_count(data: list):
    # Выводим шапку таблицы
    print('\n')
    print('┌' + '─' * 50 + '┬' + '─' * 25 + '┐')
    print('│ НАИМЕНОВАНИЕ КОМПАНИИ                            │ КОЛИЧЕСТВО ВАКАНСИЙ     │')
    print('├' + '─' * 50 + '┼' + '─' * 25 + '┤')
    # Выводим периодическую часть таблицы
    for item in data:
        print(f'│ {item[0]:<49}│ {item[1]:<24}│')
    # Выводим подвал таблицы
    print('└' + '─' * 50 + '┴' + '─' * 25 + '┘\n')


def print_all_vacancies(data: list):
    # Переменная company_name_for_table вводится для избегания повторений наименования
    # компании в списке вакансий, если компания разместила несколько вакансий
    company_name_for_table: str = ''
    # Выводим шапку таблицы
    print('\n')
    print('┌' + '─' * 40 + '┬' + '─' * 40 + '┬' + '─' * 10 + '┐')
    print('│ НАИМЕНОВАНИЕ КОМПАНИИ                  │ НАИМЕНОВАНИЕ ВАКАНСИИ                  │ ЗАРПЛАТА │')
    # Выводим периодическую часть таблицы
    for item in data:
        item_0 = f'{item[0][:35]}...' if len(item[0]) > 38 else item[0]
        if company_name_for_table == item_0:
            item_0 = ''
        else:
            company_name_for_table = item_0
            print('├' + '─' * 40 + '┼' + '─' * 40 + '┼' + '─' * 10 + '┤')
        item_1 = f'{item[1][:35]}...' if len(item[1]) > 38 else item[1]
        print(f'│ {item_0:<39}│ {item_1:<39}│ {item[2]:<9}│')
    # Выводим подвал таблицы
    print('└' + '─' * 40 + '┴' + '─' * 40 + '┴' + '─' * 10 + '┘\n')


def print_avg_salary(data: int):
    print('\n' + '─' * 62)
    print(f' СРЕДНЯЯ ЗАРПЛАТА ПО СОХРАНЕННЫМ ВАКАНСИЯМ СОСТАВЛЯЕТ: {data}')
    print('─' * 62)
