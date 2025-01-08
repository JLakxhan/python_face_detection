from pymongo import MongoClient

# Initialize MongoDB connection
MONGO_CLIENT = MongoClient("mongodb://localhost:27017/")
MONGO_DB = MONGO_CLIENT["mydatabase"]  # Replace 'mydatabase' with your DB name
MONGO_USER_COLLECTION = MONGO_DB["users"]
MONGO_SHIFT_COLLECTION = MONGO_DB["shift_predictions"]

