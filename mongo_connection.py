import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in .env file!")

# Function to get database connection
def get_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client["recipe_db"]  # Change this to your actual database name
        print("Connected to MongoDB Atlas successfully!")

        
        return db
    
    except Exception as e:
        print(" MongoDB Connection Failed:", e)
        return None

# Initialize database connection
db = get_database()

# Check if database connection is valid
if db is None:
    raise ConnectionError("Failed to connect to MongoDB. Check your MONGO_URI!")

# Define and export collections
users_collection = db["users"]
recipes_collection = db["recipes"]
comments_collection = db["comments"]
