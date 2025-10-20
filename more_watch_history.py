'''
this is an attempt to make a few movies be watched over and over again to test aggregation
but here the dates got messed up
i did this correctly in more_watch_history2.py
'''
from datetime import datetime, timedelta
from main import watch_col, movies_col, users_col

def add_watch_history():

    # fetch users and movies from database
    users = list(users_col.find())
    movies = list(movies_col.find())

    if len(users) < 5 or len(movies) < 5:
        print("⚠️ Not enough users or movies in DB to add watch history.")
        return

    watch_entries = []

    # repeated watches for first 3 movies
    repeated_movies_ids = [movies[0]['_id'], movies[1]['_id'], movies[2]['_id']]
    for movie_id in repeated_movies_ids:
        for i in range(3):  # Each movie watched 3 times by different users
            user_id = users[i]['_id']
            watch_entries.append({
                "user_id": user_id,
                "movie_id": movie_id,
                "timestamp": datetime(2025, 10, 19, 18+i, 0, 0),
                "watch_duration": 120 + i*10
            })

    # single watches for a few more movies
    for i, movie in enumerate(movies[3:6]):  # 3 more movies
        user_id = users[i]['_id']
        watch_entries.append({
            "user_id": user_id,
            "movie_id": movie['_id'],
            "timestamp": datetime(2025, 10, 19, 19+i, 30, 0),
            "watch_duration": 90 + i*5
        })

    # to avoid duplicates
    inserted_count = 0
    for entry in watch_entries:
        exists = watch_col.find_one({
            "user_id": entry["user_id"],
            "movie_id": entry["movie_id"],
            "timestamp": entry["timestamp"]
        })
        if not exists:
            watch_col.insert_one(entry)
            inserted_count += 1

    print(f" Added {inserted_count} watch history entries successfully!")

# to prevent automatic execution when imported
if __name__ == "__main__":
    add_watch_history()
