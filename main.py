from app.Models.UserModel import Users
from app.Models.Expenses import Expenses
from app.Services.ExchangeApi import CurrencyExchangeApi

db = "app\Database\sqlite.db"

user = Users(db)
expenses = Expenses(db)