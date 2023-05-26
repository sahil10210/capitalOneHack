import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_RESPONSE_LENGTH = 500  # Define the maximum length of the response to display


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        human = request.form["human"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(human),
            temperature=0.6,
            max_tokens=MAX_RESPONSE_LENGTH,  # Limit the response length
        )
        result = truncate_text(response.choices[0].text)
        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(human):
    return """Suggest financial advice for a human living in the United States.

Human: I have 0 dollars in my bank account.
Response: Save money
Human: I have 10000000 dollars in my bank account
Response: Invest 200,000 into a Roth IRA account, save 200,000, put 300,000 into investments, and use the rest of the money for personal expenses
Human: {}
Response:""".format(
        human.capitalize()
    )


def truncate_text(text):
    if len(text) > MAX_RESPONSE_LENGTH:
        return text[:MAX_RESPONSE_LENGTH] + "..."  # Truncate the text and add ellipsis
    return text


if __name__ == "__main__":
    app.run()
