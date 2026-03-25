import os
from dotenv import load_dotenv

load_dotenv()

# 🔐 DATABASE
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# 🤖 AI
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 🌐 MAP + SELENIUM
MAP_SIMULATOR_URL = os.getenv("MAP_SIMULATOR_URL")
WINDOW_SIZE = os.getenv("SELENIUM_WINDOW_SIZE", "1920,1080")
WAIT_TIME = int(os.getenv("SELENIUM_WAIT_TIME", 15))
FALLBACK_IMAGE = os.getenv("FALLBACK_IMAGE_PATH")

# ⚙️ OPTIONAL
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
