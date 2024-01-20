import csv
from datetime import datetime

class CSV():

    def __init__(self) -> None:
        pass

    def report(self, rows):
        with open(f"{datetime.now().strftime("%d_%m_%Y")}_report_expenses.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Date", "Type", "Amount", "Amount in USD", "Amount in GBP", "Category", "Description"])
            if len(rows) > 0:
                for row in rows:
                    amount, description, category, type, date, amount_usd, amount_gbp = row
                    writer.writerow([date.split(" ")[0], type, amount, amount_usd, amount_gbp, category, description])
                input(f"The report {datetime.now().strftime("%d_%m_%Y")}_report_expenses.csv is ready. Press Enter...")
            else:
                input("There is no data in db for report. Press Enter...")