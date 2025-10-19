# print_movies.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]
movies_col = db["Movies"]

# Print all movie IDs and titles
for movie in movies_col.find():
    print(movie["_id"], movie["title"])
