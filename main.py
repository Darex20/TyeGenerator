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

properties = {
        "name": "String",
        "image": "String", 
        "env": "String[]", 
        "project": "String", 
        "dockerFile": "String",
        "dockerFileArgs": "String[]",
        "dockerFileContext": "String",
        "executable": "String",
        "external": "bool",
        "replicas": "int",
        "env_file": "String[]",
        "args": "String",
        "build": "bool",
        "workingDirectory": "String",
        "include": "String",
        "repository": "String",
        "cloneDirectory": "String",
        "azureFunctions": "String",
        "pathToFunc": "String"
}

rootProperties = {
    "name": "String",
    "registry": "String",
    "namespace": "String",
    "network": "String",
}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        return flask.render_template('select.html', services=request.form.getlist('services'), properties=properties, rootProperties=rootProperties)

    services = db.services.find({})
    return flask.render_template('index.html', services=services.rewind())

@app.route('/about')
def about():
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    return flask.render_template('about.html', embed=html)

@app.route('/select', methods=['GET', 'POST'])
def select():
    
    services = db.services.find()
    dict = {}
    outputFile = ""
    for service in services.rewind():
        currentDataDict = {}
        print(service)
        for property in properties:
            value = service["rootName"] + "_" + property
            value = request.form.get(value)
            if(value != None and value != ""):
                currentDataDict[property] = value
        if currentDataDict != {}:
            dict[service["rootName"]] = currentDataDict
    
    for property in rootProperties:
        value = request.form.get(property)
        if value:
            outputFile = outputFile + property + ": " + value + "\n"

    outputFile = outputFile + "services:"
    
    for key in dict:
        check = True
        for value in dict[key]:
            print(properties[value])
            if value == "name":
                outputFile = outputFile + "\n- " + value + ": " + dict[key][value]
            elif "[]" in properties[value]:
                subProperties = dict[key][value].split(";")
                outputFile = outputFile + "\n  " + value + ": "
                for property in subProperties:
                    outputFile = outputFile + "\n  - " + property
                # outputFile = outputFile + "\n- " + value + ": " + dict[key][value]
            elif "bool" == properties[value]:
                outputFile = outputFile + "\n  " + value + ": " + "true"

            else:
                outputFile = outputFile + "\n  " + value + ": " + dict[key][value]

            """elif (value == "port" or value == "protocol") and check:
                outputFile = outputFile + "\n  bindings:\n  - " + value + ": " + dict[key][value]
                check = False    
            elif not check and value == "protocol":
                outputFile =  outputFile + "\n    " + value + ": " + dict[key][value]
            else:
                outputFile = outputFile + "\n  " + value + ": " + dict[key][value]"""

    html = "<p>" + outputFile.replace("\n", "<br>") + "</p>"

    return flask.render_template('preview.html', outputFile=outputFile, configName=request.form.get("name"), html=html, valueDict=dict)

