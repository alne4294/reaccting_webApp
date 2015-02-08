#Handles REST requests for accessing REACCTING data in MongoDB

import pymongo
from datetime import datetime
from flask import Flask, request, render_template, jsonify
import json
from bson import json_util
import os


app = Flask(__name__)

#==========================================================
#Formats error response to JSON

def format_error(message):
    return jsonify(error=1, data=message)

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


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
