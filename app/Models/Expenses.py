import sqlite3
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

    def record(self, **kwargs):
        try:
            self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES({', '.join(['?'] * len(kwargs.values()))})", list(kwargs.values()))
            self.connection.commit()
            return True
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            return False
        
    def history(self, start_date, end_date):
        result = self.cursor.execute(f"SELECT amount, description, category, type, date, amount_usd, amount_gbp FROM {self.table} WHERE date >= ? AND date <= ? ORDER BY type, date ASC", (start_date, end_date,))
        return result.fetchall()