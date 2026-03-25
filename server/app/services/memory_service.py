from app.config.db import users_collection
from bson import ObjectId


# ✅ SAVE USER PREFERENCES (USER-SPECIFIC)
def save_user_preference(message: str, user_id: str):
    try:
        if not user_id:
            print("⚠️ WARNING: user_id missing in save_user_preference")
            return

        preferences = {}
        msg = message.lower()

        if "dog" in msg or "pet" in msg:
            preferences["has_pet"] = True

        if preferences:
            users_collection.update_one(
                {"_id": ObjectId(user_id)},  # ✅ FIXED
                {"$set": preferences},
                upsert=False,  # ❌ don't create new user
            )

    except Exception as e:
        print(f"[Memory SAVE ERROR]: {e}")


# ✅ GET USER PREFERENCES (SAFE)
def get_user_preferences(user_id: str = None):
    try:
        if not user_id:
            print("⚠️ WARNING: user_id missing in get_user_preferences")
            return {}

        user = users_collection.find_one(
            {"_id": ObjectId(user_id)},  # ✅ FIXED
            {"password": 0},  # ✅ remove sensitive data
        )

        if not user:
            return {}

        # ✅ Return only relevant preferences
        return {"has_pet": user.get("has_pet", False)}

    except Exception as e:
        print(f"[Memory GET ERROR]: {e}")
        return {}
