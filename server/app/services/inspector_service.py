from app.utils.browser_tool import take_screenshot


def inspect_property(address: str, index: int):
    try:
        # 🔥 Safe filename
        safe_address = address.replace(" ", "_").replace(",", "")
        filename = f"{safe_address}_{index}.png"

        print(f"[Inspector] Processing property: {address}")

        # 🔥 Take screenshot using Selenium
        screenshot_path = take_screenshot(address, filename)

        print(f"[Inspector] Screenshot saved at: {screenshot_path}")

        return screenshot_path

    except Exception as e:
        print(f"[Inspector ERROR]: {e}")

        # 🔥 fallback image (frontend will handle this)
        return "data/screenshots/fallback.png"
