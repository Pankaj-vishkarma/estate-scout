import os
import shutil


def create_property_files(property):
    try:
        # 🔥 Safe folder name
        safe_address = (
            property.get("address", "unknown").replace(" ", "_").replace(",", "")
        )
        folder = f"data/listings/{safe_address}"

        # ✅ Create directory
        os.makedirs(folder, exist_ok=True)

        # 🔥 Screenshot move (IMPORTANT)
        image_path = property.get("image")

        if image_path:
            # remove leading slash (/data/...)
            image_path_clean = image_path.lstrip("/")

            if os.path.exists(image_path_clean):
                new_image_path = os.path.join(folder, "screenshot.png")

                # move file
                shutil.copy(image_path_clean, new_image_path)

                # update property image path
                property["image"] = f"/{new_image_path}"

        # 🔥 Create lease file (detailed)
        lease_path = os.path.join(folder, "lease.txt")

        with open(lease_path, "w") as f:
            f.write("===== PROPERTY LEASE AGREEMENT =====\n\n")
            f.write(f"Title   : {property.get('title', 'N/A')}\n")
            f.write(f"Price   : {property.get('price', 'N/A')}\n")
            f.write(f"Address : {property.get('address', 'N/A')}\n\n")
            f.write("Terms & Conditions:\n")
            f.write("- Minimum lease duration: 12 months\n")
            f.write("- Security deposit required\n")
            f.write("- No illegal activities allowed\n")
            f.write("- Property inspection completed\n\n")
            f.write("Status: Ready for lease\n")

        print(f"[Broker] Files created for {safe_address}")

        return folder

    except Exception as e:
        print(f"[Broker ERROR]: {e}")
        return None
