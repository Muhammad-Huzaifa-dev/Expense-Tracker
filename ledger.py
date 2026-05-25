import csv
import os
import datetime
from transaction import Transaction

class Ledger:
    
    def __init__(self):
        self.transactions = []
        self.fetch_from_csv()

    def add(self, name, price, date, time, income_type):
        t = Transaction(name, price, date, time, income_type)
        self.transactions.append(t)
    
    def save_to_csv(self):
        with open('transactions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Price', 'Date', 'Time', 'Income Type'])
            for t in self.transactions:
                writer.writerow([t.id, t.name, t.price, t.date, t.time, t.income_type])

    def fetch_from_csv(self):
        if os.path.exists('transactions.csv'):
            with open('transactions.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader, None) 
                for row in reader:
                    if row:
                            self.transactions.append(Transaction(
                                name=row[1], 
                                price=float(row[2]), 
                                date=datetime.date.fromisoformat(row[3]), 
                                time=datetime.time.fromisoformat(row[4]), 
                                income_type=row[5],
                                trans_id=row[0]
    ))

    def summary(self):
        total_salary = sum(t.price for t in self.transactions if t.income_type == 'salary')
        total_expense = sum(t.price for t in self.transactions if t.income_type == 'expense')
        total_profit = sum(t.price for t in self.transactions if t.income_type == 'profit')
        total_income = total_salary + total_profit
        net_balance = total_income - total_expense
        avg_transaction = sum(t.price for t in self.transactions) / len(self.transactions) if self.transactions else 0

        return {
            'total_salary': total_salary,
            'total_profit': total_profit,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'avg_transaction': round(avg_transaction, 2)
        }

    def edit(self, index, name=None, price=None, date=None, time=None, income_type=None):
        """Edit a transaction. Pass None for fields you don't want to change."""
        t = self.transactions[index]
        if name is not None:
            t.name = name
        if price is not None:
            t.price = price
        if date is not None:
            t.date = date
        if time is not None:
            t.time = time
        if income_type is not None:
            t.income_type = income_type
    
    def remove(self, index):
        """Remove a transaction by index."""
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
        else:
            print(f"Invalid index: {index}")

    @staticmethod
    def get_valid_date(date_str=None):
        date_format = "%Y-%m-%d"
    
        while True:
            if date_str is None:
                date_str = input("Enter date (YYYY-MM-DD): ")

            if date_str == 'today':
                return datetime.date.today()
            try:
                valid_date = datetime.datetime.strptime(date_str, date_format).date()
                return valid_date
            except ValueError:
                print("Invalid format. Please use YYYY-MM-DD (e.g., 2026-05-18).")
                date_str = None 

    @staticmethod
    def get_valid_time(time_str=None):
        time_format = "%H:%M"
        
        while True:
            if time_str is None:
                time_str = input("Enter time (HH:MM): ")
            
            try:
                valid_time = datetime.datetime.strptime(time_str, time_format).time()
                return valid_time
            except ValueError:
                print("Invalid format. Please use HH:MM (e.g., 01:30).")
                time_str = None
