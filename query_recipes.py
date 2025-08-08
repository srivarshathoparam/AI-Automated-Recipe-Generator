from mongo_connection import collection

# Fetch 5 random recipes
recipes = collection.aggregate([{"$sample": {"size": 5}}])
for recipe in recipes:
    print(recipe["title"])
