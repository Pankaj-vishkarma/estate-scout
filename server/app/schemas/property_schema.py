def property_serializer(property) -> dict:
    try:
        return {
            "id": str(property.get("_id", "")),
            "title": property.get("title") or "Untitled Property",
            "price": property.get("price") or "N/A",
            "address": property.get("address") or "Unknown Location",
            # ✅ Safe image fallback
            "image": property.get("image") or "/images/apartment1.jpg",
            # ✅ Safe street view fallback
            "street_view": property.get("street_view")
            or property.get("image")
            or "/images/apartment1.jpg",
        }

    except Exception as e:
        print(f"[Serializer ERROR]: {e}")

        return {
            "id": "",
            "title": "Property",
            "price": "N/A",
            "address": "Unknown",
            "image": "/images/apartment1.jpg",
            "street_view": "/images/apartment1.jpg",
        }
