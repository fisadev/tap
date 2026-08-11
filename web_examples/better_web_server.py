#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["flask"]
# ///
from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define the route for a page
@app.route('/hello/<name>')
def hello_world(name):
    return f"<html><body><h1>Hello {name}!</h1></body></html>"

# Run the local development server
app.run(debug=True)
