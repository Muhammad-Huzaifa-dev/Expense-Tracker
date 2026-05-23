import csv
from operator import index
import os
import datetime

class Transaction:
    # 1. This is a Class Variable. It belongs to the class itself, not individual objects.
    _id_counter = 1

    # 2. We add 'trans_id=None' to the parameters. 
    # If it's None, we know it's a new transaction.
    def __init__(self, name, price, date, time, income_type, trans_id=None):
        
        if trans_id is None:
            # It's a new transaction! Assign the current counter value, then increment it.
            self.id = Transaction._id_counter
            Transaction._id_counter += 1
        else:
            # It's an existing transaction being loaded from the CSV.
            self.id = int(trans_id)
            
            # Make sure our counter stays ahead of the loaded IDs to prevent duplicates
            if self.id >= Transaction._id_counter:
                Transaction._id_counter = self.id + 1

        self.name = name
        self.price = price
        self.date = date
        self.time = time
        self.income_type = income_type

    def __str__(self):
        # Update the string representation to include the ID
        return f"[{self.id}] {self.name} | {self.price} | {self.date} | {self.time} | {self.income_type}"

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

        print("\n=== SUMMARY ===")
        print("\nIncome:")
        print(f"  Total Salary: {total_salary:,.2f} pkr")
        print(f"  Total Profit: {total_profit:,.2f} pkr")
        print(f"  Total Income: {total_income:,.2f} pkr")
        
        print("\nExpenses:")
        print(f"  Total Expenses: {total_expense:,.2f} pkr")
        
        print(f"\nNet Balance: {net_balance:,.2f} pkr")
        print(f"Average Transaction: {avg_transaction:.2f} pkr")

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

def add_transaction_menu(ledger):
    """Get user input for a new transaction."""
    
    # Get transaction type (required)
    while True:
        income_type = input("Enter transaction type (salary/expense/profit): ").lower()
        if income_type in ['salary', 'expense', 'profit']:
            break
        else:
            print("Invalid type. Please enter salary, expense, or profit.")
    
    # Get name (required, non-empty)
    while True:
        name = input("Enter transaction name: ").strip()
        if name:
            break
        else:
            print("Transaction name cannot be empty.")
    
    # Get price (required, valid float)
    while True:
        try:
            price = float(input("Enter transaction price: "))
            break
        except ValueError:
            print("Invalid price. Please enter a number.")
    date = ledger.get_valid_date()
    time = ledger.get_valid_time()

    ledger.add(name, price, date, time, income_type)
    print("Transaction added successfully!")

def view_transactions_menu(ledger):
        """Display all transactions."""
        if not ledger.transactions:
            print("No transactions found.")
            return
        
        print("\nTransactions:")
        for idx, transaction in enumerate(ledger.transactions, start=1):
            print(f"{idx}. {transaction}")

def select_transaction(ledger):
    """Display transactions and let user pick one. Returns the index, or None to cancel."""
    if not ledger.transactions:
        print("No transactions found.")
        return None
    
    view_transactions_menu(ledger)
    
    while True:
        choice = input("\nEnter transaction number to select (or 'cancel' to go back): ").lower()
        
        if choice == 'cancel':
            print("Cancelled.")
            return None
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(ledger.transactions):
                return choice_num - 1
            else:
                print(f"Please enter a number between 1 and {len(ledger.transactions)}")
        except ValueError:
            print("Please enter a valid number or 'cancel'.")

def remove_transaction_menu(ledger):
    index = select_transaction(ledger)
    if index is not None:
        ledger.remove(index)
        print("Transaction removed successfully!")

def edit_transaction_menu(ledger):
    index = select_transaction(ledger)
    if index is not None:
        print("Editing transaction:")
        print(ledger.transactions[index])
        
        name = input("Enter new transaction name (leave blank to keep current): ")
        price_input = input("Enter new transaction price (leave blank to keep current): ")
        date_input = input("Enter new transaction date (YYYY-MM-DD, leave blank to keep current): ")
        time_input = input("Enter new transaction time (HH:MM, leave blank to keep current): ")
        income_type = input("Enter new transaction type (salary/expense/profit, leave blank to keep current): ").lower()
        
        # Validate inputs
        price = float(price_input) if price_input else None
        date = Ledger.get_valid_date(date_input) if date_input else None
        time = Ledger.get_valid_time(time_input) if time_input else None
        
        # Apply edit
        ledger.edit(index, name=name if name else None, price=price, date=date, time=time, income_type=income_type if income_type else None)
        print("Transaction updated successfully!")



def main():
    ledger = Ledger()
    
    while True:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Remove transaction")
        print("4. Edit transaction")
        print("5. View summary")
        print("6. Exit")
        
        choice = input("Pick an option (1-6): ")
        
        if choice == '1':
            # Add transaction logic here
            print('Selected "Add transaction"')
            add_transaction_menu(ledger)
            ledger.save_to_csv()
        elif choice == '2':
            # View transactions logic here
            print('Selected "View transactions"')
            view_transactions_menu(ledger)
        elif choice == '3':
            # View transactions logic here
            print('Selected "Remove transaction"')
            remove_transaction_menu(ledger)
            ledger.save_to_csv()
        elif choice == '4':
            # View transactions logic here
            print('Selected "Edit transaction"')
            edit_transaction_menu(ledger)
            ledger.save_to_csv()
        elif choice == '5':
            # View summary logic here
            print('Selected "View summary"')
            ledger.summary()
        elif choice == '6':
            ledger.save_to_csv()
            print("Data saved. Goodbye!")
            break

if __name__ == '__main__':
    main()