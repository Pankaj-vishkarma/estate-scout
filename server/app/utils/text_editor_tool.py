import os


def write_file(path: str, content: str) -> bool:
    try:
        # ✅ Validate path
        if not path or not isinstance(path, str):
            raise ValueError("Invalid file path")

        directory = os.path.dirname(path)

        # ✅ Ensure directory exists
        if directory:
            os.makedirs(directory, exist_ok=True)

        # ✅ Write file safely
        with open(path, "w", encoding="utf-8") as f:
            f.write(content or "")

        return True  # ✅ success

    except Exception as e:
        print(f"[TextEditor ERROR]: {e}")
        return False  # ❌ failure
