import subprocess


def run_command(cmd: str):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"[Bash ERROR]: {e}")
        return None
