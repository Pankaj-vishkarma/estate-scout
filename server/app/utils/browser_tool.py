from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import os


def run_browser_action(action: str, value: str = "", filename: str = "output.png"):
    options = webdriver.ChromeOptions()

    # 🔥 Headless mode
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    wait = WebDriverWait(driver, 10)

    try:
        print(f"[Browser] Action: {action} | Value: {value}")

        driver.get("http://localhost:3000/map-simulator")

        # 🔥 TYPE action
        if action in ["type", "search_and_capture"]:
            search_box = wait.until(
                EC.presence_of_element_located((By.ID, "search-box"))
            )
            search_box.clear()
            search_box.send_keys(value)

        # 🔥 CLICK action
        if action in ["click", "search_and_capture"]:
            search_btn = wait.until(EC.element_to_be_clickable((By.ID, "search-btn")))
            search_btn.click()

        # 🔥 SCREENSHOT action
        if action in ["screenshot", "search_and_capture"]:
            image = wait.until(
                EC.presence_of_element_located((By.ID, "street-view-image"))
            )

            time.sleep(1)

            os.makedirs("data/screenshots", exist_ok=True)
            path = f"data/screenshots/{filename}"

            image.screenshot(path)

            print(f"[Browser] Screenshot saved: {path}")

            return path

        return None

    except Exception as e:
        print(f"[Browser ERROR]: {e}")
        return "data/screenshots/fallback.png"

    finally:
        driver.quit()
