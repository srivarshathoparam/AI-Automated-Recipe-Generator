import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

# ✅ Load API key from .env
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

if not API_KEY:
    raise ValueError("API key is missing! Check your .env file.")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["recipe_db"]  # Replace with your actual DB name
recipes_collection = db["recipes"]

API_URL = f"https://api.spoonacular.com/recipes/random?number=10&apiKey={API_KEY}"

def fetch_recipe():
    response = requests.get(API_URL)
    if response.status_code != 200:
        print(f"Error fetching recipes: {response.status_code} - {response.text}")
        return

    data = response.json()

    for item in data.get("recipes", []):
        recipe = {
            "title": item["title"],
            "ingredients": [ing["name"] for ing in item.get("extendedIngredients", [])],
            "cuisine": item.get("cuisines", ["Unknown"])[0],
            "meal_type": item.get("dishTypes", ["Unknown"])[0],
            "difficulty": "Medium",
            "calories": item.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", 0),
            "prep_time": item.get("readyInMinutes", 0),
            "instructions": item.get("instructions", "No instructions available."),
            "popularity_score": 0
        }
        recipes_collection.insert_one(recipe)

    print("✅ Recipes fetched and stored successfully in MongoDB!")

if __name__ == "__main__":
    fetch_recipe()
