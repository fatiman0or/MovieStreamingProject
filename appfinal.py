from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from difflib import SequenceMatcher


app = Flask(__name__)

# Connect to Mongo DB
client = MongoClient("mongodb://localhost:27017/")
db = client["MovieStreamingDB_NewFinal"]

movies_col = db["Movies"]
users_col = db["Users"]
reviews_col = db["Reviews"]
watch_col = db["WatchHistory"]

def similarity(a, b):
    """Returns a ratio between 0 and 1 indicating how similar two strings are"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()



# ROUTES

# home route

@app.route('/')
def home():
    return "🎬 Movie Streaming API is running!"

# to get watch history of a specific user

@app.route('/users/<user_id>/history', methods=['GET'])
def get_watch_history(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID"}), 400

        history_cursor = watch_col.find({"user_id": ObjectId(user_id)})
        history_list = []

        for entry in history_cursor:
            movie = movies_col.find_one({"_id": entry["movie_id"]})
            history_list.append({
                "movie_title": movie["title"] if movie else "Unknown",
                "timestamp": entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "watch_duration": entry["watch_duration"]
            })

        return jsonify({"user_id": user_id, "history": history_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# to get reviews of a specific movie

@app.route('/movies/<movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    # Movie Reviews code
    try:
        if not ObjectId.is_valid(movie_id):
            return jsonify({"error": "Invalid movie ID"}), 400

        reviews_cursor = reviews_col.find({"movie_id": ObjectId(movie_id)})
        reviews_list = []

        for review in reviews_cursor:
            user = users_col.find_one({"_id": review["user_id"]})
            reviews_list.append({
                "user_name": user["name"] if user else "Unknown",
                "rating": review["rating"],
                "review_text": review["review_text"]
            })

        return jsonify({"movie_id": movie_id, "reviews": reviews_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from difflib import SequenceMatcher
from flask import request, jsonify

# hybrid search

@app.route('/movies/search', methods=['GET'])
def hybrid_search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results_list = []

    # Precompute watch counts
    watch_counts = {}
    for entry in watch_col.find({}):
        movie_id_str = str(entry["movie_id"])
        watch_counts[movie_id_str] = watch_counts.get(movie_id_str, 0) + 1

    for movie in movies_col.find({}):
        movie_id_str = str(movie["_id"])

        # Compute title similarity
        title_similarity = SequenceMatcher(None, query.lower(), movie.get("title", "").lower()).ratio()
        # Compute director similarity
        director_similarity = SequenceMatcher(None, query.lower(), movie.get("director", "").lower()).ratio()
        # Compute cast similarity
        cast_similarity = 0
        matched_cast = []
        for member in movie.get("cast", []):
            member_name = member.get("name", "")
            sim = SequenceMatcher(None, query.lower(), member_name.lower()).ratio()
            if sim > 0.5:  # threshold for matching cast
                cast_similarity = max(cast_similarity, sim)
                matched_cast.append(member_name)

        # Take the maximum similarity across title, director, and cast
        similarity_score = max(title_similarity, director_similarity, cast_similarity)

        # Skip if similarity is too low
        if similarity_score < 0.5:
            continue

        # Weighted score: 50% similarity, 30% rating (out of 10), 20% popularity
        weighted_score = (
            0.5 * similarity_score +
            0.3 * (movie.get("rating", 0) / 10) +
            0.2 * (watch_counts.get(movie_id_str, 0) / max(1, max(watch_counts.values(), default=1)))
        )

        results_list.append({
            "movie_id": movie_id_str,
            "title": movie.get("title", "Unknown"),
            "director": movie.get("director", "Unknown"),
            "genres": movie.get("genres", []),
            "rating": movie.get("rating", 0),
            "cast": [member.get("name", "Unknown") for member in movie.get("cast", [])],
            "matched_cast": matched_cast,
            "popularity": watch_counts.get(movie_id_str, 0),
            "similarity": round(similarity_score, 2),
            "weighted_score": round(weighted_score, 2)
        })

    # Sort results by weighted_score descending
    results_list.sort(key=lambda x: x["weighted_score"], reverse=True)

    return jsonify({"query": query, "results": results_list})



# RUN SERVER

if __name__ == "__main__":
    app.run(debug=True)
