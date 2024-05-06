import fdb

# подключение к БД
DB_CONNECTION_STRING = r"C:/Users/borck/PycharmProjects/ACSv2/ACS"
DB_USERNAME = "sysdba"
DB_PASSWORD = "12345"
DB_CHARSET = "utf8"


# Класс для подключения к базе данных и выполнению запросов
class DBConnection:
    def __init__(self) -> None:
        self.conn = fdb.connect(
            dsn=DB_CONNECTION_STRING,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            charset=DB_CHARSET,
        )
        self.cur = self.conn.cursor()
