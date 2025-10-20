from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]

movies_col = db["Movies"]
users_col = db["Users"]
reviews_col = db["Reviews"]
watch_col = db["WatchHistory"]

print(" Connected to existing database!")

# add more data for movies collection
new_movies = [
    {"title": "Interstellar", "release_year": 2014, "genres": ["Sci-Fi", "Adventure"],
     "cast": [{"name": "Matthew McConaughey", "role": "Cooper"}], "director": "Christopher Nolan", "rating": 8.6},
    {"title": "The Lion King", "release_year": 1994, "genres": ["Animation", "Drama"],
     "cast": [{"name": "Matthew Broderick", "role": "Simba"}], "director": "Roger Allers", "rating": 8.5},
    {"title": "Joker", "release_year": 2019, "genres": ["Crime", "Drama"],
     "cast": [{"name": "Joaquin Phoenix", "role": "Arthur Fleck"}], "director": "Todd Phillips", "rating": 8.4},
    {"title": "Avatar", "release_year": 2009, "genres": ["Sci-Fi", "Adventure"],
     "cast": [{"name": "Sam Worthington", "role": "Jake Sully"}], "director": "James Cameron", "rating": 7.8},
    {"title": "Spider-Man: No Way Home", "release_year": 2021, "genres": ["Action", "Adventure"],
     "cast": [{"name": "Tom Holland", "role": "Spider-Man"}], "director": "Jon Watts", "rating": 8.3},
    {"title": "The Social Network", "release_year": 2010, "genres": ["Drama"],
     "cast": [{"name": "Jesse Eisenberg", "role": "Mark Zuckerberg"}], "director": "David Fincher", "rating": 7.7},
    {"title": "Parasite", "release_year": 2019, "genres": ["Thriller", "Drama"],
     "cast": [{"name": "Song Kang-ho", "role": "Kim Ki-taek"}], "director": "Bong Joon-ho", "rating": 8.6},
    {"title": "Whiplash", "release_year": 2014, "genres": ["Drama", "Music"],
     "cast": [{"name": "Miles Teller", "role": "Andrew Neiman"}], "director": "Damien Chazelle", "rating": 8.5},
    {"title": "Black Panther", "release_year": 2018, "genres": ["Action", "Adventure"],
     "cast": [{"name": "Chadwick Boseman", "role": "T’Challa"}], "director": "Ryan Coogler", "rating": 7.3},
    {"title": "Frozen", "release_year": 2013, "genres": ["Animation", "Adventure"],
     "cast": [{"name": "Idina Menzel", "role": "Elsa"}], "director": "Chris Buck", "rating": 7.4}
]

# i did this to make sure theres no duplicatiion
new_movie_ids = []
for movie in new_movies:
    existing = movies_col.find_one({"title": movie["title"]})
    if not existing:
        res = movies_col.insert_one(movie)
        new_movie_ids.append(res.inserted_id)
    else:
        new_movie_ids.append(existing["_id"])
print(f" Added {len(new_movie_ids)} new movies!")

# add more data for users collection
new_users = [
    {"name": "Ahmed Raza", "email": "ahmed.raza@example.com", "subscription_type": "Premium"},
    {"name": "Hina Malik", "email": "hina.malik@example.com", "subscription_type": "Standard"},
    {"name": "Tariq Ali", "email": "tariq.ali@example.com", "subscription_type": "Free"},
    {"name": "Sana Yousaf", "email": "sana.yousaf@example.com", "subscription_type": "Premium"},
    {"name": "Hamza Shahid", "email": "hamza.shahid@example.com", "subscription_type": "Standard"},
    {"name": "Laiba Asif", "email": "laiba.asif@example.com", "subscription_type": "Free"},
    {"name": "Raza Qureshi", "email": "raza.qureshi@example.com", "subscription_type": "Premium"},
    {"name": "Nimra Javed", "email": "nimra.javed@example.com", "subscription_type": "Standard"},
    {"name": "Adeel Khan", "email": "adeel.khan@example.com", "subscription_type": "Free"},
    {"name": "Emaan Fatima", "email": "emaan.fatima@example.com", "subscription_type": "Premium"}
]

# i did this to make sure theres no duplicatiion
new_user_ids = []
for user in new_users:
    existing = users_col.find_one({"email": user["email"]})
    if not existing:
        res = users_col.insert_one(user)
        new_user_ids.append(res.inserted_id)
    else:
        new_user_ids.append(existing["_id"])
print(f" Added {len(new_user_ids)} new users!")


# add more data for reviews collection
new_reviews = []
for i in range(10):
    new_reviews.append({
        "user_id": new_user_ids[i],
        "movie_id": new_movie_ids[i],
        "rating": 7 + i % 4,
        "review_text": f"Enjoyed watching movie #{i+11}! Great experience."
    })

# i did this to make sure theres no duplicatiion
for review in new_reviews:
    existing = reviews_col.find_one({"user_id": review["user_id"], "movie_id": review["movie_id"]})
    if not existing:
        reviews_col.insert_one(review)
print(" 10 new reviews added!")

# add more data for reviews collection
for i in range(10):
    new_entry = {
        "user_id": new_user_ids[i],
        "movie_id": new_movie_ids[i],
        "timestamp": datetime(2025, 10, 19, 18 + i % 3, 30, 0),
        "watch_duration": 120 + i * 5
    }
    existing = watch_col.find_one({"user_id": new_entry["user_id"], "movie_id": new_entry["movie_id"]})
    if not existing:
        watch_col.insert_one(new_entry)
print("10 new watch history entries added!")

print(" All new data added safely without overwriting old entries!")