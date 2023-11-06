from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "123"

@app.route("/")
def home():
    """
    Homepage route.

    Returns:
        str: Rendered template for the index.html page.
    """
    return render_template("index.html")

with app.app_context():
    # Importing different views for the website.
    from views import *

if __name__ == "__main__":
    app.run(debug=True)
