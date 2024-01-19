from app.Models.UserModel import Users
from app.Models.Expenses import Expenses
from app.Services.ExchangeApi import CurrencyExchangeApi
from datetime import datetime
from getpass import getpass

db = r"app\Database\sqlite.db"

class UI():

    def __init__(self) -> None:
        self.session = {"uid": None, "auth": False}
        self.user = Users(db)
        self.expenses = Expenses(db)
    
    # Authentication of user
    def user_auth(self):
        self.prompt("First run of application. Please enter Username & Password. If you don't have account the program propose you to add additional info to register. Press Enter...")
        self.username = self.prompt("Please enter Username: ")
        self.password = getpass()
        credentials = self.user.get_user_by_credentials(self.username, self.password)
        if credentials is None:
            uid = self.user_reg()
            if uid > 0:
                self.session["uid"] = uid
                self.session["auth"] = True
        else:
            self.session["uid"] = credentials
            self.session["auth"] = True

        return self.session

    # Registration of user
    def user_reg(self):
        self.prompt("You are newbie in the app. Please enter additional information to proceed further. Press Enter...")
        firstname = self.prompt("Please enter First Name: ")
        lastname = self.prompt("Please enter Last Name: ")
        email = self.prompt("Please enter Email: ")
        
        result = self.user.create_user( 
                                        username = self.username, 
                                        password = self.password, 
                                        first_name = firstname, 
                                        last_name = lastname, 
                                        email = email
                                        )
        
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
            [5]: Exit'''
        return print(text)
    
    def prompt(self, text):
        return input(text)

    # Main methods
    # Record expenses
    def record_expenses(self):
        amount = float(self.prompt("Enter Amount: "))
        description = self.prompt("Enter Description: ")
        category = self.prompt("Enter Category: ")
        type = self.prompt("Enter Type: ")

        #Get data from exchange using API
        api = CurrencyExchangeApi()
        usd_rate = api.get_exhange_rate("USD", "KZT")
        gbp_rate = api.get_exhange_rate("GBP", "KZT")
        save_expenses = self.expenses.record_expenses(
                                            amount = amount, 
                                            description = description, 
                                            category = category,
                                            type = type,
                                            user_id = self.session["uid"], 
                                            date = datetime.now(), 
                                            amount_usd = round(amount / usd_rate, 2), 
                                            amount_gbp = round(amount / gbp_rate, 2)
                                            )
        if save_expenses:
            self.prompt("The data has been recorded. Press Enter...")
        else:
            self.prompt("Error is occured. The data has not been recorded. Please try again...")
    
    # Record incomes 
    def record_incomes(self):
        return True
    
    # Print history of expenses
    def history_of_expenses(self):
        return True
    
    # Export report to csv file
    def export_csv(self):
        return True

    def app_exit(self):
        return True

    def main(self):
        if self.session["auth"]:
            self.header()
            try:
                option = int(self.prompt("Press number [1-5] to choose option: "))
                match option:
                    case 1:
                        return self.record_expenses()
                    case 2:
                        return self.record_incomes()
                    case 3:
                        return self.history_of_expenses()
                    case 4:
                        return self.export_csv()
                    case 5:
                        return self.app_exit()
                    case _:
                        return True
            except Exception as e:
                self.prompt(f"Error: {e} \nYour input is wrong. Please try again.")

        else:
            if self.user_auth():
                self.main()
            else:
                self.prompt("The problem is occured during the registration proccess. Please connect to admin to resolve it (anatoliy@brovarnik.kz)")

if __name__ == "__main__":
    ui = UI()
    while True:
        if ui.main() is False:
            break