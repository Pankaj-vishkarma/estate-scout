from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import os


def take_screenshot(address: str, filename: str):
    options = webdriver.ChromeOptions()

    # 🔥 Headless (faster + no UI)
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    wait = WebDriverWait(driver, 10)

    try:
        print(f"[Browser] Opening map for: {address}")

        driver.get("http://localhost:3000/map-simulator")

        # 🔥 Wait for input field
        search_box = wait.until(EC.presence_of_element_located((By.ID, "search-box")))

        search_box.clear()
        search_box.send_keys(address)

        # 🔥 Wait for button
        search_btn = wait.until(EC.element_to_be_clickable((By.ID, "search-btn")))

        search_btn.click()

        # 🔥 Wait for image update
        image = wait.until(EC.presence_of_element_located((By.ID, "street-view-image")))

        time.sleep(1)  # small delay for render

        # 🔥 Create folder
        os.makedirs("data/screenshots", exist_ok=True)
        path = f"data/screenshots/{filename}"

        # 🔥 Take screenshot of ONLY image (important)
        image.screenshot(path)

        print(f"[Browser] Screenshot saved: {path}")

        return path

    except Exception as e:
        print(f"[Browser ERROR]: {e}")

        return "data/screenshots/fallback.png"

    finally:
        driver.quit()
