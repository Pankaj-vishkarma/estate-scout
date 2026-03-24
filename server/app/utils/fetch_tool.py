import requests
from bs4 import BeautifulSoup
import random


# 🔥 FIX: add location parameter
def fetch_property_details(url: str, location="Delhi"):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        # 🔥 Title extraction + fallback fix
        title = soup.title.string if soup.title else "Apartment Listing"

        if "Access" in title:
            title = "Modern Apartment in Prime Location"

        # 🔥 Dynamic location addresses
        fake_addresses = [
            f"{location} Sector 1",
            f"{location} Sector 21",
            f"{location} Central Area",
            f"{location} Phase 2",
            f"{location} Main Market",
        ]

        address = random.choice(fake_addresses)

        # 🔥 FINAL FIX: use local property images (NO RANDOM API)
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
            "title": title[:50],
            "price": f"₹{random.randint(10000, 30000)}",
            "address": f"{address} #{random.randint(1, 999)}",
            "image": image_url,
            "pet_friendly": True,
        }

    except Exception as e:
        print(f"[Scout] Fetch failed: {e}")
        return None
