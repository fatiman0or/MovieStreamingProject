# MovieStreamingProject
Movie streaming API project for Advance Database

## 📖 Overview  
This project simulates a **Movie Streaming Platform backend** using **Flask** and **MongoDB**.  
It provides an API to:  
- Manage users, movies, reviews, and watch history.  
- Perform a hybrid movie search combining similarity matching, ratings, and popularity.  
- Fetch user watch history and movie reviews dynamically from the database.  

The dataset is initialized in `main.py`, and the API logic runs in `appfinal.py`. 

## ⚙️ Required Installs / Setup Instructions
Before running the project, make sure you have the following installed:

### 🧩 1. Python
- **Version:** 3.8 or above  
- [Download Python](https://www.python.org/downloads/)

---

### 🧰 2. MongoDB
- Install and start **MongoDB Community Server**  
- [Download MongoDB](https://www.mongodb.com/try/download/community)
- Make sure your MongoDB service is running locally at: mongodb://localhost:27017/

---

### 📦 3. Required Python Libraries
Install all required dependencies using **pip**:
pip install flask pymongo bson

---

### 🚀 4. How to Run the Project
-Populate the MongoDB database by running:
python main.py 

-Start the Flask API server by running:
python appfinal.py

-Open your browser or API testing tool (like Postman) and go to:
http://127.0.0.1:5000/

-You should see the message:
🎬 **Movie Streaming API is running!**

The API is now live and ready for use. You can test routes such as:

-GET /users/<user_id>/history → **Fetch a user's watch history**

-GET /movies/<movie_id>/reviews → **Get reviews for a specific movie**

-GET /movies/search?query=<movie_name> → **Search for movies by title, director, or cast**

## 🧠 Technical Aspects

**Database:** MongoDB (NoSQL)

**Backend Framework:** Flask

**APIs:** RESTful APIs using Flask routes

**Data Handling:** PyMongo for MongoDB queries

**Similarity Algorithm:** SequenceMatcher from difflib for hybrid movie search

**Indexes:**

Text index on title, director, and cast.name in the Movies collection

Single-field index on movie_id in the WatchHistory collection

## 🗂️ Dataset

The dataset is manually initialized in main.py and consists of:

**Movies Collection:** 10 movies with genres, cast, directors, and ratings

**Users Collection:** 10 users with name, email, and subscription type

**Reviews Collection:** Reviews for each movie, linked by user and movie IDs

**WatchHistory Collection:** User watch history with timestamps and durations

## 🛠️ Tech Stack

| Component             | Technology Used               |
| --------------------- | ----------------------------- |
| **Language**          | Python                        |
| **Backend Framework** | Flask                         |
| **Database**          | MongoDB                       |
| **ORM / Driver**      | PyMongo                       |
| **Libraries**         | Flask, PyMongo, bson, difflib |
| **Environment**       | Localhost (127.0.0.1:5000)    |

## 👩‍💻 Author

Fatima Noor

COMSATS University — Advanced Database Project

