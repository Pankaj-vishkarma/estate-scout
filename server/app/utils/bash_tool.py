import subprocess


def run_command(cmd: list[str]):
    """
    Safe command execution (NO shell=True)
    Example: ["mkdir", "-p", "folder"]
    """
    try:
        if not cmd or not isinstance(cmd, list):
            raise ValueError("Command must be a list")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # ✅ prevent hang
        )

        if result.returncode != 0:
            print(f"[Bash ERROR]: {result.stderr}")
            return None

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print("[Bash ERROR]: Command timed out")
        return None

    except Exception as e:
        print(f"[Bash ERROR]: {e}")
        return None
