from app.services.memory_service import get_user_preferences


def scout_properties(query: str):
    print(f"[Scout] Searching properties for query: {query}")

    # 🔥 Get user preferences (memory)
    preferences = get_user_preferences()

    has_pet = preferences.get("has_pet", False)

    print(f"[Scout] User preferences: {preferences}")

    # 🔥 Base mock data
    properties = [
        {
            "title": "2BHK Apartment",
            "price": "$2000",
            "address": "123 Main St",
            "pet_friendly": True,
        },
        {
            "title": "Studio Apartment",
            "price": "$1500",
            "address": "456 Park Ave",
            "pet_friendly": False,
        },
    ]

    # 🔥 Apply memory-based filtering
    if has_pet:
        print("[Scout] Filtering pet-friendly properties")

        properties = [p for p in properties if p.get("pet_friendly")]

    return properties
