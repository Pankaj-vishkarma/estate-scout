from app.utils.browser_tool import run_browser_action
import os
import re

from app.config.settings import FALLBACK_IMAGE


def inspect_property(address: str, index: int):
    try:
        print(f"[Inspector] Processing property: {address}")

        # ✅ Better safe folder name (handles special chars)
        safe_address = re.sub(r"[^a-zA-Z0-9]", "_", address)

        # ✅ Folder structure (assignment compliant)
        folder_path = os.path.join("data", "listings", safe_address)
        os.makedirs(folder_path, exist_ok=True)

        # ✅ Fixed filename (cross-platform safe)
        filename = os.path.join(folder_path, "view.png")

        # 🔥 Browser automation
        screenshot_path = run_browser_action(
            action="search_and_capture",
            value=address,
            filename=filename,
        )

        print(f"[Inspector] Screenshot saved at: {screenshot_path}")

        # ✅ Return structured data
        return {
            "address": address,
            "street_view": screenshot_path,
            "folder": folder_path,
        }

    except Exception as e:
        print(f"[Inspector ERROR]: {e}")

        # ✅ Fallback (ENV-based)
        return {
            "address": address,
            "street_view": FALLBACK_IMAGE,
            "folder": os.path.dirname(FALLBACK_IMAGE),
        }
