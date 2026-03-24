from app.utils.browser_tool import run_browser_action


def inspect_property(address: str, index: int):
    try:
        print(f"[Inspector] Processing property: {address}")

        # 🔥 Safe filename
        safe_address = address.replace(" ", "_").replace(",", "")
        filename = f"{safe_address}_{index}.png"

        # 🔥 Explicit computer-use actions
        screenshot_path = run_browser_action(
            action="search_and_capture", value=address, filename=filename
        )

        print(f"[Inspector] Screenshot saved at: {screenshot_path}")

        # 🔥 RETURN AS STREET VIEW (IMPORTANT FIX)
        return {"street_view": screenshot_path}

    except Exception as e:
        print(f"[Inspector ERROR]: {e}")

        return {"street_view": "data/screenshots/fallback.png"}
