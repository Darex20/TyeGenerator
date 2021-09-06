from flask import Flask, request
import flask
import markdown
import json
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

with open('./config.json') as f:
    config = json.load(f)

app.config.update(config)
client = pymongo.MongoClient(config["connection_url"])

database_name = config["database_name"]
db=client[database_name]

collection_name = config["collection_name"]
services=db[collection_name]

rootProperties = config["root_properties"]

def typeList(type):
    list = []
    for service in db.services.find().rewind():
        if service["type"] == type:
            list.append(service)
    return list

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        localServices = []
        for service in db.services.find({}):
            if service["rootName"] in request.form.getlist('services'):
                localServices.append(service) 
        return flask.render_template('select.html', services=localServices, rootProperties=rootProperties)

    services=db.services.find({})
    return flask.render_template('index.html', services=services.rewind())

@app.route('/addservice', methods=['GET', 'POST'])
def addservice():
    properties = config["service_properties"]
    if request.method == 'POST':
        print(request.form)
        type = request.form.get("add_service")
        print(type)
        service_name = request.form.get("service_name")
        root_name = service_name.strip().lower().replace(" ", "_")
        service = {}
        json_properties = {}
        form_properties = request.form.getlist('properties')
        for property in properties:
            if property in form_properties:
                json_property = {"type": properties[property], "value": request.form.get(property)}
                json_properties[property] = json_property
        service = {"displayName": service_name, "rootName": root_name, "type": type, "properties": json_properties}
        services.insert_one(service)
        return flask.render_template(f'{type}.html', services=typeList(type))
    else:
        type = flask.request.args.get("add_service")
        add_services = []
        for service in typeList(type):
            add_services.append(service["displayName"])
        return flask.render_template('addservice.html', type=type, properties=properties, services=add_services)

@app.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        _id = request.form.get("clicked_button")
        result = db.services.delete_one({"_id": ObjectId(_id)})
    list = typeList('project')
    return flask.render_template('project.html', services=list)

@app.route('/commercial', methods=['GET', 'POST'])
def commercial():
    if request.method == 'POST':
        _id = request.form.get("clicked_button")
        result = db.services.delete_one({"_id": ObjectId(_id)})
    list = typeList('commercial')
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
        for property in service["properties"]:
            value = service["rootName"] + "_" + property
            value = request.form.get(value)
            if(value != None and value != ""):
                currentDataDict[property] = [value, service["properties"][property]]
        if currentDataDict != {}:
            dict[service["rootName"]] = currentDataDict
    
    for property in rootProperties:
        value = request.form.get(property)
        if value:
            outputFile = outputFile + property + ": " + value + "\n"

    outputFile = outputFile + "services:"
    
    for service in dict:
        for tuple in dict[service]:
            print(dict[service][tuple])
            if tuple == "name":
                outputFile = outputFile + "\n- " + tuple + ": " + dict[service][tuple][0]
            elif "[]" in dict[service][tuple][1]:
                subProperties = dict[service][tuple][0].split(";")
                outputFile = outputFile + "\n  " + tuple + ": "
                for property in subProperties:
                    outputFile = outputFile + "\n  - " + property
            elif "bool" == dict[service][tuple][1]:
                outputFile = outputFile + "\n  " + dict[service][tuple][0] + ": " + "true"
            else:
                outputFile = outputFile + "\n  " + tuple + ": " + dict[service][tuple][0]


    html = "<p>" + outputFile.replace("\n", "<br>") + "</p>"

    return flask.render_template('preview.html', outputFile=outputFile, configName=request.form.get("name"), html=html, valueDict=dict)



