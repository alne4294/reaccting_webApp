
import pymongo
from datetime import datetime

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient(host='localhost',port=27017)
    sums = conn.sums
    print "Connected to: " + str(sums)

except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e 

# print "available collections: " + str(sumsDb.collection_names())
p1 = sums.p1
print "Connected to: " + str(p1)

doc = p1.find_one()
print "Document: " + str(doc)

count = p1.count()
print "Count: " + str(count)

result = p1.find({"device": "R28"}).count()
print "Number of R28 devices: " + str(result)

date = datetime.strptime("12/11/13 00:00", "%d/%m/%y %H:%M")
result = p1.find({'iso_dt':{"$gt":date}}).count()
print "Number of dates after 14/11/13: " + str(result)

stats = sums.command({'dbstats': 1})
print "SUMS stats: " + str(stats)

