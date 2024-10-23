from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Task Manager</h1>"

if __name__ == "__main__":
    app.run(debug=True)

# Flask(__name__): Initializes the Flask app. The __name__ argument is used to determine the root path of the app.
# @app.route('/'): Defines the route for the home page (i.e., the URL "/").
# app.run(debug=True): Runs the development server with debug mode on.

