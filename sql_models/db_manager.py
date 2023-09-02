import os

import psycopg2
from dotenv import load_dotenv

from models.exceptions import SQLDataException


class DBManager:

    @classmethod
    def create_database(cls, database_name: str):
        # todo Написать обработку исключений для connection
        connection = psycopg2.connect(dbname='postgres', **cls.get_db_parameters())
        connection.autocommit = True
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"DROP DATABASE IF EXISTS {database_name} WITH (FORCE)")
            except psycopg2.errors.ObjectInUse:
                raise SQLDataException('Ошибка удаления базы данных')

            cursor.execute(f"CREATE DATABASE {database_name}")
        connection.close()

        connection = psycopg2.connect(dbname=database_name, **cls.get_db_parameters())
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url TEXT,
                    alternate_url TEXT,
                    vacancies_url TEXT,
                    open_vacancies INT
                )
            ''')

            cursor.execute('''
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    name VARCHAR NOT NULL,
                    city VARCHAR(127),
                    salary INT,
                    currency CHAR(3),
                    experience TEXT,
                    requirement TEXT,
                    alternate_url TEXT
                )
            ''')
        # connection.commit()
        connection.close()

    @classmethod
    def save_data_to_database(cls, data: list[dict], database_name: str):
        """Сохранение данных о компаниях и их вакансиях в базу данных."""
        connection = psycopg2.connect(dbname=database_name, **cls.get_db_parameters())
        with connection.cursor() as cursor:
            for employer in data:
                employer_data = employer['employers']
                cursor.execute('''
                    INSERT INTO employers (employer_id, name, url, alternate_url,
                    vacancies_url, open_vacancies) VALUES (%s, %s, %s, %s, %s, %s)''',
                    (int(employer_data['id']), employer_data['name'],
                     employer_data['url'], employer_data['alternate_url'],
                     employer_data['vacancies_url'], int(employer_data['open_vacancies']))
                )
                vacancies_data = employer['vacancies']

                for vacancy in vacancies_data:
                    salary = cls.get_vacancy_salary(vacancy)
                    if salary == 0:
                        continue
                    cursor.execute('''
                        INSERT INTO vacancies (vacancy_id, employer_id, name, city,
                        salary, currency, experience, requirement, alternate_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (int(vacancy['id']), int(employer_data['id']), vacancy['name'], vacancy['area']['name'],
                         salary, vacancy['salary']['currency'], vacancy['experience']['name'],
                         vacancy['snippet']['requirement'], vacancy['alternate_url'])
                    )
        connection.commit()
        connection.close()
        print('\nДанные по компаниям и их вакансиям записаны в базу данных\n')

    @staticmethod
    def get_db_parameters():
        load_dotenv()
        return {'host': os.environ.get('HOST'),
                'user': os.environ.get('USER_'),
                'password': os.environ.get('PASSWORD'),
                'port': os.environ.get('PORT')}

    @staticmethod
    def get_vacancy_salary(vacancy) -> int:
        salary_from = int(vacancy['salary'].get('from')) if vacancy['salary'].get('from') else 0
        salary_to = int(vacancy['salary'].get('to')) if vacancy['salary'].get('to') else 0
        salary: int = {
            salary_from == 0 and salary_to == 0: 0,
            salary_from > 0 and salary_to == 0: salary_from,
            salary_from == 0 and salary_to > 0: salary_to,
            salary_from > 0 and salary_to > 0: int((salary_from + salary_to) / 2)
        }[True]
        return salary
