import os
import openai
import requests
from flask import Flask, render_template, request, redirect, url_for, session
import json


app = Flask(__name__)
app.secret_key = os.urandom(24)
openai.api_key = os.environ.get("OPENAI_API_KEY")
MAX_RESPONSE_LENGTH = 500  # Define the maximum length of the response to display

# Get all the data from the API
url = 'http://api.nessieisreal.com/enterprise/accounts?key=e1cac451319e9263333280ff4a5b28f6'
response = requests.get(url)
initilizingjsondata = response.json()['results']  # Access the 'results' key in the JSON response

# Open the accounts.json file
with open('accounts.json') as json_file:
    # Load the JSON data from the file
    data = json.load(json_file)

# Access the 'results' key in the JSON data
data = data['results']

# Define home page route
@app.route('/')
def home():
    return render_template('login.html', account_found=False)


# Define logout route to handle logout action
@app.route('/logout')
def logout():
    session.pop("id", None)  # Remove the 'id' from the session
    return redirect('/')


# Define login route to handle form submission (using the ID because there is no password)
@app.route('/login', methods=['POST'])
def login():
    # Initialize the account_found variable to False
    account_found = False
    nickname = ''
    balance = 0
    creditscore = ''
    loans = ''
    debt = ''
    bills = ''

    # Get the account ID from the form
    id = request.form["id"]
    # Loop through the data to find the account with the ID
    for account in data:
        if account["_id"] == id:
            account_found = True
            old_nickname = account["nickname"]
            nickname = old_nickname.replace("'s Account", "")

            oldbalance = account["balance"]
            balance = "{:.2f}".format(oldbalance)

            creditscore = account["Creditscore"]

            loans = account["Loans"]
            debt = account["Debt"]
            bills = account["Bills"]

            break
    # If account is found, store the ID in the session and render the index.html template with the account details
    if account_found:
        session["id"] = id  # Store the ID in the session
        return render_template('index.html', nickname=nickname, balance=balance, creditscore=creditscore,loans=loans,debt=debt,bills=bills, account_found=True)
    else: 
        return render_template('login.html', account_found=False)

@app.route("/openaifunc", methods=["GET", "POST"])
def openaifunc():
    nickname = ''
    balance = 0

    if request.method == "POST":
        human = request.form["human"]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=generate_prompt(human, nickname, balance),
            temperature=0.6,
            max_tokens=MAX_RESPONSE_LENGTH,
        )
        result = truncate_text(response.choices[0].text)

        # Retrieve the ID from the session
        id = session.get("id")
        if id:
            for account in data:
                if account["_id"] == id:
                    old_nickname = account["nickname"]
                    nickname = old_nickname.replace("'s Account", "")

                    oldbalance = account["balance"]
                    balance = "{:.2f}".format(oldbalance)
                    creditscore = account["Creditscore"]

                    loans = account["Loans"]
                    debt = account["Debt"]
                    bills = account["Bills"]


                    break
        return render_template('index.html', nickname=nickname, balance=balance, creditscore=creditscore,loans=loans,debt=debt,bills=bills, account_found=True, result=result)

    # Retrieve the ID from the session
    id = session.get("id")
    if id:
        for account in data:
            if account["_id"] == id:
                old_nickname = account["nickname"]
                nickname = old_nickname.replace("'s Account", "")

                oldbalance = account["balance"]
                balance = "{:.2f}".format(oldbalance)
                loans = account["Loans"]
                debt = account["Debt"]
                bills = account["Bills"]


                break

    result = request.args.get("result")
    return render_template('index.html', nickname=nickname, balance=balance, creditscore=creditscore,loans=loans,debt=debt,bills=bills, account_found=True, result=result)


def generate_prompt(human, nickname, balance):
    nickname = ''
    balance = 0

        # Retrieve the ID from the session
    id = session.get("id")
    if id:
        for account in data:
            if account["_id"] == id:
                old_nickname = account["nickname"]
                nickname = old_nickname.replace("'s Account", "")

                oldbalance = account["balance"]
                balance = "{:.2f}".format(oldbalance)
                break


    return f"""Suggest financial advice for {nickname} with a balance of {balance}. Provide detailed recommendations based on different financial situations, including leveraging specific Capital One services.

    Human: What is my account balance
    Response: Dear {nickname}, your account balance is {balance} dollars.
    
    Human: I am struggling to manage my expenses.
    Response: If you're having difficulty managing expenses {nickname}, consider using Capital One's budgeting tools like the Capital One Mobile App to track your spending. Create a detailed budget that includes essential expenses and discretionary spending. Reach out to Capital One's customer support for personalized guidance.

    Human: I want to start saving for the future.
    Response: To begin saving for the future {nickname}, open a Capital One 360 Savings Account. Set specific savings goals and establish automatic transfers from your checking account. Capital One provides online tools to monitor your progress. Explore Capital One's investment options to grow your savings.

    Human: I am considering purchasing a home.
    Response: If you're planning to buy a home {nickname}, reach out to Capital One Home Loans for mortgage options and assistance. Use Capital One's mortgage calculator to estimate payments. Capital One's Home Loans team can guide you through the process, including pre-qualification, application, and closing.

    Human: I am interested in investing in the stock market.
    Response: If you're considering investing in the stock market {nickname}, Capital One Investing provides a platform for online trading and investment research. Open a Capital One Investing account to access a wide range of investment options. Utilize Capital One's research tools and educational resources. Consult with Capital One's investment advisors for personalized guidance.

    Human: I have 0 dollars in my bank account.
    Response: Focus on saving money diligently {nickname}. Consider opening a Capital One 360 Savings Account. Create a budget to track expenses and identify areas to cut back. Explore government assistance programs. Look for ways to reduce costs on essential items. Gradually build an emergency fund.

    Human: {human}
    Response:""".format(nickname=nickname)

def truncate_text(text):
    if len(text) > MAX_RESPONSE_LENGTH:
        return text[:MAX_RESPONSE_LENGTH] + "..."  # Truncate the text and add ellipsis
    return text


if __name__ == "__main__":
    app.run(debug=True)
