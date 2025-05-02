import subprocess
import sys
from tkinter import messagebox

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False

def check_python_version():
    return sys.version_info >= (3, 8)

def verify_environment():
    errors = []
    if not check_python_version():
        errors.append("Python 3.8+ required")
    if not check_ffmpeg():
        errors.append("FFmpeg not installed")
    
    if errors:
        messagebox.showerror(
            "Environment Error",
            "Fix these issues:\n- " + "\n- ".join(errors)
        )
        return False
    return True

if __name__ == "__main__":
    verify_environment()
