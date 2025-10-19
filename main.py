from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create/access new database
db = client["MovieStreamingDB_NewFinal"]
print("✅ New database ready!")

# Movies collection
movies_col = db["Movies"]


movies_data = [
    {"title": "The Godfather", "release_year": 1972, "genres": ["Crime", "Drama"],
     "cast": [{"name": "Marlon Brando", "role": "Vito Corleone"}], "director": "Francis Ford Coppola", "rating": 9.2},
    {"title": "The Dark Knight", "release_year": 2008, "genres": ["Action", "Crime"],
     "cast": [{"name": "Christian Bale", "role": "Batman"}], "director": "Christopher Nolan", "rating": 9.0},
    {"title": "Inception", "release_year": 2010, "genres": ["Action", "Sci-Fi"],
     "cast": [{"name": "Leonardo DiCaprio", "role": "Cobb"}], "director": "Christopher Nolan", "rating": 8.8},
    {"title": "Pulp Fiction", "release_year": 1994, "genres": ["Crime", "Drama"],
     "cast": [{"name": "John Travolta", "role": "Vincent Vega"}], "director": "Quentin Tarantino", "rating": 8.9},
    {"title": "The Shawshank Redemption", "release_year": 1994, "genres": ["Drama"],
     "cast": [{"name": "Tim Robbins", "role": "Andy Dufresne"}], "director": "Frank Darabont", "rating": 9.3},
    {"title": "Forrest Gump", "release_year": 1994, "genres": ["Drama", "Romance"],
     "cast": [{"name": "Tom Hanks", "role": "Forrest Gump"}], "director": "Robert Zemeckis", "rating": 8.8},
    {"title": "Gladiator", "release_year": 2000, "genres": ["Action", "Drama"],
     "cast": [{"name": "Russell Crowe", "role": "Maximus"}], "director": "Ridley Scott", "rating": 8.5},
    {"title": "Titanic", "release_year": 1997, "genres": ["Drama", "Romance"],
     "cast": [{"name": "Leonardo DiCaprio", "role": "Jack Dawson"}], "director": "James Cameron", "rating": 7.8},
    {"title": "The Matrix", "release_year": 1999, "genres": ["Action", "Sci-Fi"],
     "cast": [{"name": "Keanu Reeves", "role": "Neo"}], "director": "Lana Wachowski", "rating": 8.7},
    {"title": "Avengers: Endgame", "release_year": 2019, "genres": ["Action", "Adventure"],
     "cast": [{"name": "Robert Downey Jr.", "role": "Iron Man"}], "director": "Anthony Russo", "rating": 8.4}
]

# Insert movies if not already present
movie_ids = []
for movie in movies_data:
    existing = movies_col.find_one({"title": movie["title"]})
    if not existing:
        result = movies_col.insert_one(movie)
        movie_ids.append(result.inserted_id)
    else:
        movie_ids.append(existing["_id"])
print("✅ 10 movies added!")

# Users collection
users_col = db["Users"]
users_data = [
    {"name": "Fatima Noor", "email": "fatima@example.com", "subscription_type": "Premium"},
    {"name": "Ali Khan", "email": "ali@example.com", "subscription_type": "Free"},
    {"name": "Sara Ahmed", "email": "sara@example.com", "subscription_type": "Premium"},
    {"name": "Hassan Raza", "email": "hassan@example.com", "subscription_type": "Standard"},
    {"name": "Ayesha Iqbal", "email": "ayesha@example.com", "subscription_type": "Premium"},
    {"name": "Bilal Shah", "email": "bilal@example.com", "subscription_type": "Free"},
    {"name": "Zara Malik", "email": "zara@example.com", "subscription_type": "Standard"},
    {"name": "Omar Farooq", "email": "omar@example.com", "subscription_type": "Premium"},
    {"name": "Noor Fatima", "email": "noor@example.com", "subscription_type": "Free"},
    {"name": "Usman Ali", "email": "usman@example.com", "subscription_type": "Standard"}
]

# Insert users if not already present
user_ids = []
for user in users_data:
    existing = users_col.find_one({"email": user["email"]})
    if not existing:
        result = users_col.insert_one(user)
        user_ids.append(result.inserted_id)
    else:
        user_ids.append(existing["_id"])
print("✅ 10 users added!")

# Reviews collection
reviews_col = db["Reviews"]
reviews_data = [
    {"user_id": user_ids[0], "movie_id": movie_ids[0], "rating": 10, "review_text": "Wow! Amazing movie, I totally recommend it."},
    {"user_id": user_ids[1], "movie_id": movie_ids[1], "rating": 9, "review_text": "Great film with stunning action scenes."},
    {"user_id": user_ids[2], "movie_id": movie_ids[2], "rating": 8, "review_text": "Mind-blowing concept, loved it."},
    {"user_id": user_ids[3], "movie_id": movie_ids[3], "rating": 9, "review_text": "Classic Tarantino, must watch!"},
    {"user_id": user_ids[4], "movie_id": movie_ids[4], "rating": 10, "review_text": "Inspiring story, beautifully acted."},
    {"user_id": user_ids[5], "movie_id": movie_ids[5], "rating": 8, "review_text": "Heartwarming and emotional journey."},
    {"user_id": user_ids[6], "movie_id": movie_ids[6], "rating": 9, "review_text": "Epic story and amazing performance."},
    {"user_id": user_ids[7], "movie_id": movie_ids[7], "rating": 8, "review_text": "Romantic and tragic, very touching."},
    {"user_id": user_ids[8], "movie_id": movie_ids[8], "rating": 9, "review_text": "Innovative sci-fi masterpiece."},
    {"user_id": user_ids[9], "movie_id": movie_ids[9], "rating": 8, "review_text": "Exciting and emotional finale."}
]

# Insert reviews if not already present
for review in reviews_data:
    existing = reviews_col.find_one({"user_id": review["user_id"], "movie_id": review["movie_id"]})
    if not existing:
        reviews_col.insert_one(review)
print("✅ 10 reviews added!")

# WatchHistory collection
watch_col = db["WatchHistory"]
watch_history_data = [
    {"user_id": user_ids[0], "movie_id": movie_ids[0], "timestamp": datetime(2025,10,18,20,0,0), "watch_duration": 175},
    {"user_id": user_ids[1], "movie_id": movie_ids[1], "timestamp": datetime(2025,10,18,18,30,0), "watch_duration": 152},
    {"user_id": user_ids[2], "movie_id": movie_ids[2], "timestamp": datetime(2025,10,17,21,0,0), "watch_duration": 148},
    {"user_id": user_ids[3], "movie_id": movie_ids[3], "timestamp": datetime(2025,10,16,19,0,0), "watch_duration": 154},
    {"user_id": user_ids[4], "movie_id": movie_ids[4], "timestamp": datetime(2025,10,15,20,0,0), "watch_duration": 142},
    {"user_id": user_ids[5], "movie_id": movie_ids[5], "timestamp": datetime(2025,10,14,18,0,0), "watch_duration": 142},
    {"user_id": user_ids[6], "movie_id": movie_ids[6], "timestamp": datetime(2025,10,13,21,0,0), "watch_duration": 155},
    {"user_id": user_ids[7], "movie_id": movie_ids[7], "timestamp": datetime(2025,10,12,20,0,0), "watch_duration": 195},
    {"user_id": user_ids[8], "movie_id": movie_ids[8], "timestamp": datetime(2025,10,11,19,0,0), "watch_duration": 136},
    {"user_id": user_ids[9], "movie_id": movie_ids[9], "timestamp": datetime(2025,10,10,20,0,0), "watch_duration": 181}
]

# Insert watch history if not already present
for watch in watch_history_data:
    existing = watch_col.find_one({"user_id": watch["user_id"], "movie_id": watch["movie_id"], "timestamp": watch["timestamp"]})
    if not existing:
        watch_col.insert_one(watch)
print("✅ 10 watch history entries added!")


# Text index on title, director, and cast names
movies_col.create_index([
    ("title", "text"),
    ("director", "text"),
    ("cast.name", "text")
])
print("✅ Text index created on Movies collection!")
watch_col.create_index("movie_id")
print("✅ Index created on WatchHistory for movie_id!")


