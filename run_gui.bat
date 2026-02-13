@echo off
echo ========================================
echo  AI Clothing Photo Sorter - GUI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Starting GUI application...
echo.

python gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo.
    echo Please make sure all dependencies are installed:
    echo   pip install -r requirements.txt
    echo.
    pause
)
