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
    
    def create_user(self, first_name, last_name, username, email, password):
        super().create({'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email, 'password': password})
