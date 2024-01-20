from app.Models.UserModel import Users
from app.Models.Expenses import Expenses
from app.Services.ExchangeApi import CurrencyExchangeApi
from datetime import datetime
from getpass import getpass
from hashlib import md5
import re
import os
import csv

db = r"app\Database\sqlite.db"

class UI():

    def __init__(self) -> None:
        self.session = 0
        self.user = Users(db)
        self.expenses = Expenses(db)
    
    # Authentication of user
    def user_auth(self):
        print("Please enter Username & Password. If you don't have account the program propose you to add additional info to register.")
        self.username = input("Username: ")
        self.password = getpass()
        # Get password from db by username
        password_from_db = self.user.get_pass_by_username(self.username)
        # If there's no such user in db, try to register him
        if password_from_db is None:
            uid = self.user_reg()
            if uid > 0:
                self.session = uid
        else:
            # if there is the user in db, check password. If password incorrect suggest to try again
            if password_from_db[1] == md5(self.password.encode()).hexdigest():
                self.session = password_from_db[0]
            else:
                self.session = -1
        return self.session

    # Registration of user
    def user_reg(self):
        input("You are newbie in the app. Please enter additional information to proceed further. Press Enter...")
        firstname = input("First Name: ")
        lastname = input("Last Name: ")
        email = input("Email: ")
        
        result = self.user.create_user( 
                                        username = self.username, 
                                        password = md5(self.password.encode()).hexdigest(), 
                                        first_name = firstname, 
                                        last_name = lastname, 
                                        email = email
                                        )
        return result
    
    # Clean screen of terminal
    def clean(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    # Header of Menu
    def header(self):
        text =  "[1]: Record Expenses\n" + \
                "[2]: Record Incomes\n" + \
                "[3]: History of Expenses\n" + \
                "[4]: Export report to *.csv\n" + \
                "[5]: Exit"
        return print(text)

    # Main methods
    # Record expenses or income
    def record(self, type):
        amount = float(input("Amount: "))
        description = input("Description: ")
        category = input("Category: ")

        #Get data from exchange using API
        api = CurrencyExchangeApi()
        usd_rate = api.get_exhange_rate("USD", "KZT")
        gbp_rate = api.get_exhange_rate("GBP", "KZT")
        save_expenses = self.expenses.record(
                                            amount = amount, 
                                            description = description, 
                                            category = category,
                                            type = "expenses" if type == "expenses" else "income",
                                            user_id = self.session, 
                                            date = datetime.now(), 
                                            amount_usd = round(amount / usd_rate, 2), 
                                            amount_gbp = round(amount / gbp_rate, 2)
                                            )
        if save_expenses:
            input("The data has been recorded. Press Enter...")
        else:
            input("Error is occured. The data has not been recorded. Please try again...")
    
    # Print history or create report of expenses
    def history(self, format):
        
        #Validate dates
        flag_start = True
        while flag_start:
            start_date = input("Enter Start Date: ")
            if not re.match(r"[\d]{2}.[\d]{2}.[\d]{4}", start_date):
                print ("Template for dates is [dd.mm.yyyy]")
            else:
                flag_start = False
        
        flag_end = True
        while flag_end:        
            end_date = input("Enter End Date: ")
            if not re.match(r"[\d]{2}.[\d]{2}.[\d]{4}", end_date):
                print("Template for dates is [dd.mm.yyyy]")
            else:
                flag_end = False
        # Format dates for db
        start_date = datetime.strptime(start_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        result = self.expenses.history(start_date, end_date)
        
        # show history
        if format == "history":
            if len(result) > 0:
                for row in result:
                    amount, description, category, type, date, amount_usd, amount_gbp = row
                    print(f"[{date.split(" ")[0]}] Type: {type}; Amount: {amount} ₸/[${amount_usd}/£{amount_gbp}]; Category: {category}; Description: {description};")
                input("Press Enter...")
            else:
                    input("There is no data in db for showing. Press Enter...")
        
        # create report
        elif format == "report":
            with open(f"{datetime.now().strftime("%d_%m_%Y")}_report_expenses.csv", "w", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Date", "Type", "Amount", "Amount in USD", "Amount in GBP", "Category", "Description"])
                if len(result) > 0:
                    for row in self.expenses.history(start_date, end_date):
                        amount, description, category, type, date, amount_usd, amount_gbp = row
                        writer.writerow([date.split(" ")[0], type, amount, amount_usd, amount_gbp, category, description])
                    input(f"The report {datetime.now().strftime("%d_%m_%Y")}_report_expenses.csv is ready. Press Enter...")
                else:
                    input("There is no data in db for report. Press Enter...")
        return True
    
    # Exit app
    def app_exit(self):
        exit()

    # Main method
    def main(self):
        if self.session > 0:
            self.clean()
            self.header()
            try:
                option = int(input("Press number [1-5] to choose option: "))
                match option:
                    case 1:
                        return self.record("expenses")
                    case 2:
                        return self.record("income")
                    case 3:
                        return self.history("history")
                    case 4:
                        return self.history("report")
                    case 5:
                        return self.app_exit()
            except Exception as e:
                input(f"Error: {e} \nYour input is wrong. Please try again.")

        else:
            if self.session == 0:
                self.user_auth()
                self.main()
            elif self.session == -1:
                self.session = 0
                input("Your password is not correct. Please try again.")
            else:
                self.session = 0
                input("The problem is occured during the registration proccess.")

if __name__ == "__main__":
    ui = UI()
    while True:
        if ui.main() is False:
            break
