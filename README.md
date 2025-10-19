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
-pip install flask pymongo bson

## How to Run the Project
-Populate the MongoDB database by running: python main.py.

