@echo off
:: GEO-v1.3 Environment Setup Script
:: Updated for Manim 0.19.0+ compatibility

setlocal enabledelayedexpansion

:: 1. Check for admin rights (required for winget)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Please run this script as Administrator!
    echo Right-click and select "Run as administrator"
    pause
    exit /b
)

:: 2. Install FFmpeg
echo.
echo [1/3] Installing FFmpeg...
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
if %errorlevel% neq 0 (
    echo.
    echo ERROR: FFmpeg installation failed
    echo Manual installation required from: https://ffmpeg.org/download.html
    pause
    exit /b
)

:: 3. Verify Python
echo.
echo [2/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python not found in PATH
    echo Download Python 3.8+ from: https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation
    pause
    exit /b
)

:: Verify Python version
for /f "tokens=2 delims= " %%A in ('python --version 2^>^&1') do (
    set "python_version=%%A"
)
for /f "tokens=1,2 delims=." %%A in ("!python_version!") do (
    if %%A lss 3 (
        set "python_ok=0"
    ) else if %%A equ 3 if %%B lss 8 (
        set "python_ok=0"
    )
)

if defined python_ok (
    echo.
    echo ERROR: Python 3.8+ required (Found: !python_version!)
    echo Download newer version from: https://www.python.org/downloads/
    pause
    exit /b
)

:: 4. Install Python dependencies
echo.
echo [3/3] Installing Python packages...
python -m pip install --upgrade pip --no-warn-script-location
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to upgrade pip
    pause
    exit /b
)

pip install manim numpy --no-warn-script-location
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Package installation failed
    pause
    exit /b
)

:: Success message
echo.
echo SUCCESS: Environment setup complete!
echo You can now run: python main_gui.py
pause