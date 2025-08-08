import pandas as pd
from mongo_connection import collection  # Import MongoDB connection

# Load CSV
csv_file = "dataset\full_dataset.csv"  # Ensure this file is in the correct directory
df = pd.read_csv(csv_file)

# Convert DataFrame to JSON and insert into MongoDB
json_data = df.to_dict(orient="records")  
collection.insert_many(json_data)  

print(f"Inserted {len(json_data)} recipes into MongoDB successfully!")
