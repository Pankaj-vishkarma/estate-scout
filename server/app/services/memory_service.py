from app.config.db import users_collection


def save_user_preference(message: str):
    preferences = {}

    msg = message.lower()

    if "dog" in msg or "pet" in msg:
        preferences["has_pet"] = True

    if preferences:
        users_collection.update_one(
            {"user_id": "default_user"}, {"$set": preferences}, upsert=True
        )


def get_user_preferences():
    user = users_collection.find_one({"user_id": "default_user"})

    if not user:
        return {}

    return user
