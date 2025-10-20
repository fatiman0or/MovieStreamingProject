
from fastapi import FastAPI, HTTPException, Query
from bson.objectid import ObjectId
from difflib import SequenceMatcher
from datetime import datetime
import json
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
import numpy as np



# to import my collections
from main import movies_col, users_col, reviews_col, watch_col

# to create  fast api
app = FastAPI(
    title="🎬 Movie Streaming API",
    version="2.0",
    description="FastAPI version of the Movie Streaming backend"
)

# to initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# function for semantic search

def semantic_similarity_search(query: str, top_k: int = 5):

    query_embedding = embedding_model.encode(query)

    results = []
    for movie in movies_col.find({}):
        if "embedding" in movie:
            movie_embedding = np.array(movie["embedding"])
            # cosine similarity
            similarity = np.dot(query_embedding, movie_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(movie_embedding)
            )
            results.append({
                "movie_id": str(movie["_id"]),
                "title": movie.get("title", "Unknown"),
                "director": movie.get("director", "Unknown"),
                "genres": movie.get("genres", []),
                "rating": movie.get("rating", 0),
                "similarity": round(float(similarity), 3)
            })

    # to sort descending by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_k]

# making 2 functions reciprocal_rank_fusion and keyword_search_logic_for_rrf to use in hybrid search

# integrates results from various search algos boosting items that consistently appear near the top using RRF logic
def reciprocal_rank_fusion(rankings: list[list[dict]], k: int = 60) -> list[dict]:
    fused_scores = {}
    
    for ranking in rankings:
        for rank, item in enumerate(ranking):
            movie_id = item['movie_id']
            score = 1 / (k + rank + 1)
            fused_scores[movie_id] = fused_scores.get(movie_id, 0) + score
            
    sorted_fused_scores = sorted(
        fused_scores.items(), 
        key=lambda item: item[1], 
        reverse=True
    )
    
    final_results = []
    metadata_map = {}
    
    for ranking in rankings:
        for item in ranking:
            metadata_map[item['movie_id']] = {
                "title": item.get('title', 'Unknown'),
                "director": item.get('director', 'Unknown'),
                "genres": item.get('genres', []),
                "rating": item.get('rating', 0),
            }

    for movie_id, score in sorted_fused_scores:
        metadata = metadata_map.get(movie_id, {})
        final_results.append({
            "movie_id": movie_id,
            "title": metadata.get('title', 'Unknown'),
            "rrf_score": round(score, 4)
        })
        
    return final_results

# gets movies matching user keywords using text search and returns ranked results for fusion
def keyword_search_logic_for_rrf(query: str, search_k: int = 50):
    results = []
    query_lower = query.lower()
    
    for movie in movies_col.find({}):
        title_sim = SequenceMatcher(None, query_lower, movie.get("title","").lower()).ratio()
        director_sim = SequenceMatcher(None, query_lower, movie.get("director","").lower()).ratio()
        
        # to calculate max similarity for cast
        cast_sim = max([
            SequenceMatcher(None, query_lower, c.get("name","").lower()).ratio() 
            for c in movie.get("cast",[]) 
            if isinstance(c, dict) or isinstance(c, str)
        ] + [0])
        
        sim_score = max(title_sim, director_sim, cast_sim)
        
        # keeping a low threshold to ensure enough candidates for RRF
        if sim_score < 0.5:
            continue
            
        results.append({
            "movie_id": str(movie["_id"]),
            "title": movie.get("title","Unknown"),
            "similarity": round(sim_score,2)
        })
        
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:search_k]


@app.get("/movies/search/hybrid")
def hybrid_search(query: str = Query(..., min_length=1), top_k: int = 10):
    """
    Combines Keyword and Semantic search results using Reciprocal Rank Fusion (RRF).
    """
    search_k = max(2 * top_k, 20) 

    # first get rankings from both methods
    semantic_results = semantic_similarity_search(query, top_k=search_k)
    keyword_results = keyword_search_logic_for_rrf(query, search_k=search_k)

    # then fuse the rankings
    rankings_to_fuse = [semantic_results, keyword_results]
    hybrid_results = reciprocal_rank_fusion(rankings_to_fuse)
    
    # finally return the top_k results
    return {"query": query, "results": hybrid_results[:top_k]}

# all api routes

# to confirm api is running
@app.get("/")
def home():
    return {"message": "🎬 Movie Streaming API is running with FastAPI!"}


# to get watch history of a specific User
@app.get("/users/{user_id}/history")
def get_watch_history(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    try:
        history_cursor = watch_col.find({"user_id": ObjectId(user_id)})
        history_list = []

        for entry in history_cursor:
            movie = movies_col.find_one({"_id": entry["movie_id"]})
            history_list.append({
                "movie_title": movie["title"] if movie else "Unknown",
                "timestamp": entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "watch_duration": entry["watch_duration"]
            })

        # return formatted JSON response
        return JSONResponse(
    content=json.loads(json.dumps({"user_id": user_id, "history": history_list}, indent=4))
)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# to get reviews for a specific movie
@app.get("/movies/{movie_id}/reviews")
def get_movie_reviews(movie_id: str):
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(status_code=400, detail="Invalid movie ID")

    try:
        reviews_cursor = reviews_col.find({"movie_id": ObjectId(movie_id)})
        reviews_list = []

        for review in reviews_cursor:
            user = users_col.find_one({"_id": review["user_id"]})
            reviews_list.append({
                "user_name": user["name"] if user else "Unknown",
                "rating": review["rating"],
                "review_text": review["review_text"]
            })
        # return formatted JSON response
        return {"movie_id": movie_id, "reviews": reviews_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# keyword based movie search
@app.get("/movies/search/keyword")
def search_movies_keyword(query: str):
    results = []
    query_lower = query.lower()

    for movie in movies_col.find():
        # to get movie info
        title = movie.get("title", "")
        director = movie.get("director", "")
        cast = movie.get("cast", [])

        # to normalize for comparison
        title_lower = title.lower()

        # movie director can be string or list
        if isinstance(director, list):
            director_lower = " ".join(director).lower()
        else:
            director_lower = str(director).lower()

        # to convert into lowercase names
        cast_lower = []
        for c in cast:
            if isinstance(c, dict):
                name = c.get("name", "").lower()
            else:
                name = str(c).lower()
            if name:
                cast_lower.append(name)

        # direct substring match (high confidence)
        if (
            query_lower in title_lower
            or query_lower in director_lower
            or any(query_lower in c for c in cast_lower)
        ):
            sim_score = 1.0
        else:
            # fuzzy character similarity
            sim_score = max(
                SequenceMatcher(None, query_lower, title_lower).ratio(),
                SequenceMatcher(None, query_lower, director_lower).ratio(),
                max((SequenceMatcher(None, query_lower, c).ratio() for c in cast_lower), default=0)
            )

        # to apply a smart threshold (tuneable)
        if sim_score >= 0.65:
            results.append({
                "movie_id": str(movie["_id"]),
                "title": title,
                "director": director,
                "similarity": round(sim_score, 2)
            })

    # Sort high to low by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return {"query": query, "results": results}

from datetime import timedelta

# top-watched movies in the last 30 days
@app.get("/movies/top-watched")
def top_watched_movies_last_month(top_k: int = 5):
    """
    Returns the top_k most-watched movies in the last 30 days.
    Uses aggregation on watch history.
    """
    try:
        # to calculate date 30 days ago
        thirty_days_ago = datetime.now() - timedelta(days=30)

        # mongo db aggregation pipeline
        pipeline = [
            {"$match": {"timestamp": {"$gte": thirty_days_ago}}},
            {"$group": {
                "_id": "$movie_id",
                "watch_count": {"$sum": 1}
            }},
            {"$sort": {"watch_count": -1}},
            {"$limit": top_k},
            {"$lookup": {
                "from": "Movies",
                "localField": "_id",
                "foreignField": "_id",
                "as": "movie_info"
            }},
            {"$unwind": "$movie_info"},
            {"$project": {
                "_id": 0,
                "movie_id": {"$toString": "$_id"},
                "title": "$movie_info.title",
                "watch_count": 1
            }}
        ]

        results = list(watch_col.aggregate(pipeline))

        return {"top_k": top_k, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# python -m uvicorn appfinal:app --reload

