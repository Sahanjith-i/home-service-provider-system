import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# If MONGODB_URL doesn't contain encoded credentials, encode them
# This handles cases where special characters in password aren't pre-encoded
if MONGODB_URL and "mongodb+srv://" in MONGODB_URL:
    try:
        # Try to connect directly first
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.server_info()  # Verify connection works
    except Exception as e:
        if "Username and password must be escaped" in str(e):
            # Extract and re-encode the credentials
            if "@" in MONGODB_URL:
                # Split at mongodb+srv://
                prefix = MONGODB_URL.split("://")[0] + "://"
                rest = MONGODB_URL.split("://", 1)[1]
                
                # Split credentials from host
                credentials, host_part = rest.rsplit("@", 1)
                username, password = credentials.split(":", 1)
                
                # Encode credentials
                encoded_username = quote_plus(username)
                encoded_password = quote_plus(password)
                
                # Rebuild URL
                MONGODB_URL = f"{prefix}{encoded_username}:{encoded_password}@{host_part}"
                client = MongoClient(MONGODB_URL)
        else:
            raise
else:
    # If already provided as encoded or local connection
    client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
customers_collection = db[COLLECTION_NAME]

# Create indexes for better query performance
customers_collection.create_index("email", unique=True)
customers_collection.create_index("customer_id")


def get_database():
    """Get database instance"""
    return db


def get_customers_collection():
    """Get customers collection"""
    return customers_collection


def convert_object_id(data):
    """Convert ObjectId to string for JSON serialization"""
    if isinstance(data, list):
        return [convert_object_id(item) for item in data]
    elif isinstance(data, dict):
        data_copy = data.copy()
        if "_id" in data_copy:
            data_copy["_id"] = str(data_copy["_id"])
        return data_copy
    return data


def create_customer_id():
    """Generate a new customer ID"""
    count = customers_collection.count_documents({})
    return f"CUST{str(count + 1).zfill(6)}"
