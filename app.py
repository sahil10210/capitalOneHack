import os
import openai
import requests
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, redirect, url_for, session
import json
#define the route to atmporcessing.py
from atmproccessing import get_top_3_atms


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

# Open the adresses.json file
with open('adresses.json') as json_file:
    # Load the JSON data from the file
    mapdata = json.load(json_file)

mapdata = mapdata["data"]



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
            
            old_bills = account["Bills"]
            bills = old_bills.replace(".", ": ")



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
    creditscore = ''
    loans = ''
    debt = ''
    bills = ''

    if request.method == "POST":
        human = request.form["human"]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=generate_prompt(human, nickname, balance, creditscore, loans, debt, bills),
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

                creditscore = account["Creditscore"]
                loans = account["Loans"]
                debt = account["Debt"]
                bills = account["Bills"]


                break

    result = request.args.get("result")
    return render_template('index.html', nickname=nickname, balance=balance, creditscore=creditscore,loans=loans,debt=debt,bills=bills, account_found=True, result=result)



def generate_prompt(human, nickname, balance, creditscore, loans, debt, bills):
    nickname = ''
    balance = 0
    creditscore = ''
    loans = ''
    debt = ''
    bills = ''


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


    return f"""Suggest financial advice for {nickname} with a balance of {balance}, a credit score of {creditscore}, a loan amount of {loans}, a debt of {debt}, and bills of amount {bills}. Provide detailed recommendations based on different financial situations, including leveraging specific Capital One services. Do not dodge the question under any circumstances. If asked a question for a number amount, always give a number amount, even if unsure.

    Human: What is my account balance
    Response: Dear {nickname}, your account balance is {balance} dollars.

    Human: What is my credit score
    Response: Dear {nickname}, your credit score is {creditscore}.

    Human: Can I afford to buy a house
    Response: Dear {nickname}, you can afford to buy a house if you have a credit score of at least 620, a down payment of at least 3%, and a debt-to-income ratio of 36% or less. Since your credit score is {creditscore}, you can afford to buy a house.

    Human: How much debt do I have
    Response: {nickname}, your debt is {debt}!

    Human: What is my loan amount
    Response: {nickname}, your loan is {loans}.

    Human: What is my bill amount
    Response: Dear {nickname}, your bill is {bills}.

    Human: How could I improve my credit score
    Response: To improve your credit score {nickname}, pay your bills on time, keep your credit card balances low, and limit the number of credit accounts you have.
    
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


#define a /maps route that will take us to map.html from login.html template with the variables of adress, atm 1, atm 2, amt 3. It will ask for the address  and radius and then use the address to find the nearest 3 atms.
@app.route('/map', methods=["GET", "POST"])
def map():
    # Initialize the maps_found variable to False
    address = ''
    radius = 0
    atm1 = ''
    long1 = 0
    lat1 = 0
    atm2 = ''  
    long2 = 0
    lat2 = 0
    atm3 = ''
    long3 = 0
    lat3 = 0

    # Get the address and radius from the form
    if request.method == "POST":
        address = request.form["add"]
        radius = request.form["radius"]

    result = get_top_3_atms(address, radius)

    atm1 = result[0]['address']
    long1 = result[0]['geocode']['lng']
    lat1 = result[0]['geocode']['lat']
    atm2 = result[1]['address']
    long2 = result[1]['geocode']['lng']
    lat2 = result[1]['geocode']['lat']
    atm3 = result[2]['address']
    long3 = result[2]['geocode']['lng']
    lat3 = result[2]['geocode']['lat']

    startaddress = address.replace(" ", "+")


    address1=atm1.replace(" ", "+")
    address2=atm2.replace(" ", "+")
    address3=atm3.replace(" ", "+")

    link1 = f"https://www.google.com/maps/dir/{startaddress}/{address1}"
    link2 = f"https://www.google.com/maps/dir/{startaddress}/{address2}"
    link3 = f"https://www.google.com/maps/dir/{startaddress}/{address3}"

    return render_template('map.html', address=address, link1=link1, link2=link2,link3=link3, radius=radius, atm1=atm1, long1=long1, lat1=lat1, atm2=atm2, long2=long2, lat2=lat2, atm3=atm3, long3=long3, lat3=lat3, maps_found=True)


if __name__ == "__main__":
    app.run(debug=True)
