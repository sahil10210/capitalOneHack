import requests
import json
import pandas as py
from flask import Flask, render_template, request, redirect, flash, session, url_for

app = Flask(__name__)

#get all the data from the api
url = 'http://api.nessieisreal.com/enterprise/accounts?key=e1cac451319e9263333280ff4a5b28f6'
response = requests.get(url)
data = response.json()

with open('accounts.json', 'w') as file:
    json.dump(data, file)