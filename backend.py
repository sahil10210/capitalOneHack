import requests
import json
import pandas as pd
from flask import Flask, render_template, request, redirect, flash, session, url_for

app = Flask(__name__)

# Get all the data from the API
url = 'http://api.nessieisreal.com/enterprise/accounts?key=e1cac451319e9263333280ff4a5b28f6'
response = requests.get(url)
data = response.json()

# Define home page route
# When the URL is accessed, the index function will run,
# which will render the index.html template with the variable account_found=False
@app.route('/')
def index():
    return render_template('index.html', account_found=False)

# Define logout route to handle logout action
# When the URL is called with /logout, the logout function will be called
# which will lead the user to the base URL
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
    # request.form is a dictionary that contains the form data
    id = request.form['id']
    # Loop through the data to find the account with the ID
    for account in data:
        if account['id'] == id:
            account_found = True
            nickname = account['nickname']
            balance = account['balance']
            break
    # If account is found, render the account.html template with the account details
    if account_found:
        return render_template('login.html', nickname=nickname, balance=balance)
    else:
        return render_template('index.html', account_found=False)
