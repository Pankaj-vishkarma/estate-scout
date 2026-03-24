import requests
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

print("[DEBUG] Tavily API Key Loaded:", "YES" if TAVILY_API_KEY else "NO")


def search_properties(query: str):
    url = "https://api.tavily.com/search"

    print(f"[Scout] 🔍 Search Query: {query}")

    if not TAVILY_API_KEY:
        print("[Scout] ❌ ERROR: Tavily API key missing in .env")
        return []

    payload = {"query": query, "search_depth": "basic", "max_results": 3}

    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}

    try:
        print("[Scout] 🚀 Sending request to Tavily API...")

        response = requests.post(url, json=payload, headers=headers, timeout=5)

        print(f"[Scout] 📡 Status Code: {response.status_code}")

        # 🔥 Print raw response (IMPORTANT)
        print("[Scout] 📦 Raw Response:", response.text[:500])

        if response.status_code != 200:
            print(f"[Scout] ❌ Search API failed: {response.text}")
            return []

        results = response.json().get("results", [])

        print(f"[Scout] ✅ Results Found: {len(results)}")

        # 🔥 Print URLs
        for i, r in enumerate(results):
            print(f"[Scout] Result {i+1}: {r.get('url')}")

        return results

    except Exception as e:
        print(f"[Scout] ❌ Search error: {e}")
        return []
