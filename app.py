import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Get all the data from the API
url = 'http://api.nessieisreal.com/enterprise/accounts?key=e1cac451319e9263333280ff4a5b28f6'
response = requests.get(url)
data = response.json()['results']  # Access the 'results' key in the JSON response

# Define home page route
@app.route('/')
def index():
    return render_template('login.html', account_found=False)

# Define logout route to handle logout action
@app.route('/logout')
def logout():
    return redirect('/')

# Define login route to handle form submission (using the ID because there is no password)
@app.route('/login', methods=['POST'])
def login():
    # Initialize the account_found variable to False
    account_found = False
    nickname = ''
    balance = 0
    # Get the account ID from the form
    id = request.form["id"]
    # Loop through the data to find the account with the ID
    for account in data:
        if account["_id"] == id:
            account_found = True
            nickname = account["nickname"]
            balance = account["balance"]
            break
    # If account is found, render the index.html template with the account details
    if account_found:
        return render_template('index.html', nickname=nickname, balance=balance, account_found=True)
    else:
        return render_template('login.html', account_found=False)

if __name__ == "__main__":
    app.run()
