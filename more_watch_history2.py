# more_watch_history.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# ---------------- CONNECT TO DB ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]

movies_col = db["Movies"]
users_col = db["Users"]
watch_col = db["WatchHistory"]

print("✅ Connected to database!")

# ---------------- GET ALL MOVIES & USERS ----------------
all_movie_ids = [movie["_id"] for movie in movies_col.find()]
all_user_ids = [user["_id"] for user in users_col.find()]

# ---------------- ADD RANDOM WATCH HISTORY ----------------
added_count = 0
for user_id in all_user_ids:
    for movie_id in all_movie_ids:
        # Generate a watch timestamp within the last 60 days
        random_days_ago = random.randint(0, 60)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        watch_time = datetime.now() - timedelta(days=random_days_ago,
                                                hours=random_hours,
                                                minutes=random_minutes)
        duration = random.randint(60, 150)  # watch duration in minutes

        # Check if this user already watched this movie in the exact same minute
        exists = watch_col.find_one({
            "user_id": user_id,
            "movie_id": movie_id,
            "timestamp": {"$eq": watch_time}
        })
        if not exists:
            watch_col.insert_one({
                "user_id": user_id,
                "movie_id": movie_id,
                "timestamp": watch_time,
                "watch_duration": duration
            })
            added_count += 1

print(f"✅ Added {added_count} regular watch history entries!")

# ---------------- ADD HEAVILY WATCHED MOVIES (LAST 3 MOVIES) ----------------
heavy_movies = all_movie_ids[-3:]  # last 3 movies
heavy_added_count = 0

for movie_id in heavy_movies:
    for user_id in all_user_ids:  # all users watch these movies
        for _ in range(random.randint(2, 4)):  # 2-4 watches per user per movie
            random_days_ago = random.randint(0, 29)  # last 30 days
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            watch_time = datetime.now() - timedelta(days=random_days_ago,
                                                    hours=random_hours,
                                                    minutes=random_minutes)
            duration = random.randint(90, 150)

            # No duplicate check; allow multiple watches for heavy tracking
            watch_col.insert_one({
                "user_id": user_id,
                "movie_id": movie_id,
                "timestamp": watch_time,
                "watch_duration": duration
            })
            heavy_added_count += 1

print(f"✅ Added {heavy_added_count} heavily watched entries in the last 30 days!")
print("🎉 Done! Your database now has more realistic watch history for aggregation testing.")
