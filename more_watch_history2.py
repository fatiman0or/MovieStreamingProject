# adding more watches for specififc movies over the last 30 days to test @app.get("/movies/top-watched")

from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]

movies_col = db["Movies"]
users_col = db["Users"]
watch_col = db["WatchHistory"]

print(" Connected to existing database!")

# to fetch existing data
all_movie_ids = [m["_id"] for m in movies_col.find()]
all_user_ids = [u["_id"] for u in users_col.find()]

if not all_movie_ids or not all_user_ids:
    print("❌ No movies or users found in DB. Please add some first.")
    exit()

# to add regular watch history
added_count = 0
for i in range(min(len(all_user_ids), len(all_movie_ids))):
    user_id = all_user_ids[i]
    movie_id = all_movie_ids[i]

    watch_time = datetime.now() - timedelta(days=random.randint(30, 60))  # older entries
    duration = random.randint(90, 150)

    existing = watch_col.find_one({
        "user_id": user_id,
        "movie_id": movie_id,
        "timestamp": watch_time
    })
    if not existing:
        watch_col.insert_one({
            "user_id": user_id,
            "movie_id": movie_id,
            "timestamp": watch_time,
            "watch_duration": duration
        })
        added_count += 1

print(f" Added {added_count} regular watch history entries successfully!")

# to add heavily watched movies in last 30 days
heavily_watched_movies = all_movie_ids[-3:]  # last 3 movies

heavy_added_count = 0
for movie_id in heavily_watched_movies:
    for user_id in all_user_ids:  # every user watches these movies
        for _ in range(random.randint(2, 4)):  # 2-4 watches per user per movie
            random_days_ago = random.randint(0, 29)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            watch_time = datetime.now() - timedelta(days=random_days_ago,
                                                    hours=random_hours,
                                                    minutes=random_minutes)
            duration = random.randint(90, 150)

            existing = watch_col.find_one({
                "user_id": user_id,
                "movie_id": movie_id,
                "timestamp": watch_time
            })
            if not existing:
                watch_col.insert_one({
                    "user_id": user_id,
                    "movie_id": movie_id,
                    "timestamp": watch_time,
                    "watch_duration": duration
                })
                heavy_added_count += 1

print(f" Added {heavy_added_count} heavily watched entries in the last 30 days!")

print("All watch history entries added safely without duplicates!")
