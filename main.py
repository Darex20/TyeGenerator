from flask import Flask, request
from flask_wtf import FlaskForm
import flask
import markdown

app = Flask(__name__)

app.config['SECRET_KEY'] = 'DZ?gx3|:A^#}IRn$)JTt>qKfnk4>fn'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return flask.render_template('select.html', value=request.form.getlist('services'))
    return flask.render_template('index.html')

@app.route('/about')
def about():
    # static file from project root
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
        
    # getting README.md file directly from my github site
    """with open(file, 'r') as f:
        text=f.read()
        html = markdown.markdown(text)"""

    return flask.render_template('about.html', embed=html)

@app.route('/select', methods=['GET', 'POST'])
def select():
    str = request.form.get("devicesname") + request.form.get("devicesproject") + request.form.get("devicesimage")
    return str
    #return flask.render_template('preview.html', value=request)

"""@app.route('/handle_data', methods=['GET', 'POST'])
def handle_path():
    if request.method == 'POST':
        return "Hello"
    print(request.form.getlist('project_services'))"""