from mongo_connection import db
from bson import ObjectId
from transformers import pipeline

# Load AI model (pre-trained GPT-based model)
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=-1)  # -1 means CPU

# User Model for MongoDB
class User:
    def __init__(self, username, dietary_restrictions=None, allergies=None, liked_recipes=None, 
                 recently_viewed=None, preferred_cuisines=None, disliked_ingredients=None, 
                 cooking_skill_level=None, feedbacks=None, favorite_recipes=None):
        self.username = username
        self.dietary_restrictions = dietary_restrictions
        self.allergies = allergies
        self.liked_recipes = liked_recipes if liked_recipes else []
        self.recently_viewed = recently_viewed if recently_viewed else []
        self.preferred_cuisines = preferred_cuisines
        self.disliked_ingredients = disliked_ingredients
        self.cooking_skill_level = cooking_skill_level
        self.feedbacks = feedbacks
        self.favorite_recipes = favorite_recipes

    def save(self):
        users_collection = db['users']
        result = users_collection.insert_one(self.__dict__)  # Save user document to MongoDB
        return str(result.inserted_id)  # Return the inserted ID as a string

    @staticmethod
    def get(user_id):
        users_collection = db['users']
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            # Convert ObjectId to string
            user["_id"] = str(user["_id"])
        return user

# Recipe Model for MongoDB
class Recipe:
    def __init__(self, title, ingredients, cuisine, meal_type, difficulty, calories, prep_time, instructions, popularity_score):
        self.title = title
        self.ingredients = ingredients
        self.cuisine = cuisine
        self.meal_type = meal_type
        self.difficulty = difficulty
        self.calories = calories
        self.prep_time = prep_time
        self.instructions = instructions
        self.popularity_score = popularity_score

    def save(self):
        recipes_collection = db['recipes']
        result = recipes_collection.insert_one(self.__dict__)  # Save recipe document to MongoDB
        return str(result.inserted_id)  # Return the inserted ID as a string

    @staticmethod
    def get(recipe_id):
        recipes_collection = db['recipes']
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe:
            # Convert ObjectId to string
            recipe["_id"] = str(recipe["_id"])
        return recipe

# AI Recipe Generation
def generate_recipe(ingredients, preferences):
    prompt = f"Create a recipe using {', '.join(ingredients)}."
    
    if preferences:
        prompt += f" Consider user preferences: {preferences}."

    response = generator(prompt, max_length=200, do_sample=True)
    return response[0]['generated_text']
