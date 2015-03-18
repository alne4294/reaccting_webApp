#Handles REST requests for accessing REACCTING data in MongoDB

import pymongo
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, Response
from functools import wraps
import json
from bson import json_util
import os


app = Flask(__name__)

#==========================================================
#Formats error response to JSON

def format_error(message):
    return jsonify(error=1, data=message)


#==========================================================
#Authentication helpers

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid."""

    return username == 'reaccting' and password == 'ghana'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


#==========================================================
#GET

@app.route('/api/1.0/mongoWebApp/findOne')
def findOne():
    if request.method == 'GET':
        try:
            conn=pymongo.MongoClient(host='localhost',port=27017)
            sums = conn.sums
            print "Connected to: " + str(sums)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 

        p1 = sums.p1

        if(app.debug):
            print "available collections: " + str(sums.collection_names())
            print "Connected to: " + str(p1)

        doc = p1.find_one()

        jsonDoc = json.dumps(doc, default=json_util.default)
        return jsonify(error=0, data=jsonDoc)

    else:
        return format_error("Need a GET request at this endpoint")


@app.route('/api/1.0/mongoWebApp/find')
def find():
    if request.method == 'GET':
        try:
            conn=pymongo.MongoClient(host='localhost',port=27017)
            sums = conn.sums
            print "Connected to: " + str(sums)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 

        p1 = sums.p1

        if(app.debug):
            print "available collections: " + str(sums.collection_names())
            print "Connected to: " + str(p1)

        date = datetime.strptime("15/06/14 00:00", "%d/%m/%y %H:%M")
        docs = p1.find({'iso_dt':{"$gt":date}, "device":"R28"})
        
        if(app.debug):
            print "Retrieved: " + str((docs).count()) + " records"

        json_docs = []
        for doc in docs:
            json_doc = json.dumps(doc, default=json_util.default)
            json_docs.append(json_doc)

        return jsonify(error=0, data=json_docs)

    else:
        return format_error("Need a GET request at this endpoint")


@app.route('/api/1.0/mongoWebApp/countTotal')
def countTotal():
    if request.method == 'GET':
        try:
            conn=pymongo.MongoClient(host='localhost',port=27017)
            sums = conn.sums
            print "Connected to: " + str(sums)
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 

        p1 = sums.p1
        count = p1.count()

        if(app.debug):
            print "available collections: " + str(sums.collection_names())
            print "Connected to: " + str(p1)

        return jsonify(error=0, count=count)

    else:
        return format_response(False, "Need a GET request at this endpoint")


@app.route('/api/1.0/mongoWebApp/getPhoneData/<int:phoneNum>')
def getPhoneData(phoneNum):
  
  if(phoneNum < 1 or phoneNum > 2):
    # Return empty dictionary
    return jsonify(data={})
  

  # Open the file for reading
  jsonFile = open('Phone'+str(phoneNum)+'.json', 'r')

  # Load the contents from the file, which creates a new dictionary
  coordDict = json.load(jsonFile)

  # Close the file... we don't need it anymore  
  jsonFile.close()

  # Convert Matlab time into Gregorian time string
  for doc in coordDict:
    matlab_datenum = float(doc["time"])
    python_datetime = datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum%1) - timedelta(days = 366)
    #Convert to string and remove units smaller than seconds
    doc["time"] = (str(python_datetime)).split('.', 1)[0]

  return jsonify(data=coordDict)



@app.route('/animation')
def animation():
    return render_template('animation.html')


@app.route("/")
@requires_auth
def index():
    return render_template('index.html')


@app.route("/map")
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
