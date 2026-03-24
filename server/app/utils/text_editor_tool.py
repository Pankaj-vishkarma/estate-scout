import os  # 🔥 NEW


def write_file(path: str, content: str):
    try:
        # 🔥 Ensure directory exists (CRITICAL FIX)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 🔥 FIX: UTF-8 encoding added
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        print(f"[TextEditor ERROR]: {e}")
