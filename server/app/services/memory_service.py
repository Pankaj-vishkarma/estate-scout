from app.config.db import users_collection


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
                {"user_id": user_id},  # ✅ USER-SPECIFIC
                {"$set": preferences},
                upsert=True,
            )

    except Exception as e:
        print(f"[Memory SAVE ERROR]: {e}")


# ✅ GET USER PREFERENCES (SAFE + USER-SPECIFIC)
def get_user_preferences(user_id: str = None):  # 🔥 FIX: optional param
    try:
        print("🔥 get_user_preferences CALLED WITH:", user_id)

        # 🔥 SAFETY: avoid crash if called बिना user_id
        if not user_id:
            print("⚠️ WARNING: user_id missing in get_user_preferences")
            return {}

        user = users_collection.find_one({"user_id": user_id})

        if not user:
            return {}

        return user

    except Exception as e:
        print(f"[Memory GET ERROR]: {e}")
        return {}
