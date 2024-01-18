import sqlite3

class Database:

    def __init__(self, db_path) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()