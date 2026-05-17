import json
from pymongo import MongoClient

# ✅ Connect to MongoDB via localhost (since you're running from host)
client = MongoClient("mongodb://localhost:27017/")

# ✅ Select database
db = client["dealershipsDB"]

# ✅ Clear existing collections
db.dealerships.delete_many({})
db.reviews.delete_many({})

# ✅ Load dealers.json
with open("dealers.json") as f:
    dealers_data = json.load(f)
db.dealerships.insert_many(dealers_data)

# ✅ Load reviews.json
with open("reviews.json") as f:
    reviews_data = json.load(f)
db.reviews.insert_many(reviews_data)

print("Database seeded successfully!")
