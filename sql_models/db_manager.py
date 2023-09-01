import os

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

    def create_database(self, database_name):
        conn = psycopg2.connect(dbname='postgres', **self.parameters)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {database_name}")   # WITH (FORCE)
        except psycopg2.errors.ObjectInUse:
            raise SQLDataException('Ошибка удаления базы данных')

        cur.execute(f"CREATE DATABASE {database_name}")

        cur.close()
        conn.close()
