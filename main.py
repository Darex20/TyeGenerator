from flask import Flask, request
from flask_wtf import FlaskForm
import flask
import markdown
import json
import pymongo

app = Flask(__name__)

with open('./config.json') as f:
    config = json.load(f)

app.config.update(config)
client = pymongo.MongoClient(config["connection_url"])

database_name="tye_generator"
db=client[database_name]

collection_name="services"
services=db[collection_name]

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return flask.render_template('select.html', value=request.form.getlist('services'))
    
    services = db.services.find()
    return flask.render_template('index.html', services=services)

@app.route('/about')
def about():
    # static file from project root
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    return flask.render_template('about.html', embed=html)

@app.route('/select', methods=['GET', 'POST'])
def select():
    services = db.services.find()
    dict = {}
    for service in services:
        print(service)
        currentDataDict = {}
        for field in service:
            print(field)
            value = service[field]
            value = request.form.get(value)
            if(value != None and value != ""):
                currentDataDict[field] = value
        if currentDataDict != {}:
            dict[service["service"]] = currentDataDict
            print(currentDataDict)
    
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
    return flask.render_template('preview.html', outputFile=outputFile, configName=configName, html=html, valueDict=dict)


"""@app.route('/preview', methods=['GET', 'POST'])
def preview():"""
