import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://sweetieheart313:palakpaneer@recipegenerator.0ezzpvy.mongodb.net/?retryWrites=true&w=majority&appName=recipeGenerator")
db = client["recipe_db"]
collection = db["recipes"]

# Load the dataset
df = pd.read_csv(r"D:\IOMP-B11\backend\dataset\full_dataset.csv", chunksize=10000)

count = 0  # Track inserted records
LIMIT = 550000  # Set a limit

for chunk in df:
    if count >= LIMIT:
        print("✅ Insert limit reached. Stopping import.")
        break  # Stop further insertions

    batch = chunk.to_dict(orient="records")
    collection.insert_many(batch)
    
    count += len(batch)
    print(f"✅ Inserted {count} records...")

print("✅ Import process completed.")
