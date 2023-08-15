# Import libraries
from flask import Flask, request, render_template, redirect, url_for
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation


@app.route('/', methods=["GET"])
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation


@app.route('/add', methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']

        if not date or not amount:
            return {"message": "Incorrect data"}, 422

        transactions.append({
            'id': len(transactions)+1,
            'date': date,
            'amount': amount
        })

        return redirect(url_for('get_transactions'))
    return render_template('form.html')

# Update operation


@app.route('/edit/<int:transaction_id>', methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transaction = next(
        (t for t in transactions if t['id'] == transaction_id), None)
    if not transaction:
        return {"message": "No transaction found with this id"}, 404

    if request.method == 'POST':
        for t in transactions:
            if t['id'] == transaction_id:
                t['date'] = request.form['date']
                t['amount'] = request.form['amount']

        return redirect(url_for('get_transactions'))

    return render_template('edit.html', transaction=transaction)


# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    transaction = next(
        (t for t in transactions if t['id'] == transaction_id), None)
    if not transaction:
        return {"message": "No transaction was found with this id"}, 404

    transactions.remove(transaction)
    return redirect(url_for('get_transactions'))


@app.route('/search', methods=["GET", "POST"])
def search_transactions():
    if request.method == 'POST':
        max_val = float(request.form['max_amount'])
        min_val = float(request.form['min_amount'])
        filtered_transactions = []
        for t in transactions:
            if t['amount'] <= max_val and t['amount'] >= min_val:
                filtered_transactions.append(t)
        if len(filtered_transactions) == 0:
            return {'message': "No transactions were found"}, 404
        return render_template('transactions.html', transactions=filtered_transactions)
    return render_template('search.html')


@app.route('/balance')
def total_balance():
    total = 0
    for t in transactions:
        total = total + t['amount']

    return render_template('transactions.html', transactions=transactions, total_balance=total)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=9000)
