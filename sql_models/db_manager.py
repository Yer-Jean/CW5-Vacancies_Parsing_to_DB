import os
from typing import Any

import psycopg2
from dotenv import load_dotenv

from models.exceptions import SQLDataException


class DBManager:

    def __init__(self):
        load_dotenv()
        self.parameters = {'host': os.environ.get('HOST'),
                           'user': os.environ.get('USER_'),
                           'password': os.environ.get('PASSWORD'),
                           'port': os.environ.get('PORT')}

    def create_database(self, database_name: str):
        # todo Написать обработку исключений для connection
        connection = psycopg2.connect(dbname='postgres', **self.parameters)
        connection.autocommit = True
        # cur = conn.cursor()
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"DROP DATABASE IF EXISTS {database_name} WITH (FORCE)")
            except psycopg2.errors.ObjectInUse:
                raise SQLDataException('Ошибка удаления базы данных')

            cursor.execute(f"CREATE DATABASE {database_name}")
            # cursor.close()
        connection.close()

        connection = psycopg2.connect(dbname=database_name, **self.parameters)
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
                    employment VARCHAR(20),
                    schedule VARCHAR(20),
                    salary_from INT,
                    salary_to INT,
                    currency CHAR(3),
                    experience TEXT,
                    requirement TEXT,
                    alternate_url TEXT
                )
            ''')
        # connection.commit()
        connection.close()

    def save_data_to_database(self, data: list[dict[str, Any]], database_name: str):
        """Сохранение данных о каналах и видео в базу данных."""

        connection = psycopg2.connect(dbname=database_name, **self.parameters)
