def property_serializer(property) -> dict:
    return {
        "id": str(property["_id"]),
        "title": property.get("title"),
        "price": property.get("price"),
        "address": property.get("address"),
        # 🔥 SAFE IMAGE (IMPORTANT)
        "image": property.get("image"),
        # 🔥 NEW FIELD (VERY IMPORTANT)
        "street_view": property.get("street_view"),
    }
