from ledger import Ledger

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

def summary_menu(ledger):
    summary = ledger.summary()
    print("=== SUMMARY ===")
    print(f"\nIncome:")
    print(f"  Total Salary: {summary['total_salary']} pkr")
    print(f"  Total Profit: {summary['total_profit']} pkr")
    print(f"  Total Income: {summary['total_income']} pkr")
    print(f"\nExpenses:")
    print(f"  Total Expenses: {summary['total_expense']} pkr")
    print(f"\nNet Balance: {summary['net_balance']} pkr")
    print(f"Average Transaction: {summary['avg_transaction']} pkr")

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
            summary_menu(ledger)
        elif choice == '6':
            ledger.save_to_csv()
            print("Data saved. Goodbye!")
            break

if __name__ == '__main__':
    main()