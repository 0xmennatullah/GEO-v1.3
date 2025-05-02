@echo off
:: Install FFmpeg
winget install Gyan.FFmpeg

:: Verify Python
python --version
if errorlevel 1 (
    echo Python not found! Install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b
)

:: Install dependencies
pip install --upgrade pip
pip install manim numpy
