# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
def total_balance():
    return sum(transaction['amount'] for transaction in transactions)


# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions, saldo=total_balance())

# Create operation
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        new_transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(new_transaction)
        return redirect(url_for('get_transactions'))
    return render_template('form.html')


# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = request.form['date']
                transaction['amount'] = float(request.form['amount'])
                return redirect(url_for('get_transactions'))
    else:
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template('edit.html', transaction=transaction)

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t['id'] != transaction_id]
    return redirect(url_for('get_transactions'))

#funcion de busqueda entre valores

@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = [t for t in transactions if min_amount <= t['amount'] <= max_amount]
        return render_template('transactions.html', transactions=filtered_transactions)
    else:
        return render_template('search.html')
#funcion de saldo total
@app.route('/balance')
def total_balance():
    total = sum(transaction['amount'] for transaction in transactions)
    return f"Saldo Total: {total}"


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    