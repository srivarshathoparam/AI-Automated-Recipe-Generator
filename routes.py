from flask import Blueprint, request, render_template, jsonify
from flask import session, redirect, url_for
import openai
import json
from mongo_connection import db
import os
from mongo_connection import users_collection, recipes_collection, comments_collection
from bson.objectid import ObjectId
from flask import session 
from models import Recipe
from uuid import uuid4

# Initialize Blueprint for routes
recipe_routes = Blueprint("recipe_routes", __name__)
auth_routes = Blueprint("auth_routes", __name__)

# OpenAI API Key (Move to .env)
MONGO_URI = os.getenv("MONGO_URI")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get recipes collection from MongoDB
recipes_collection = db["recipes"]

# generate_recipe = {}

# ✅ ROUTES FOR HTML PAGES
@recipe_routes.route('/')
def homepage():
    return render_template('homepage.html')

@recipe_routes.route('/recipes')
def recipes():
    return render_template('rb.html')

@recipe_routes.route('/ingredients')
def ingredients():
    return render_template('ingredients.html')

# @auth_routes.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#         else:
#             return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415

#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         # TODO: Add validation, hashing, duplicate check

#         # Optional: Save to MongoDB
#         db["users"].insert_one({
#             "username": username,
#             "email": email,
#             "password": password  # ❗ Hash it in production
#         })

#         return jsonify({"message": "User registered successfully"}), 200

#     return render_template('register.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        users_collection = db["users"]
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return render_template("register.html", error="Email already exists")

        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": password  # 🔐 Hash later in production
        })

        session['user_id'] = str(result.inserted_id)  # ✅ Store user ID in session


        return redirect(url_for('recipe_routes.recipes'))

    return render_template('register.html')


@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')

        password = request.form.get('password')

        users_collection = db["users"]
        
        user = users_collection.find_one({"username": username})

        if not user or user["password"] != password:
            return render_template("login.html", error="Invalid email or password")

        session['user_id'] = str(user['_id'])  # ✅ Store user ID in session

        return redirect(url_for('recipe_routes.recipes'))  # ✅ Redirects to rb.html

    return render_template('login.html')

# from flask import Blueprint, render_template, redirect, url_for, session
# from bson.objectid import ObjectId
# from mongo_connection import users_collection, recipes_collection, comments_collection

# recipe_routes = Blueprint('recipe_routes', __name__)

@recipe_routes.route('/profile')
def profile():
    # # Check if user is logged in
    # if 'user_id' not in session:
    #     return redirect(url_for('auth_routes.login'))

    # user_id = session['user_id']
    # user = users_collection.find_one({'_id': ObjectId(user_id)})

    # if not user:
    #     return redirect(url_for('auth_routes.login'))

    # 🔧 TEMPORARY BYPASS: Use a dummy user ID from your database
    user_id = "67f41b8fa8f3f35938bba3e9"  # Replace this with an actual ObjectId from your MongoDB

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        return f"Error fetching dummy user: {e}"

    if not user:
        return "Dummy user not found. Please check the ObjectId."

    # Extracting user details
    username = user.get('username', 'Guest')
    allergies = ', '.join(user.get('allergies', []))
    favorite_ids = user.get('favorites', [])
    liked_ids = user.get('liked_recipes', [])

    # Get recipe documents for favorites and likes
    favorite_recipes = [r['name'] for r in recipes_collection.find({'_id': {'$in': [ObjectId(fid) for fid in favorite_ids]}})]
    liked_recipes = list(recipes_collection.find({'_id': {'$in': [ObjectId(lid) for lid in liked_ids]}}))

    # Get user's comments
    user_comments = list(comments_collection.find({'user_id': ObjectId(user_id)}))
    for comment in user_comments:
        recipe = recipes_collection.find_one({'_id': ObjectId(comment['recipe_id'])})
        comment['recipe_name'] = recipe['name'] if recipe else 'Unknown Recipe'

    return render_template(
        'profile.html',
        username=username,
        allergies=allergies,
        favorite_recipes=', '.join(favorite_recipes),
        liked_recipes=liked_recipes,
        user_comments=user_comments
    )

@auth_routes.route('/profile/edit', methods=['GET', 'PUT'])
def profile_edit():
    if request.method == 'GET':
        return render_template('profileEdit.html')  # render form for user to update

    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # update_data = {
    #     "username": data.get("username", user.get("username")),
    #     "feedbacks": data.get("feedbacks", ""),
    #     "allergies": data.get("allergies", "").split(","),
    #     "favoriteRecipes": data.get("favoriteRecipes", "").split(",")
    # }

    preferences_data = {
    "feedbacks": data.get("feedbacks", ""),
    "allergies": [a.strip() for a in data.get("allergies", "").split(",") if a.strip()],
    "favoriteRecipes": [f.strip() for f in data.get("favoriteRecipes", "").split(",") if f.strip()]
    }

    update_data = {
        "username": data.get("username", user.get("username")),
        "preferences": preferences_data
    }


    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    return jsonify({"message": "Profile updated successfully"})

@recipe_routes.route('/carbonara')
def carbonara_recipe():
    return render_template('carbonara.html')

@recipe_routes.route('/chicken')
def chicken_recipe():
    return render_template('chicken_curry.html')

@recipe_routes.route('/stirfry')
def stirfry_recipe():
    return render_template('chicken_stirfry.html')

@recipe_routes.route('/chocolatelavacake')
def chocolatelavacake_recipe():
    return render_template('chocolate_lava_cake.html')

@recipe_routes.route('/caesarSalad')
def caesarSalad_recipe():
    return render_template('caesar_salad.html')

@recipe_routes.route("/search", methods=["GET"])
def search_recipe():
    title = request.args.get("q", "").strip()  # Matches frontend ?q= usage

    if not title:
        return jsonify({"found": False, "recipes": []}), 400

    # Search MongoDB
    recipes = recipes_collection.find(
        {"title": {"$regex": title, "$options": "i"}},
        {"_id": 0}
    )

    results = list(recipes)

    if results:
        return jsonify({"found": True, "recipes": results})

    # Not found
    return jsonify({"found": False, "recipes": []}), 200  # Not 404


# At top (after imports)
@recipe_routes.route("/api/generate-recipe", methods=["POST"])
def generate_recipe(ingredients=None, preferences=""):
    """Helper function to generate a recipe using OpenAI."""
    if ingredients is None:
        ingredients = []

    ingredient_str = ', '.join(ingredients) if ingredients else "any ingredients you like"

    prompt = f"""
    You are an expert chef. Create a unique, delicious recipe using these ingredients: {ingredient_str}.
    Preferences (if any): {preferences}.
    Respond ONLY in the following JSON format:
    {{
        "name": "Recipe Name",
        "description": "Short description",
        "ingredients": ["list", "of", "ingredients"],
        "instructions": ["Step 1", "Step 2"]
    }}
    """

    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700
        )
        content = response["choices"][0]["message"]["content"]

        recipe = json.loads(content)
        return recipe  # 🔥 return parsed recipe dict
    except Exception as e:
        print(f"OpenAI error: {e}")
        return None

# ✅ AI RECIPE GENERATION
@recipe_routes.route("/api/generate-recipe", methods=["POST"])
def generate_ai_recipe():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    preferences = data.get("preferences", "")

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Ingredients must be a non-empty list"}), 400

    recipe = generate_recipe(ingredients, preferences)

    if recipe:
        recipe["id"] = "ai_" + "_".join(ingredients)
        return jsonify({"recipe": recipe})
    else:
        return jsonify({"error": "Failed to generate recipe"}), 500
    
@recipe_routes.route('/recipe/preview', methods=['GET'])
def recipe_preview():
    recipe = generate_recipe()  # No ingredients passed

    if not recipe:
        return "Error generating recipe", 500

    # Build recipe dict
    generated_recipe = {
        'title': recipe.get('name', 'Generated Recipe'),
        'ingredients': recipe.get('ingredients', ["Ingredients not specified"]),
        'instructions': " ".join(recipe.get('instructions', ["Instructions not available"]))
    }

    return render_template('recipe_template.html', recipe=generated_recipe)

    
@recipe_routes.route('/recipe/<slug>')
def recipe_detail(slug):
    recipe = generate_ai_recipe.get(slug)

    if not recipe:
        # Try fetching the recipe from MongoDB if not found in the generated_recipes
        recipe = recipes_collection.find_one({"slug": slug})

        if not recipe:
            return "Recipe not found", 404

    return render_template('recipe_template.html', recipe=recipe)


# @recipe_routes.route('/recipe/<recipe_name>')
# def recipe_detail(recipe_name):
#     # Convert hyphenated URL to proper title format
#     title = recipe_name.replace('-', ' ').title()

#     # Ideally this would query a DB or AI model to get the full recipe details
#     recipe_data = generate_recipe_page_data(title)  # Call your AI generator

#     if not recipe_data:
#         return "Recipe not found", 404

#     return render_template('recipe_template.html', recipe=recipe_data)

@recipe_routes.route('/store_recipes', methods=['POST'])
def store_recipes():
    data = request.get_json()
    for recipe in data:
        slug = recipe['slug']
        generated_recipes[slug] = recipe
    return jsonify({'status': 'success'})

@recipe_routes.route('/cuisine/italian')
def italian_cuisine():
    return render_template('italian.html')

@recipe_routes.route('/cuisine/mexican')
def mexican_cuisine():
    return render_template('mexican.html')

@recipe_routes.route('/cuisine/indian')
def indian_cuisine():
    return render_template('indian.html')

@recipe_routes.route('/cuisine/japanese')
def japanese_cuisine():
    return render_template('japanese.html')

@recipe_routes.route('/cuisine/french')
def french_cuisine():
    return render_template('french.html')

@recipe_routes.route('/cuisine/chinese')
def chinese_cuisine():
    return render_template('chinese.html')

@recipe_routes.route('/meal/breakfast')
def breakfast():
    return render_template('breakfast.html')

@recipe_routes.route('/meal/lunch')
def lunch():
    return render_template('lunch.html')

@recipe_routes.route('/meal/dinner')
def dinner():
    return render_template('dinner.html')

@recipe_routes.route('/meal/desserts')
def desserts():
    return render_template('desserts.html')

@recipe_routes.route('/meal/brunch')
def brunch():
    return render_template('brunch.html')

@recipe_routes.route('/meal/snacks')
def snacks():
    return render_template('snacks.html')