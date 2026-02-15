# PowerShell Build Script for AI Clothing Photo Sorter
# Run as: .\build_windows.ps1

Write-Host ""
Write-Host "============================================"
Write-Host "AI Clothing Photo Sorter - Windows Build"
Write-Host "============================================"
Write-Host ""

# Check if PyInstaller is installed
$piInstalled = pip show pyinstaller 2>&1 | Select-String "Name: pyinstaller"

if (-not $piInstalled) {
    Write-Host "Installing PyInstaller..."
    python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install PyInstaller"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "[1/5] Cleaning previous builds..."
Remove-Item -Path "dist" -Recurse -ErrorAction SilentlyContinue | Out-Null
Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue | Out-Null
Remove-Item -Path "__pycache__" -Recurse -ErrorAction SilentlyContinue | Out-Null
Write-Host "Done."

Write-Host ""
Write-Host "[2/5] Running PyInstaller..."
python -m PyInstaller build_exe.spec --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: PyInstaller build failed"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Done."

Write-Host ""
Write-Host "[3/5] Build output created in: dist\AI_Clothing_Sorter\"
if (Test-Path "dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe") {
    Write-Host "Successfully created: AI_Clothing_Sorter.exe"
}

Write-Host ""
Write-Host "[4/5] Creating release package..."
if (-not (Test-Path "release")) {
    New-Item -ItemType Directory -Path "release" | Out-Null
}
Copy-Item -Path "dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe" -Destination "release\" -Force
Copy-Item -Path "README.md" -Destination "release\README.txt" -ErrorAction SilentlyContinue -Force
Copy-Item -Path "QUICKSTART.md" -Destination "release\QUICKSTART.txt" -ErrorAction SilentlyContinue -Force
Copy-Item -Path "requirements.txt" -Destination "release\" -Force
Write-Host "Done."

Write-Host ""
Write-Host "[5/5] Build Summary:"
Write-Host "============================================"
Write-Host "- Executable: dist/AI_Clothing_Sorter/AI_Clothing_Sorter.exe"
Write-Host "- Release folder: release/"
Write-Host "- Start with: AI_Clothing_Sorter.exe"
Write-Host ""
Write-Host "NOTE: First run will download PyTorch models (~2-3 GB)"
Write-Host "      Place in Documents/ai_clothing_models/ if pre-downloading"
Write-Host "============================================"
Write-Host ""
Write-Host "Build complete!"
Write-Host ""

# Get file sizes
$exeSize = ((Get-Item "dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe").Length / 1MB).ToString("F2")
$folderSize = ((Get-ChildItem "dist" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB).ToString("F2")

Write-Host "File Sizes:"
Write-Host "- Main executable: $exeSize MB"
Write-Host "- Total dist folder: $folderSize MB"
Write-Host ""

Read-Host "Press Enter to exit"
