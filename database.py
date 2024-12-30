import sqlite3


class DateBase:

    def __init__(self):
        self._con = None
        self.history_len = 0

    def __enter__(self):
        self._con = sqlite3.connect("./database.db")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._con is not None:
            self._con.close()

    def create_table(self):
        cursor = self._con.cursor()
        cursor.execute(
            """
            create table if not exists history (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date text not null,
            city text not null,
            weather text not null,
            temperature text not null,
            feels_like text not null,
            wind_speed text not null
            )
        """
        )
        self._con.commit()

    def insert_data(self, info):
        cursor = self._con.cursor()
        cursor.execute(
            f"""
            insert into history (date, city, weather, temperature, feels_like, wind_speed)
            values
                ('{info[0]}', '{info[1]}', '{info[2]}', '{info[3]}', '{info[4]}', '{info[5]}')
        """
        )
        self._con.commit()

    def select_data(self, num: int):
        cursor = self._con.cursor()
        cursor.execute(
            """
            select date, city, weather, temperature, feels_like, wind_speed from history
        """
        )
        history = cursor.fetchall()
        self.history_len = len(history)
        try:
            if 1 <= num <= self.history_len:
                print("date, city, weather, temperature, feels_like, wind_speed")
                for _ in range(self.history_len-num, self.history_len):
                    print(*history[_])
                print("\n")
            elif self.history_len == 0:
                print('Прежде чем смотреть историю запросов, необходимо сделать хотя бы один)')
            else:
                raise IndexError
        except sqlite3.OperationalError:
            print('Ошибка с базой данных')
