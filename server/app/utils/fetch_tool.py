import requests
from bs4 import BeautifulSoup
import random


def fetch_property_details(url: str, location="Delhi"):
    try:
        if not url:
            return None

        # ✅ safer request
        res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

        # ❌ skip bad responses
        if res.status_code != 200:
            print(f"[Fetch] Failed URL ({res.status_code}): {url}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ Safe title extraction
        title = "Apartment Listing"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        # fallback for blocked pages
        if "Access" in title or not title:
            title = "Modern Apartment in Prime Location"

        # ✅ deterministic seed (IMPORTANT for AI consistency)
        seed = sum(ord(c) for c in url)
        random.seed(seed)

        # 🔥 Dynamic location-based addresses
        fake_addresses = [
            f"{location} Sector 1",
            f"{location} Sector 21",
            f"{location} Central Area",
            f"{location} Phase 2",
            f"{location} Main Market",
        ]

        address = random.choice(fake_addresses)

        # 🔥 local images (deterministic)
        property_images = [
            "/images/apartment1.jpg",
            "/images/apartment2.jpg",
            "/images/apartment3.jpg",
            "/images/apartment4.jpg",
            "/images/apartment5.jpg",
            "/images/apartment6.jpg",
            "/images/apartment7.jpg",
            "/images/apartment8.jpg",
            "/images/apartment9.jpg",
            "/images/apartment10.jpg",
            "/images/apartment11.jpg",
            "/images/apartment12.jpg",
            "/images/apartment13.jpg",
        ]

        image_url = random.choice(property_images)

        return {
            "title": title[:60],
            "price": f"₹{random.randint(10000, 30000)}",
            "address": f"{address} #{random.randint(1, 999)}",
            "image": image_url,
            "pet_friendly": True,
        }

    except requests.exceptions.Timeout:
        print(f"[Fetch] Timeout: {url}")
        return None

    except Exception as e:
        print(f"[Fetch ERROR]: {e}")
        return None
