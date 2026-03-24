from app.utils.bash_tool import run_command
from app.utils.text_editor_tool import write_file
import os
import re  # 🔥 NEW


def create_property_files(property):
    try:
        # 🔥 Safe folder name (FIXED)
        safe_address = property.get("address", "unknown")

        if not safe_address or safe_address == "N/A":
            safe_address = "property_unknown"

        # 🔥 REMOVE ALL SPECIAL CHARS (IMPORTANT FIX)
        safe_address = re.sub(r"[^a-zA-Z0-9_]", "_", safe_address)

        folder = f"data/listings/{safe_address}"

        # ✅ Bash: create directory
        run_command(f"mkdir -p {folder}")

        # 🔥 EXTRA SAFETY
        os.makedirs(folder, exist_ok=True)

        # 🔥 Screenshot move (FIXED FIELD)
        image_path = property.get("street_view")  # 🔥 CHANGED

        if image_path:
            image_path_clean = image_path.lstrip("/")

            new_image_path = f"{folder}/screenshot.png"

            if os.path.exists(image_path_clean):
                run_command(f"cp {image_path_clean} {new_image_path}")

                # 🔥 STORE AS STREET_VIEW (NOT image)
                property["street_view"] = f"/{new_image_path}"
            else:
                print(f"[Broker] Image not found: {image_path_clean}")

        # 🔥 Lease content
        lease_content = f"""
===== PROPERTY LEASE AGREEMENT =====

Title   : {property.get('title', 'N/A')}
Price   : {property.get('price', 'N/A')}
Address : {property.get('address', 'N/A')}

Terms & Conditions:
- Minimum lease duration: 12 months
- Security deposit required
- No illegal activities allowed
- Property inspection completed

Status: Ready for lease
"""

        lease_path = f"{folder}/lease.txt"

        # ✅ Text Editor Tool
        write_file(lease_path, lease_content)

        print(f"[Broker] Files created for {safe_address}")

        return folder

    except Exception as e:
        print(f"[Broker ERROR]: {e}")
        return None
