from flask import Flask
import flask

app = Flask(__name__)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route('/about')
def about():
    return flask.render_template('about.html')