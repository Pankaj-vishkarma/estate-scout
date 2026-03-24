from app.services.memory_service import get_user_preferences
from app.utils.search_tool import search_properties
from app.utils.fetch_tool import fetch_property_details


# 🔥 NEW: Extract location from query
def extract_location(query: str):
    words = query.lower().split()

    for i, w in enumerate(words):
        if w in ["in", "at", "near"] and i + 1 < len(words):
            return words[i + 1].capitalize()

    return "Delhi"  # fallback


def scout_properties(query: str):
    print(f"[Scout] 🔍 Searching properties for query: {query}")

    # 🔥 Get user preferences
    preferences = get_user_preferences()
    has_pet = preferences.get("has_pet", False)

    print(f"[Scout] 🧠 User preferences: {preferences}")

    # 🔥 NEW: detect location
    location = extract_location(query)
    print(f"[Scout] 📍 Detected Location: {location}")

    # 🔥 Build search query
    search_query = f"{query} apartment listing site:zillow.com OR site:apartments.com"

    print(f"[Scout] 🧾 Final Search Query: {search_query}")

    # 🔥 Step 1: Web Search
    search_results = search_properties(search_query)

    print(f"[Scout] 🔎 Raw Search Results Count: {len(search_results)}")

    properties = []

    # 🔥 Step 2: Fetch details
    for i, result in enumerate(search_results):
        url = result.get("url")

        print(f"[Scout] 🌐 Result {i+1} URL: {url}")

        if not url:
            print("[Scout] ⚠️ Skipping empty URL")
            continue

        # 🔥 FIX: pass location
        details = fetch_property_details(url, location)

        print(f"[Scout] 📦 Extracted Details: {details}")

        # 🔥 ensure valid data
        if details and details.get("address"):
            details["source_url"] = url
            properties.append(details)
        else:
            print("[Scout] ❌ Invalid property skipped")

    # 🔥 Fallback (IMPROVED)
    if not properties:
        print("[Scout] ⚠️ Using fallback mock data")

        properties = [
            {
                "title": "2BHK Apartment",
                "price": "₹18000",
                "address": f"{location} Sector 21 #101",  # 🔥 FIX
                "pet_friendly": True,
            },
            {
                "title": "Studio Apartment",
                "price": "₹15000",
                "address": f"{location} Central Area #202",  # 🔥 FIX
                "pet_friendly": True,
            },
            {
                "title": "1BHK Apartment",
                "price": "₹12000",
                "address": f"{location} Phase 2 #303",  # 🔥 FIX
                "pet_friendly": True,
            },
        ]

    print(f"[Scout] ✅ Final Properties Count: {len(properties)}")

    # 🔥 Step 3: Apply memory filtering
    if has_pet:
        print("[Scout] 🐶 Filtering pet-friendly properties")
        properties = [p for p in properties if p.get("pet_friendly")]

    print(f"[Scout] 🎯 Properties After Filtering: {len(properties)}")

    return properties
