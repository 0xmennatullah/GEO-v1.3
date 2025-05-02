import subprocess
import sys
from tkinter import messagebox

def check_latex():
    """Check if LaTeX is installed"""
    try:
        # Check for either MiKTeX or TeX Live
        result = subprocess.run(["latex", "--version"], 
                              capture_output=True, 
                              text=True)
        return "MiKTeX" in result.stdout or "TeX Live" in result.stdout
    except FileNotFoundError:
        return False

def verify_environment():
    """Check all dependencies"""
    missing = []
    
    if not check_latex():
        missing.append("LaTeX (MiKTeX or TeX Live)")
    
    # [Keep your existing FFmpeg and Python checks...]
    
    if missing:
        messagebox.showwarning(
            "Missing Dependencies",
            "For full functionality, install:\n- " + "\n- ".join(missing) +
            "\n\nBasic rendering will work without LaTeX."
        )
        return True  # Continue with warning instead of exiting
    return True
