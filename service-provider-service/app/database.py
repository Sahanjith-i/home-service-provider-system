import os
from pathlib import Path
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv

#absolute path to .env - one level up from app/
env_path = Path(__file__).resolve().parent.parent / ".env"


print(f"Loading .env from: {env_path}")

#Loading environment variables
load_dotenv(dotenv_path=env_path)

#Reading values
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


print(f"MONGODB_URL: {MONGODB_URL}")
print(f"DB_NAME: {DB_NAME}")
print(f"COLLECTION_NAME: {COLLECTION_NAME}")

try:
    #Connect to MongoDB
    client = MongoClient(MONGODB_URL)

    #Test the connection
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")

    #Database and collections
    db = client[DB_NAME]
    provider_collection = db[COLLECTION_NAME]
    counter_collection = db["counters"]

    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print("Counter collection: counters")

    #Auto-increment id
    def get_next_provider_id():
        counter = counter_collection.find_one_and_update(
            {"_id": "provider_id"},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return counter["sequence_value"]

except Exception as e:
    print("❌ MongoDB connection failed!")
    print(e)

    # fallback to avoid crashes in imports
    provider_collection = None
    counter_collection = None

    def get_next_provider_id():
        return None