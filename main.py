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
    services = ["control_point", "devices", "reports", "video", "archive", "mongodb", "redis", "greylog", "dapr", "sqlserver"]
    fields = ["name", "project", "image", "port", "protocol"]
    dict = {}
    for service in services:
        currentDataDict = {}
        for field in fields:
            str = service + field
            str = request.form.get(str)
            if(str != None and str != ""):
                currentDataDict[field] = str
        if currentDataDict != {}:
            dict[service] = currentDataDict
    
    configName = request.form.get("configname")
    outputFile = "name: " + configName + "\n" + "services:"
    
    for key in dict:
        check = True
        for value in dict[key]:
            if value == "name":
                outputFile = outputFile + "\n- " + value + ": " + dict[key][value]
            elif (value == "port" or value == "protocol") and check:
                outputFile = outputFile + "\n  bindings:\n  - " + value + ": " + dict[key][value]
                check = False    
            elif not check and value == "protocol":
                outputFile =  outputFile + "\n    " + value + ": " + dict[key][value]
            else:
                outputFile = outputFile + "\n  " + value + ": " + dict[key][value]

    print(outputFile)
    html = "<p>" + outputFile.replace("\n", "<br>") + "</p>"

    # str = request.form.get("devicesname") + request.form.get("devicesproject") + request.form.get("devicesimage")
    return flask.render_template('preview.html', outputFile=outputFile, configName=configName, html=html)

"""@app.route('/handle_data', methods=['GET', 'POST'])
def handle_path():
    if request.method == 'POST':
        return "Hello"
    print(request.form.getlist('project_services'))"""