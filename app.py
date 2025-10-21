# Import libraries
from flask import Flask, request, render_template, url_for, redirect

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=['GET', 'POST'])
def add_transaction():
    #to see if request is post (form submission)
    if request.method == 'POST':
        #create new transac object using form field values
        transaction = {
            'id': len(transactions) + 1, #generate new id
            'date': request.form['date'], #get the 'date' field value from the form
            'amount': float(request.form['amount']) #get the amout
        }
        #append the new transaction to the transaction list
        transactions.append(transaction)
        #redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    #if the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    #check if the request is post (form submis)
    if request.method == 'POST':
        #Extract the update value from the form fields
        date = request.form['date']
        amount = float(request.form['amount']) #Get the 'amount' field value from the formand convert it to a float

        #find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date #update the 'date' field of the transaction
                transaction['amount'] = amount # update the 'amount' field of the transaction
                break    #exist the loop once the transaction is found and updated

        #redirect to the transaction list page after updating the transaction
        return redirect(url_for("get_transactions"))

    #if the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            #Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
            
    #if the transaction with the specified ID is not found, handle thiscase (optional)
    return {"message": "Transaction not found"}, 404



@app.route("/search", methods=['GET', 'POST'])
def search_transactions():
    #check if request is post
    if request.method == 'POST':
        #get min and max amount from the form and convert to float
        min_amount = float(request.form.get('min_amount', 0))
        max_amount = float(request.form.get('max_amount', 0))

        #Filter transactions based on the amount range
        filtered_transactions = [t for t in transactions if min_amount <= t['amount'] <= max_amount]

        #render the transactions template with filtered results
        return render_template('transactions.html', transactions=filtered_transactions)
    #for get request, render the search form
    return render_template('search.html')


@app.route('/balance')
def total_balance():
    # Calculate the sum of all transaction amounts
    balance = sum(t['amount'] for t in transactions)
    
    # Render the transactions template, passing transactions and the total balance
    return render_template('transactions.html', transactions=transactions, total_balance=balance)


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    #find a matching trans. ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction) #remove the transaction from the transactions list
            break # Exist the loop once the transaction is found and removed

    # redirect too the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))


# Run the Flask app
if __name__ == "__main__":
    app.run(debug = True)