from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


# ✅ Validate ENV (CRASH EARLY)
if not MONGO_URI or not DB_NAME:
    raise ValueError("Missing MONGO_URI or DB_NAME in environment variables")


try:
    # ✅ Optimized Mongo Client
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,  # ⏱️ fail fast
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=50,  # ⚡ performance
    )

    # ✅ Force connection check
    client.admin.command("ping")

    print("✅ MongoDB connected successfully")

except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise


# ✅ DB reference
db = client[DB_NAME]

# ✅ Collections
properties_collection = db["properties"]
users_collection = db["users"]
