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
            return True
        except:
            return False

    def get_user_by_credentials(self, username, password):
        query = f"SELECT * FROM {self.table} WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password, ))
        if self.cursor.fetchone() is not None:
            result = self.cursor.fetchone()[0]
        else:
            result = None
        return result
    
    