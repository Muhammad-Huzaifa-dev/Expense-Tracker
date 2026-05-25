from flask import Flask, jsonify, request, render_template
from ledger import Ledger
from transaction import Transaction
import json

app = Flask(__name__)

# Create one Ledger instance that persists while the server runs
ledger = Ledger()

@app.route('/')
def index():
    return render_template('index.html')

def transaction_to_dict(transaction):
    """Convert a Transaction object to a dictionary for JSON."""
    return {
        'id': transaction.id,
        'name': transaction.name,
        'price': transaction.price,
        'date': transaction.date.isoformat(),
        'time': transaction.time.isoformat(),
        'income_type': transaction.income_type
    }

@app.route('/api/data', methods=['GET'])
def get_data():
    """Return all transactions and summary."""
    transactions = [transaction_to_dict(t) for t in ledger.transactions]
    summary = ledger.summary()
    
    return jsonify({
        'transactions': transactions,
        'summary': summary
    })

@app.route('/api/add', methods=['POST'])
def add_transaction():
    """Add a new transaction."""
    data = request.json
    
    try:
        # Validate income_type
        if data.get('income_type') not in ['salary', 'expense', 'profit']:
            return jsonify({'error': 'Invalid income type'}), 400
        
        # Get and validate date
        date = Ledger.get_valid_date(data.get('date'))
        if date is None:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # Get and validate time
        time = Ledger.get_valid_time(data.get('time'))
        if time is None:
            return jsonify({'error': 'Invalid time format'}), 400
        
        # Add to ledger
        ledger.add(
            name=data.get('name'),
            price=float(data.get('price')),
            date=date,
            time=time,
            income_type=data.get('income_type')
        )
        
        # Save to CSV
        ledger.save_to_csv()
        
        # Return updated data
        transactions = [transaction_to_dict(t) for t in ledger.transactions]
        summary = ledger.summary()
        
        return jsonify({
            'transactions': transactions,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    """Delete a transaction by ID."""
    try:
        # Find the transaction with this ID
        index = None
        for i, t in enumerate(ledger.transactions):
            if t.id == id:
                index = i
                break
        
        if index is None:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Remove it
        ledger.remove(index)
        ledger.save_to_csv()
        
        # Return updated data
        transactions = [transaction_to_dict(t) for t in ledger.transactions]
        summary = ledger.summary()
        
        return jsonify({
            'transactions': transactions,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/edit/<int:id>', methods=['POST'])
def edit_transaction(id):
    """Edit a transaction by ID."""
    data = request.json
    
    try:
        # Find the transaction
        index = None
        for i, t in enumerate(ledger.transactions):
            if t.id == id:
                index = i
                break
        
        if index is None:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Validate and parse inputs (only if provided)
        date = Ledger.get_valid_date(data.get('date')) if data.get('date') else None
        time = Ledger.get_valid_time(data.get('time')) if data.get('time') else None
        income_type = data.get('income_type')
        
        if income_type and income_type not in ['salary', 'expense', 'profit']:
            return jsonify({'error': 'Invalid income type'}), 400
        
        # Edit using your Ledger.edit() method
        ledger.edit(
            index,
            name=data.get('name'),
            price=float(data.get('price')) if data.get('price') else None,
            date=date,
            time=time,
            income_type=income_type
        )
        
        ledger.save_to_csv()
        
        # Return updated data
        transactions = [transaction_to_dict(t) for t in ledger.transactions]
        summary = ledger.summary()
        
        return jsonify({
            'transactions': transactions,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)