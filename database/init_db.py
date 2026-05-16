import json
from pymongo import MongoClient

# Connect to MongoDB (container service name is mongo_db in docker-compose.yml)
client = MongoClient("mongodb://mongo_db:27017/")
db = client["dealershipsDB"]

# Load dealers.json
with open("dealers.json") as f:
    dealers = json.load(f)
    db.dealerships.delete_many({})
    db.dealerships.insert_many(dealers)
    print(f"Inserted {len(dealers)} dealers")

# Load reviews.json
with open("reviews.json") as f:
    reviews = json.load(f)
    db.reviews.delete_many({})
    db.reviews.insert_many(reviews)
    print(f"Inserted {len(reviews)} reviews")
