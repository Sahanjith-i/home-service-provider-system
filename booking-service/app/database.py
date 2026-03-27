import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
 
# Get absolute path to .env (one level up from app/)
env_path = Path(__file__).resolve().parent.parent / ".env"
 
# Debug print (optional)
print(f"Loading .env from: {env_path}")
 
# Load environment variables
load_dotenv(dotenv_path=env_path)
 
# Read values
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
 
# Debug prints (optional)
print(f"MONGODB_URL: {MONGODB_URL}")
print(f"DB_NAME: {DB_NAME}")
print(f"COLLECTION_NAME: {COLLECTION_NAME}")
 
try:
    # Connect to MongoDB
    client = MongoClient(MONGODB_URL)
 
    # Test connection
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")
 
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
 
    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
 
except Exception as e:
    print("❌ MongoDB connection failed!")
    print(e)