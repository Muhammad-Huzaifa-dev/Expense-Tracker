# Expense Tracker

A personal finance management application with both CLI and web interfaces. Track income, expenses, and monitor your spending patterns in real-time.

## Features

### Core Features
- **Add Transactions**: Record income (salary, profit) and expenses with date/time
- **View Transactions**: Display all transactions with unique IDs for easy reference
- **Edit Transactions**: Modify any transaction field without re-entering everything
- **Remove Transactions**: Delete unwanted transactions
- **Summary Dashboard**: View total income, total expenses, net balance, and average transaction size
- **Persistent Storage**: All data saved to CSV and automatically loaded on startup

### Versions
- **CLI Version**: Terminal-based interface with menu-driven navigation
- **Flask Web App** (in progress): Single-page web interface with dynamic updates

## Project Structure
expense-tracker/
├── main.py              # CLI application entry point
├── transaction.py       # Transaction class (data model)
├── ledger.py           # Ledger class (business logic)
├── transactions.csv    # Data persistence
└── README.md

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### CLI Version

1. Clone the repository:
```bash
git clone https://github.com/Muhammad-Huzaifa-dev/Expense-Tracker.git
cd expense-tracker
```

2. Run the application:
```bash
python main.py
```

### Usage

1. **Add Transaction**: Enter type (salary/expense/profit), name, price, date, and time
2. **View Transactions**: Display all recorded transactions with IDs
3. **Edit Transaction**: Select a transaction by ID and modify any field
4. **Remove Transaction**: Delete a transaction by selecting its ID
5. **View Summary**: See income breakdown, total expenses, and net balance
6. **Exit**: Save all changes and close the application

### Date/Time Input Format
- **Date**: `YYYY-MM-DD` format (e.g., `2026-05-18`) or type `today`
- **Time**: `HH:MM` 24-hour format (e.g., `14:30`)

## Technical Details

### Architecture
- **Transaction Class**: Immutable data model with auto-incrementing IDs
- **Ledger Class**: Manages transaction collection, persistence, and calculations
- **Separation of Concerns**: Business logic independent from UI layer

### Data Persistence
- CSV-based storage with header row
- Transaction IDs persist across sessions
- Automatic loading on startup

## Future Enhancements

- [ ] Flask web interface with dynamic updates (AJAX)
- [ ] Category-based spending breakdown
- [ ] Monthly/yearly analytics
- [ ] Budget tracking and alerts
- [ ] Data export (PDF, Excel)
- [ ] SQLite database migration

## Technologies Used

- Python 3.11+
- CSV for data persistence
- Datetime for transaction timestamps
- Flask (upcoming)

## License

This project is open source and available under the MIT License.

## Author

Muhammad Huzaifa

---

*This project is part of a portfolio demonstrating Python fundamentals, OOP design, and full-stack web development.*