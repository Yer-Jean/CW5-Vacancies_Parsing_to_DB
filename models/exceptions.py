"""Классы для исключений при работе программы"""


class DataException(Exception):
    def __init__(self, message):
        self.message = '\n' + '─' * 60 + '\n' + message + '\n' + '─' * 60


class GetRemoteDataException(DataException):
    def __init__(self, message):
        super().__init__(message)


class SQLDataException(DataException):
    def __init__(self, message):
        super().__init__(message)
