from main import movies_col  # import your MongoDB collection
from sentence_transformers import SentenceTransformer
import numpy as np

# to initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_movie_text(movie):
    cast_names = ", ".join([member['name'] for member in movie.get("cast", [])])
    genres = ", ".join(movie.get("genres", []))
    return f"{movie['title']}. Director: {movie['director']}. Cast: {cast_names}. Genres: {genres}"

# loop through all movies
for movie in movies_col.find({}):
    movie_text = get_movie_text(movie)
    embedding = model.encode(movie_text).tolist()  
    # to save embedings in mongo db
    movies_col.update_one(
        {"_id": movie["_id"]},
        {"$set": {"embedding": embedding}}
    )
    print(f"Embedding added for movie: {movie['title']}")
