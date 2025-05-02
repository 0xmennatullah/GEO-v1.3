import subprocess
import sys
from tkinter import messagebox

def check_latex():
    """Verify LaTeX is installed and working"""
    try:
        test_tex = r"\documentclass{article}\begin{document}Test\end{document}"
        result = subprocess.run(
            ["pdflatex", "--version"],
            input=test_tex,
            capture_output=True,
            text=True,
            timeout=5
        )
        return "pdfTeX" in result.stdout
    except:
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
