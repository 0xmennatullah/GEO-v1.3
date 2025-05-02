import subprocess
import sys
from tkinter import messagebox

def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Additional verification of FFmpeg version
        if "ffmpeg version" in result.stdout.split('\n')[0]:
            return True
        return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_python_version():
    """Verify Python version meets requirements"""
    return sys.version_info >= (3, 8)

def get_install_commands():
    """Return platform-specific installation commands"""
    if sys.platform == "win32":
        return {
            'ffmpeg': "winget install Gyan.FFmpeg (Admin PowerShell)",
            'python': "Download from python.org"
        }
    elif sys.platform == "darwin":
        return {
            'ffmpeg': "brew install ffmpeg",
            'python': "brew install python"
        }
    else:  # Linux
        return {
            'ffmpeg': "sudo apt install ffmpeg",
            'python': "sudo apt install python3.8+"
        }

def verify_environment():
    """Check all environment requirements"""
    errors = []
    solutions = get_install_commands()
    
    if not check_python_version():
        errors.append(f"Python 3.8+ required (Current: {sys.version.split()[0]})")
        errors.append(f"Solution: {solutions['python']}")
    
    if not check_ffmpeg():
        errors.append("FFmpeg not installed or not in PATH")
        errors.append(f"Solution: {solutions['ffmpeg']}")
    
    if errors:
        messagebox.showerror(
            "Environment Error",
            "\n".join(errors) + 
            "\n\nAfter installing, restart the application."
        )
        return False
    return True

if __name__ == "__main__":
    if verify_environment():
        print("All dependencies are properly installed!")
    else:
        sys.exit(1)