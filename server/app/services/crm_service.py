from app.config.db import properties_collection


def save_property(property):
    try:
        # 🔥 FIX: Check duplicate by address
        existing = properties_collection.find_one({"address": property.get("address")})

        if existing:
            print(f"[CRM] Duplicate skipped: {property.get('address')}")
            return

        # 🔥 Insert only if not duplicate
        properties_collection.insert_one(property)
        print(f"[CRM] Property saved: {property.get('address')}")

    except Exception as e:
        print(f"[CRM ERROR]: {e}")
