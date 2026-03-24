from app.config.db import properties_collection
from datetime import datetime


def save_property(property):
    try:
        address = property.get("address")

        # 🔥 Duplicate check
        existing = properties_collection.find_one({"address": address})

        if existing:
            print(f"[CRM] Duplicate skipped: {address}")
            return

        # 🔥 Structured document (IMPORTANT)
        property_doc = {
            "title": property.get("title"),
            "price": property.get("price"),
            "address": address,
            "image": property.get("image"),  # screenshot path
            "folder": property.get("folder"),  # 🔥 MUST HAVE
            "created_at": datetime.utcnow(),
        }

        properties_collection.insert_one(property_doc)

        print(f"[CRM] Property saved: {address}")

    except Exception as e:
        print(f"[CRM ERROR]: {e}")
