from app.config.db import properties_collection
from datetime import datetime


# 🔥 UPDATED FUNCTION
def save_property(property, user_id):
    try:
        address = property.get("address")

        # ✅ User-specific duplicate check
        existing = properties_collection.find_one(
            {"address": address, "user_id": user_id}
        )

        if existing:
            print(f"[CRM] Duplicate skipped: {address}")
            return

        # 🔥 Structured document (UPDATED)
        property_doc = {
            "title": property.get("title"),
            "price": property.get("price"),
            "address": address,
            "image": property.get("street_view"),  # ✅ FIXED
            "folder": property.get("folder"),
            "user_id": user_id,  # ✅ IMPORTANT
            "created_at": datetime.utcnow(),
        }

        properties_collection.insert_one(property_doc)

        print(f"[CRM] Property saved for user {user_id}: {address}")

    except Exception as e:
        print(f"[CRM ERROR]: {e}")
