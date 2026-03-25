import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ❗ Validate API key early
if not TAVILY_API_KEY:
    print("[Scout] ❌ Tavily API key missing")


def search_properties(query: str):
    url = "https://api.tavily.com/search"

    if not query or not query.strip():
        return []

    if not TAVILY_API_KEY:
        return []

    payload = {
        "query": query.strip(),
        "search_depth": "basic",
        "max_results": 3,
    }

    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}

    retries = 2  # ✅ retry mechanism

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=10  # ✅ safer timeout
            )

            if response.status_code != 200:
                print(f"[Scout] API failed (attempt {attempt+1})")
                time.sleep(1)
                continue

            data = response.json()

            results = data.get("results", [])

            if not isinstance(results, list):
                return []

            # ✅ Clean result format
            cleaned_results = [
                {
                    "url": r.get("url"),
                    "title": r.get("title"),
                    "content": r.get("content"),
                }
                for r in results
                if r.get("url")
            ]

            return cleaned_results

        except requests.exceptions.Timeout:
            print(f"[Scout] Timeout (attempt {attempt+1})")
            time.sleep(1)

        except Exception as e:
            print(f"[Scout] Error: {e}")
            break

    # ❌ fallback
    return []
