def property_serializer(property) -> dict:
    return {
        "id": str(property["_id"]),
        "title": property["title"],
        "price": property["price"],
        "address": property["address"],
        "image": property["image"],
    }
