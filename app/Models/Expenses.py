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
                    amount INTEGER NOT NULL,
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
