from app.Models.UserModel import Users
from app.Models.Expenses import Expenses
from app.Services.ExchangeApi import CurrencyExchangeApi
import sys

db = r"app\Database\sqlite.db"


# 
# user.create_user(first_name="Анатолий", last_name="Броварник", username="Neverhood", email="anatoliy@brovarnik.kz", password = 123)


class UI():

    def __init__(self) -> None:
        self.user = Users(db)
        self.expenses = Expenses(db)

    def user_auth(self):
        self.username = self.prompt("Please enter Username: ")
        self.password = self.prompt("Please enter Password: ")

        if self.user.get_user_by_credentials(self.username, self.password) is not None:
            if self.user_reg():
                return True
            else:
                return input("The problem is occured during the registration proccess. Please connect to admin to resolve it (anatoliy@brovarnik.kz)")
        else:
            return True

    def user_reg(self):
        self.prompt("You are newbie in the app. Please enter additional information to proceed further. Press Enter...")
        firstname = self.prompt("Please enter First Name: ")
        lastname = self.prompt("Please enter Last Name: ")
        email = self.prompt("Please enter Email: ")
        
        result = self.user.create_user(self.username, self.password, firstname, lastname, email)
        
        if result:
            return True
        else:
            return False
        
    def header(self):
        text = '''
            [1]: Record Expenses
            [2]: Record Incomes
            [3]: History of Expenses
            [4]: Export report to *.csv
            [5]: Exit
            '''
        return print(text)
    
    def prompt(self, text):
        return input(text)

    # Main methods
    # Record expenses
    def record_expenses(self):
        pass
    
    # Record incomes 
    def record_incomes(self):
        pass
    
    # Print history of expenses
    def history_of_expenses(self):
        pass
    
    # Export report to csv file
    def export_csv(self):
        pass

    def app_exit(self):
        sys.exit(0)

    def main(self):
        if self.user_auth():
            self.header()
            try:
                option = int(self.prompt("Press number [1-5] to choose option: "))
                match option:
                    case 1:
                        self.record_expenses()
                    case 2:
                        self.record_incomes()
                    case 3:
                        self.history_of_expenses()
                    case 4:
                        self.export_csv()
                    case 5:
                        self.app_exit()
                    case _:
                        self.main()
            except:
                self.prompt("Your input is wrong. Please try again.")
                self.main()
        else:


if __name__ == "__main__":
    ui = UI()
    ui.main()