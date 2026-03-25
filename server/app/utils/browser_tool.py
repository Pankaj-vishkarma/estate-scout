from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import os
from dotenv import load_dotenv

load_dotenv()

MAP_SIMULATOR_URL = os.getenv(
    "MAP_SIMULATOR_URL", "http://localhost:3000/map-simulator"
)
FALLBACK_IMAGE = os.getenv("FALLBACK_IMAGE_PATH", "data/screenshots/fallback.png")


def run_browser_action(action: str, value: str = "", filename: str = "output.png"):
    options = webdriver.ChromeOptions()

    # 🔥 Production-safe Chrome options
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    wait = WebDriverWait(driver, 15)

    try:
        print(f"[Browser] Action: {action}")

        # ✅ Use ENV URL
        driver.get(MAP_SIMULATOR_URL)

        # 🔥 TYPE
        if action in ["type", "search_and_capture"]:
            search_box = wait.until(
                EC.presence_of_element_located((By.ID, "search-box"))
            )
            search_box.clear()
            search_box.send_keys(value)

        # 🔥 CLICK
        if action in ["click", "search_and_capture"]:
            search_btn = wait.until(EC.element_to_be_clickable((By.ID, "search-btn")))
            search_btn.click()

        # 🔥 WAIT FOR IMAGE LOAD (BETTER THAN sleep)
        if action in ["screenshot", "search_and_capture"]:
            image = wait.until(
                EC.presence_of_element_located((By.ID, "street-view-image"))
            )

            # ✅ Wait until image loaded
            wait.until(lambda d: image.get_attribute("data-loaded") == "true")

            os.makedirs("data/screenshots", exist_ok=True)

            # ✅ Safe filename handling
            filename = os.path.basename(filename)
            path = os.path.join("data", "screenshots", filename)

            image.screenshot(path)

            print(f"[Browser] Screenshot saved: {path}")

            return path.replace("\\", "/")

        return None

    except Exception as e:
        print(f"[Browser ERROR]: {e}")

        # ✅ Ensure fallback exists
        os.makedirs("data/screenshots", exist_ok=True)
        if not os.path.exists(FALLBACK_IMAGE):
            with open(FALLBACK_IMAGE, "wb") as f:
                f.write(b"")

        return FALLBACK_IMAGE

    finally:
        driver.quit()
