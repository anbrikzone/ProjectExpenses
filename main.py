from app.Models.UserModel import Users
from app.Models.Expenses import Expenses
from app.Services.ExchangeApi import CurrencyExchangeApi

db = r"app\Database\sqlite.db"



user = Users(db)
expenses = Expenses(db)
user.create_user(first_name="Анатолий", last_name="Броварник", username="Neverhood", email="anatoliy@brovarnik.kz", password = 123)


class UI():

    def __init__(self) -> None:
        pass

    def header(self):
        text = '''
            [1]: Record Expenses
            [2]: Record Incomes
            [3]: History of Expenses
            [4]: Export report to *.csv
            [5]: Exit
            '''
        return input(text)
    
    def main(self):
        self.header()


if __name__ == "__main__":
    ui = UI()
    ui.main()