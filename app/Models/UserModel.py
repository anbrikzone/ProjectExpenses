import sqlite3
import traceback
import sys
from app.Services.database import Database

class Users(Database):

    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = "users"
        self.create_table()

    def create_table(self):
        query = f'''
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            '''
        self.cursor.execute(query)
        self.connection.commit()
    
    def create_user(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return 0

    def get_pass_by_username(self, username):
        self.cursor.execute(f"SELECT id, password FROM {self.table} WHERE username = ?", [username])
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None
    
    