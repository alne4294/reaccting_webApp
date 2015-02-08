#Handles REST requests from server for a queueing system

import pymongo
from datetime import datetime
# from Entry import entry
from flask import Flask, request, jsonify
import json as j


app = Flask(__name__)
# entryList = EntryList()

#==========================================================
#Formats response to JSON

def format_response(success, obj):
    response = {"error": not success}
    if isinstance(obj, deque):
        data = []
        for elt in obj:
            data.append(elt.format())
        response["data"] = data
    elif isinstance(obj, entry):
        response["data"] = obj.format()
    else:
        response["data"] = obj
    return jsonify(**response)


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

        # print "available collections: " + str(sumsDb.collection_names())
        p1 = sums.p1
        # print "Connected to: " + str(p1)

        doc = p1.find_one()
        # print "Document: " + str(doc)
        return "Document: " + str(doc)

        #TODO: readd format_response
        # return format_response(isTrue, entry)
    else:
        return format_response(False, "Need a GET request at this endpoint")


@app.route('/api/1.0/mongoWebApp/countTotal')
def countTotal():
    if request.method == 'GET':
        try:
            conn=pymongo.MongoClient(host='localhost',port=27017)
            sums = conn.sums
            print "Connected to: " + str(sums)

        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e 

        # print "available collections: " + str(sumsDb.collection_names())
        p1 = sums.p1
        count = p1.count()
        # print "Count: " + str(count)
        # print "Connected to: " + str(p1)

        return "Total count: " + str(count)

        #TODO: readd format_response
        # return format_response(isTrue, entry)
    else:
        return format_response(False, "Need a GET request at this endpoint")



if __name__ == '__main__':
    app.debug = True
    app.run()
