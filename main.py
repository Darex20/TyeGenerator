from flask import Flask
import flask

app = Flask(__name__)

@app.route("/")
def index():
    return flask.render_template('index.html')
