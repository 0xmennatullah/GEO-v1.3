@echo off
:: GEO-v1.3 Complete Setup Script
:: Installs FFmpeg, LaTeX, and Python dependencies

setlocal enabledelayedexpansion

:: 1. Check admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Run as Administrator!
    pause
    exit /b
)

:: 2. Install FFmpeg
echo Installing FFmpeg...
winget install Gyan.FFmpeg -e --accept-package-agreements
if %errorlevel% neq 0 (
    echo ERROR: FFmpeg installation failed
    pause
    exit /b
)

:: 3. Install MiKTeX (LaTeX)
echo Installing MiKTeX...
winget install ChristianSchenk.MiKTeX -e --accept-package-agreements
if %errorlevel% neq 0 (
    echo WARNING: LaTeX installation failed
    echo Manim will work but may have limited text rendering
)

:: 4. Verify Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b
)

:: 5. Install Python packages
echo Installing Python dependencies...
pip install manim numpy --no-warn-script-location
if %errorlevel% neq 0 (
    echo ERROR: Package installation failed
    pause
    exit /b
)

echo SUCCESS: Setup completed!
pause
