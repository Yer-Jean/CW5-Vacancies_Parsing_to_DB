import os

import psycopg2
from dotenv import load_dotenv

from models.exceptions import SQLDataException
from settings import DATABASE_NAME
from utils.data_utils import validate_key


class DBManager:

    @classmethod
    def create_database(cls):
        try:
            connection = psycopg2.connect(dbname='postgres', **cls.get_db_parameters())
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка подключения к базе данных')

        connection.autocommit = True
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME} WITH (FORCE);")
                cursor.execute(f"CREATE DATABASE {DATABASE_NAME};")
            except psycopg2.DatabaseError:
                raise SQLDataException('Ошибка создания базы данных')
        connection.close()

        try:
            connection = psycopg2.connect(dbname=DATABASE_NAME, **cls.get_db_parameters())
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка подключения к базе данных')
        connection.autocommit = True
        with connection.cursor() as cursor:
            try:
                cursor.execute('''
                    CREATE TABLE employers (
                        employer_id INT PRIMARY KEY,
                        employer_name VARCHAR(255) NOT NULL,
                        url TEXT,
                        alternate_url TEXT,
                        vacancies_url TEXT,
                        open_vacancies INT
                    );
                ''')
                cursor.execute('''
                    CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        employer_id INT REFERENCES employers(employer_id),
                        vacancy_name VARCHAR NOT NULL,
                        city VARCHAR(127),
                        salary INT,
                        currency CHAR(3),
                        experience TEXT,
                        requirement TEXT,
                        alternate_url VARCHAR(255)
                    );
                ''')
            except psycopg2.DatabaseError:
                raise SQLDataException('Ошибка создания таблиц в базе данных')
        connection.close()

    @classmethod
    def save_data_to_database(cls, data: list[dict]):
        """Сохранение данных о компаниях и их вакансиях в базу данных."""
        try:
            connection = psycopg2.connect(dbname=DATABASE_NAME, **cls.get_db_parameters())
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка подключения к базе данных')
        with connection.cursor() as cursor:
            for employer in data:
                employer_data = employer['employers']
                try:
                    cursor.execute('''
                        INSERT INTO employers (employer_id, employer_name, url, alternate_url,
                        vacancies_url, open_vacancies) VALUES (%s, %s, %s, %s, %s, %s);''',
                        (int(employer_data['id']), employer_data['name'],
                         employer_data['url'], employer_data['alternate_url'],
                         employer_data['vacancies_url'], int(employer_data['open_vacancies']))
                    )
                except psycopg2.DatabaseError:
                    raise SQLDataException('Ошибка сохранения данных в базу данных')

                vacancies_data = employer['vacancies']
                for vacancy in vacancies_data:
                    salary = cls.get_vacancy_salary(vacancy)
                    if salary == 0:
                        continue
                    try:
                        cursor.execute('''
                            INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name,
                            city, salary, currency, experience, requirement, alternate_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);''',
                            (int(vacancy['id']), int(employer_data['id']), vacancy['name'], vacancy['area']['name'],
                             salary, vacancy['salary']['currency'], vacancy['experience']['name'],
                             vacancy['snippet']['requirement'], vacancy['alternate_url'])
                        )
                    except psycopg2.DatabaseError:
                        raise SQLDataException('Ошибка сохранения данных в базу данных')
        connection.commit()
        connection.close()
        print('\n' + '─' * 60)
        print('Данные по компаниям и их вакансиям, в которых'
              '\nуказаны размеры оплаты, записаны в базу данных')
        print('─' * 60)

    @classmethod
    def get_companies_and_vacancies_count(cls, cursor) -> list:
        """Метод запрашивает список всех компаний и количество вакансий у каждой компании."""
        try:
            cursor.execute('''
                SELECT employer_name, COUNT(*) AS vacancies_count FROM vacancies
                INNER JOIN employers USING(employer_id)
                GROUP BY employer_name
                ORDER BY vacancies_count DESC;''')
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка получения данных из базы данных')
        return cursor.fetchall()

    @classmethod
    def get_all_vacancies(cls, cursor) -> list:
        """Метод запрашивает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        try:
            cursor.execute('''
                SELECT employer_name, vacancy_name, salary, vacancies.alternate_url
                FROM vacancies
                INNER JOIN employers USING(employer_id);''')
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка получения данных из базы данных')
        return cursor.fetchall()

    @classmethod
    def get_avg_salary(cls, cursor) -> int:
        """Метод запрашивает среднюю зарплату по вакансиям."""
        try:
            cursor.execute('SELECT AVG(salary) FROM vacancies;')
            data = cursor.fetchone()[0]
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка получения данных из базы данных')
        return int(data)

    @classmethod
    def get_vacancies_with_higher_salary(cls, cursor) -> list:
        """Метод запрашивает список всех вакансий, у которых зарплата выше
        средней по всем вакансиям."""
        try:
            query_string = f'''
                SELECT employer_name, vacancy_name, salary, vacancies.alternate_url
                FROM vacancies
                INNER JOIN employers USING(employer_id)
                WHERE salary > {cls.get_avg_salary(cursor)}
                ORDER BY employer_name;'''
            cursor.execute(query_string)
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка получения данных из базы данных')
        return cursor.fetchall()

    @classmethod
    def get_vacancies_with_keyword(cls, cursor, search_string: str) -> list:
        """Метод запрашивает список всех вакансий, в названии которых содержатся слова
        из запроса введенного пользователем."""
        query_string = f'''
            SELECT employer_name, vacancy_name, salary, vacancies.alternate_url
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            WHERE vacancy_name LIKE '%{search_string}%' OR requirement LIKE '%{search_string}%'
            ORDER BY employer_name;'''
        try:
            cursor.execute(query_string)
        except psycopg2.DatabaseError:
            raise SQLDataException('Ошибка получения данных из базы данных')
        return cursor.fetchall()

    @staticmethod
    def get_db_parameters():
        """Метод запрашивает параметры подключения к базе данных из файла .env"""
        load_dotenv()
        return {'host': os.environ.get('HOST'),
                'user': os.environ.get('USER_'),
                'password': os.environ.get('PASSWORD'),
                'port': os.environ.get('PORT')}

    @staticmethod
    def get_vacancy_salary(vacancy) -> int:
        """Метод обрабатывает поля зарплаты вакансии и возвращает ее"""
        salary_from = validate_key(vacancy, 'int', 'salary', 'from')
        salary_to = validate_key(vacancy, 'int', 'salary', 'to')

        salary: int = {
            salary_from == 0 and salary_to == 0: 0,
            salary_from > 0 and salary_to == 0: salary_from,
            salary_from == 0 and salary_to > 0: salary_to,
            salary_from > 0 and salary_to > 0: (salary_from + salary_to) / 2
        }[True]
        return salary
