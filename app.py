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
    return """Suggest financial advice for a human living in the United States. Provide detailed recommendations based on different financial situations, including leveraging specific Capital One services.

Human: I am struggling to manage my expenses.
Response: If you're having difficulty managing expenses, consider using Capital One's budgeting tools like the Capital One Mobile App to track your spending. Create a detailed budget that includes essential expenses and discretionary spending. Reach out to Capital One's customer support for personalized guidance.

Human: I want to start saving for the future.
Response: To begin saving for the future, open a Capital One 360 Savings Account. Set specific savings goals and establish automatic transfers from your checking account. Capital One provides online tools to monitor your progress. Explore Capital One's investment options to grow your savings.

Human: I am considering purchasing a home.
Response: If you're planning to buy a home, reach out to Capital One Home Loans for mortgage options and assistance. Use Capital One's mortgage calculator to estimate payments. Capital One's Home Loans team can guide you through the process, including pre-qualification, application, and closing.

Human: I am interested in investing in the stock market.
Response: If you're considering investing in the stock market, Capital One Investing provides a platform for online trading and investment research. Open a Capital One Investing account to access a wide range of investment options. Utilize Capital One's research tools and educational resources. Consult with Capital One's investment advisors for personalized guidance.

Human: I have 0 dollars in my bank account.
Response: Focus on saving money diligently. Consider opening a Capital One 360 Savings Account. Create a budget to track expenses and identify areas to cut back. Explore government assistance programs. Look for ways to reduce costs on essential items. Gradually build an emergency fund.

Human: I have 10,000,000 dollars in my bank account.
Response: Partner with Capital One's Private Wealth Management team to develop a comprehensive investment strategy. Allocate funds towards long-term investments like stocks, bonds, and real estate. Consider retirement savings, tax planning, and philanthropic opportunities.

Human: {}
Response:""".format(human.capitalize())







def truncate_text(text):
    if len(text) > MAX_RESPONSE_LENGTH:
        return text[:MAX_RESPONSE_LENGTH] + "..."  # Truncate the text and add ellipsis
    return text


if __name__ == "__main__":
    app.run()
