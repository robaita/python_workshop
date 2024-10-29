# Import necessary libraries
from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

# Define the name of the bot
name = 'Xarvis'

# Define the role of the bot
role = 'Ask Me!'

# Create a Flask web application
app = Flask(__name__)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

def get_answer(ques):
    # Fetch the HTML content from the website
    url = 'https://en.wikipedia.org/wiki/'+ques.lower().strip()
    print(url)
    response = requests.get(url)

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    all_paragraphs = soup.find_all('p')

    answer = "Sorry, Couldn't find answer"
    # Loop through and print each paragraph's text
    for p in all_paragraphs:
        if len(p.text)>150:
            answer = p.text
            break

    return answer


@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    ques = userText.split(":")[-1]
    print(ques)
    answer = get_answer(ques)
    return answer



# Run the Flask app
if __name__ == "__main__":
    app.run()