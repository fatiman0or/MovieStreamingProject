# just to print movies collection
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]
movies_col = db["Movies"]

for movie in movies_col.find():
    print(movie["_id"], movie["title"])
