from flask import Flask, request
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

collection_name="properties"
propertyCollection=db[collection_name]

properties = {}
rootProperties = {}
for property in db.properties.find():
    if property["category"] == "root_property":
        rootProperties[property["name"]] = property["type"]
    elif property["category"] == "service_property":
        properties[property["name"]] = property["type"]

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        return flask.render_template('select.html', services=request.form.getlist('services'), properties=properties, rootProperties=rootProperties)

    services = db.services.find({})
    return flask.render_template('index.html', services=services.rewind())

@app.route('/project')
def project():
    list = []
    for service in db.services.find().rewind():
        if service["type"] == "project":
            list.append(service)
    return flask.render_template('project.html', services=list)

@app.route('/commercial')
def commercial():
    list = []
    for service in db.services.find().rewind():
        if service["type"] == "commercial":
            list.append(service)
    return flask.render_template('commercial.html', services=list)

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
            if value == "name":
                outputFile = outputFile + "\n- " + value + ": " + dict[key][value]
            elif "[]" in properties[value]:
                subProperties = dict[key][value].split(";")
                outputFile = outputFile + "\n  " + value + ": "
                for property in subProperties:
                    outputFile = outputFile + "\n  - " + property
            elif "bool" == properties[value]:
                outputFile = outputFile + "\n  " + value + ": " + "true"
            else:
                outputFile = outputFile + "\n  " + value + ": " + dict[key][value]


    html = "<p>" + outputFile.replace("\n", "<br>") + "</p>"

    return flask.render_template('preview.html', outputFile=outputFile, configName=request.form.get("name"), html=html, valueDict=dict)



