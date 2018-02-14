from app import app
from flask import request, render_template
from jinja2.exceptions import TemplateNotFound
import json
import os

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/data')
def get_data():
    datafile = request.args.get('datafile')
    ret = { 'rc' : 0 }
    if datafile:
        try:
            with open(os.path.join('data',datafile),'r') as f:
                ret['data'] = json.load(f)                
        except FileNotFoundError as e:
            print(type(e))
            ret['rc'] = 2
            ret['message'] = "File " + datafile + " not found"
        except json.JSONDecodeError:
            ret['rc'] = 3
            ret['message'] = "The file " + datafile + " is not a valid json file"
    else:
        ret['rc'] = 1
        ret['message'] = "Datafile request argument is mandatory"
    return json.dumps(ret)

@app.route('/app')
def render_application():
    appfile = request.args.get('appfile')
    datafile = request.args.get('datafile')
    if datafile and appfile:
        try:
            print(os.path.join('template',appfile))
            return render_template(appfile, datafile=datafile)
        except TemplateNotFound:
            return "We could not find the file " + appfile + " in the template folder"
    else:
        return "You must specify both appfile and datafile arguments" 

