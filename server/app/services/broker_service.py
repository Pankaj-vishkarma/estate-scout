from app.utils.text_editor_tool import write_file
import os
import re
import shutil  # ✅ NEW


def create_property_files(property):
    try:
        # 🔥 Safe folder name
        safe_address = property.get("address", "unknown")

        if not safe_address or safe_address == "N/A":
            safe_address = "property_unknown"

        safe_address = re.sub(r"[^a-zA-Z0-9_]", "_", safe_address)

        # ✅ Unique folder (avoid overwrite)
        folder = os.path.join("data", "listings", safe_address)
        os.makedirs(folder, exist_ok=True)

        # 🔥 Screenshot handling
        image_path = property.get("street_view")

        if image_path:
            image_path_clean = image_path.lstrip("/")

            new_image_path = os.path.join(folder, "screenshot.png")

            if os.path.exists(image_path_clean):
                # ✅ Cross-platform copy
                shutil.copy(image_path_clean, new_image_path)

                property["street_view"] = f"/{new_image_path}".replace("\\", "/")
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

        lease_path = os.path.join(folder, "lease.txt")

        # ✅ Write file
        write_file(lease_path, lease_content)

        print(f"[Broker] Files created for {safe_address}")

        return folder.replace("\\", "/")

    except Exception as e:
        print(f"[Broker ERROR]: {e}")
        return None
