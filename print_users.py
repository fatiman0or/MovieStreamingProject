# just to print users collection

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]
users_col = db["Users"]

for user in users_col.find():
    print(user["_id"], user["name"])
