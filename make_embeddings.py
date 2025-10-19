from main import movies_col  # import your MongoDB collection
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_movie_text(movie):
    cast_names = ", ".join([member['name'] for member in movie.get("cast", [])])
    genres = ", ".join(movie.get("genres", []))
    return f"{movie['title']}. Director: {movie['director']}. Cast: {cast_names}. Genres: {genres}"

# Loop through all movies
for movie in movies_col.find({}):
    movie_text = get_movie_text(movie)
    embedding = model.encode(movie_text).tolist()  # Convert numpy array to list
    # Save embedding in MongoDB
    movies_col.update_one(
        {"_id": movie["_id"]},
        {"$set": {"embedding": embedding}}
    )
    print(f"✅ Embedding added for movie: {movie['title']}")
