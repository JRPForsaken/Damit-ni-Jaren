@echo off
REM Build script for creating AI Clothing Photo Sorter .exe on Windows
REM Requirements: PyInstaller, all dependencies from requirements.txt

echo.
echo ============================================
echo AI Clothing Photo Sorter - Windows Build
echo ============================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo [1/5] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
echo Done.

echo.
echo [2/5] Running PyInstaller...
pyinstaller build_exe.spec --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)
echo Done.

echo.
echo [3/5] Build output created in: dist\AI_Clothing_Sorter\
if exist dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe (
    echo Successfully created: AI_Clothing_Sorter.exe
)

echo.
echo [4/5] Creating release package...
REM Create a release folder with all necessary files
if not exist release mkdir release
copy dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe release\
copy README.md release\README.txt 2>nul
copy QUICKSTART.md release\QUICKSTART.txt 2>nul
copy requirements.txt release\

echo Done.

echo.
echo [5/5] Build Summary:
echo ============================================
echo - Executable: dist/AI_Clothing_Sorter/AI_Clothing_Sorter.exe
echo - Release folder: release/
echo - Start with: AI_Clothing_Sorter.exe
echo.
echo NOTE: First run will download PyTorch models (~2-3 GB)
echo       Place in Documents/ai_clothing_models/ if pre-downloading
echo ============================================
echo.
echo Build complete! Press any key to exit...
pause
