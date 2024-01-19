import sqlite3
import traceback
import sys
from app.Services.database import Database

class Expenses(Database):

    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = "expenses"
        self.create_table()

    def create_table(self):
        query = f'''
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    date INTEGER NOT NULL,
                    amount_usd REAL NOT NULL,
                    amount_gbp REAL NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            '''
        self.cursor.execute(query)
        self.connection.commit()

    def record_expenses(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return True
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return False