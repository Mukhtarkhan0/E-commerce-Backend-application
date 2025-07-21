from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["ecommerce"]
products_collection = db["products"]
orders_collection = db["orders"]

# Create indexes
products_collection.create_index([("name", "text")])
products_collection.create_index([("price", 1)])
orders_collection.create_index([("userId", 1)])
