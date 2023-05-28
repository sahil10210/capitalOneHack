OpenAI API Quickstart - Python example app

This is an example pet name generator app used in the OpenAI API quickstart tutorial. It uses the Flask web framework. Check out the tutorial or follow the instructions below to get set up.

Setup

If you don’t have Python installed, install it from here.

Clone this repository.

Navigate into the project directory:

$ cd openai-quickstart-python
Create a new virtual environment:

$ python -m venv venv
$ . venv/bin/activate
Install the requirements:

$ pip install -r requirements.txt
Make a copy of the example environment variables file:

$ cp .env.example .env
Add your API key to the newly created .env file.

Run the app:

$ flask run
You should now be able to access the app at http://localhost:5000! For the full context behind this example app, check out the tutorial.