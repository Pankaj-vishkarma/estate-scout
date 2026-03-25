from app.utils.search_tool import search_properties
from app.utils.fetch_tool import fetch_property_details


# 🔥 Extract location from query
def extract_location(query: str):
    words = query.lower().split()

    for i, w in enumerate(words):
        if w in ["in", "at", "near"] and i + 1 < len(words):
            return words[i + 1].capitalize()

    return "Delhi"  # fallback


# 🔥 UPDATED FUNCTION (IMPORTANT FIX)
def scout_properties(query: str, preferences: dict = {}):
    print(f"[Scout] 🔍 Searching properties for query: {query}")

    # ✅ Use passed preferences (NO DB CALL HERE)
    has_pet = preferences.get("has_pet", False)

    print(f"[Scout] 🧠 User preferences: {preferences}")

    # 🔥 Detect location
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

        details = fetch_property_details(url, location)
        print(f"[Scout] 📦 Extracted Details: {details}")

        if details and details.get("address"):
            details["source_url"] = url
            properties.append(details)
        else:
            print("[Scout] ❌ Invalid property skipped")

    # 🔥 Fallback
    if not properties:
        print("[Scout] ⚠️ Using fallback mock data")

        properties = [
            {
                "title": "2BHK Apartment",
                "price": "₹18000",
                "address": f"{location} Sector 21 #101",
                "pet_friendly": True,
            },
            {
                "title": "Studio Apartment",
                "price": "₹15000",
                "address": f"{location} Central Area #202",
                "pet_friendly": True,
            },
            {
                "title": "1BHK Apartment",
                "price": "₹12000",
                "address": f"{location} Phase 2 #303",
                "pet_friendly": True,
            },
        ]

    print(f"[Scout] ✅ Final Properties Count: {len(properties)}")

    # 🔥 Apply memory filtering
    if has_pet:
        print("[Scout] 🐶 Filtering pet-friendly properties")
        properties = [p for p in properties if p.get("pet_friendly")]

    print(f"[Scout] 🎯 Properties After Filtering: {len(properties)}")

    return properties
