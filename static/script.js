// When the page loads, fetch and display all data
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    
    // Add event listener to the form
    document.getElementById('transactionForm').addEventListener('submit', handleAddTransaction);
});

// Fetch all data from the API and update the page
function loadData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            displayTransactions(data.transactions);
            updateSummary(data.summary);
        })
        .catch(error => console.error('Error loading data:', error));
}

// Display transactions in the list
function displayTransactions(transactions) {
    const listElement = document.getElementById('transactionsList');
    
    if (transactions.length === 0) {
        listElement.innerHTML = '<div class="empty-state"><p>No transactions yet. Add one to get started!</p></div>';
        return;
    }
    
    listElement.innerHTML = transactions.map(transaction => `
        <div class="transaction-item">
            <div class="transaction-info">
                <span class="type ${transaction.income_type}">${transaction.income_type.toUpperCase()}</span>
                <div class="name">${transaction.name}</div>
                <div class="details">${transaction.date} at ${transaction.time}</div>
            </div>
            <div class="transaction-price">${transaction.price} PKR</div>
            <div class="transaction-actions">
                <button class="btn-edit" onclick="editTransaction(${transaction.id})">✏️ Edit</button>
                <button class="btn-delete" onclick="deleteTransaction(${transaction.id})">🗑️ Delete</button>
            </div>
        </div>
    `).join('');
}

// Update the summary section
function updateSummary(summary) {
    document.getElementById('totalSalary').textContent = `${summary.total_salary} PKR`;
    document.getElementById('totalProfit').textContent = `${summary.total_profit} PKR`;
    document.getElementById('totalIncome').textContent = `${summary.total_income} PKR`;
    document.getElementById('totalExpenses').textContent = `${summary.total_expense} PKR`;
    document.getElementById('netBalance').textContent = `${summary.net_balance} PKR`;
    document.getElementById('avgTransaction').textContent = `${summary.avg_transaction} PKR`;
}

// Handle form submission (Add transaction)
function handleAddTransaction(event) {
    event.preventDefault();
    
    const formData = {
        type: document.getElementById('type').value,
        name: document.getElementById('name').value,
        price: document.getElementById('price').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        income_type: document.getElementById('type').value
    };
    
    let apiEndpoint = '/api/add';
    let method = 'POST';
    
    // If editing, change the endpoint
    if (editingId !== null) {
        apiEndpoint = `/api/edit/${editingId}`;
    }
    
    fetch(apiEndpoint, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Clear the form and reset edit mode
            document.getElementById('transactionForm').reset();
            editingId = null;
            document.querySelector('.btn-add').textContent = 'Add Transaction';
            document.querySelector('.btn-add').style.background = '#667eea';
            
            // Update the page
            displayTransactions(data.transactions);
            updateSummary(data.summary);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to process transaction');
    });
}

// Delete a transaction
function deleteTransaction(id) {
    if (confirm('Are you sure you want to delete this transaction?')) {
        fetch(`/api/delete/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                displayTransactions(data.transactions);
                updateSummary(data.summary);
            }
        })
        .catch(error => {
            console.error('Error deleting transaction:', error);
            alert('Failed to delete transaction');
        });
    }
}

// Edit a transaction
function editTransaction(id) {
    // For now, this is a placeholder
    alert('Edit functionality coming soon! Transaction ID: ' + id);
}

let editingId = null;  // Track which transaction we're editing (null = adding new)

// Edit a transaction
function editTransaction(id) {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const transaction = data.transactions.find(t => t.id === id);
            if (transaction) {
                document.getElementById('type').value = transaction.income_type;
                document.getElementById('name').value = transaction.name;
                document.getElementById('price').value = transaction.price;
                document.getElementById('date').value = transaction.date;
                
                // Fix: Remove seconds from time
                document.getElementById('time').value = transaction.time.substring(0, 5);  // Takes only HH:MM
                
                editingId = id;
                document.querySelector('.btn-add').textContent = 'Save Changes';
                document.querySelector('.btn-add').style.background = '#28a745';
                
                document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
            }
        });
}