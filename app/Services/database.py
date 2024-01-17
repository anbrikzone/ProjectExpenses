import sqlite3

class Database:

    def __init__(self, db_path) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
    
    def create(self, **kwargs):
        values = {}
        # for key, value in kwargs.items():
        #     values.append(key)
        self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(kwargs.keys())}) VALUES ({', '.join(['?'] * len(values))})", list(kwargs.values()))
        self.connection.commit()