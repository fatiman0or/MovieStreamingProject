# Movie Streaming Database Project

This is a backend simulation of a **Movie Streaming Platform** built with **FastAPI** and **MongoDB**.  
This project was developed as part of the **Advanced Database** course.

---

## Overview

This API simulates the backend of a **movie streaming service**, allowing users to:

-  Manage movies, users, reviews, and watch history.  
- Perform **keyword-based** and **hybrid (semantic + keyword)** movie searches.  
- Retrieve reviews and ratings for any movie.  
- View user-specific watch histories.  
- Fetch **top-watched movies** from recent activity (last 30 days).  

The data is initialized using Python scripts that populate MongoDB with realistic sample datasets.

---

## Setup & Installation

###  1. Prerequisites
Make sure you have the following installed:

- **Python 3.8+** → [Download Here](https://www.python.org/downloads/)  
- **MongoDB Community Server** → [Download Here](https://www.mongodb.com/try/download/community)

> Ensure your MongoDB service is running locally at:  
> **mongodb://localhost:27017/**

---

###  2. Install Required Dependencies
Open your terminal and install dependencies via pip:

pip install fastapi pymongo bson uvicorn

---

###  3. Database Initialization

Run these scripts in order to populate your MongoDB database with initial and extended datasets:

python main.py
python add_more_data.py
python more_watch_history2.py

**main.py** → creates the core collections (Movies, Users, Reviews, WatchHistory).
**add_more_data.py** → adds more movies, users, and reviews.
**more_watch_history2.py** → generates additional watch history and simulates recent trending movies

---

### 4. Run the API Server

Start the FastAPI server locally using Uvicorn:

**python -m uvicorn appfinal:app --reload**


Once the server starts, open your browser or Postman and visit:

http://127.0.0.1:8000


You should see the message:

**🎬 Movie Streaming API is running!**

---

### 🧠 Core Features
**1. Movie Management**

View and search all movies in the database.

Text search by title, director, or cast name.

**2. Hybrid Search System**

Combines semantic similarity (via SequenceMatcher) and text indexing results.

Uses Reciprocal Rank Fusion (RRF) for combined ranking, giving smarter search results.

**3. Movie Reviews**

Retrieve all reviews for a specific movie.

Each review includes the user name, rating, and review text.

**4. User Watch History**

Fetch full watch history for any user by ID.

Each record shows movie details, duration watched, and timestamp.

**5. Top Watched Movies**

Dynamically identifies and returns the most-watched movies from the last 30 days.

---

## API Endpoints

| **Method** | **Endpoint** | **Description** |
|-------------|--------------|-----------------|
| **GET** | `/` | Root route — confirms the API is running |
| **GET** | `/movies/search/keyword?query=<term>` | Search movies by keyword (title, director, or cast) |
| **GET** | `/movies/search/hybrid?query=<term>` | Perform hybrid (semantic + keyword) search |
| **GET** | `/movies/{movie_id}/reviews` | Fetch all reviews for a specific movie |
| **GET** | `/users/{user_id}/history` | Fetch the watch history of a specific user |
| **GET** | `/movies/top-watched` | Retrieve top-watched movies from the last 30 days |


