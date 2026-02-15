# Windows .exe Build & Release Guide

## Quick Start (5 minutes)

### On Your Windows Build Machine:

1. **Install PyInstaller:**
   ```powershell
   python -m pip install pyinstaller
   ```

2. **Run build script:**
   ```powershell
   .\build_windows.bat
   ```

3. **Find executable:**
   - Main: `dist/AI_Clothing_Sorter/AI_Clothing_Sorter.exe`
   - Release package: `release/` folder

---

## What Gets Built

### In `dist/AI_Clothing_Sorter/`:
- `AI_Clothing_Sorter.exe` — Main application (standalone, ~50MB)
- Supporting DLLs, libraries, and Python runtime
- All internal modules bundled

### In `release/` (distribution package):
- `AI_Clothing_Sorter.exe` — Ready to distribute
- `README.txt` — Documentation
- `QUICKSTART.txt` — Quick setup guide
- `requirements.txt` — For reference

---

## First-Run Experience

### Model Download (~2-3 GB):
1. First launch downloads PyTorch models:
   - ResNet50 (default) — ~162 MB
   - EfficientNet-B7 (optional) — ~255 MB
   - ResNet18 (optional) — ~91 MB

2. Models stored in: `%USERPROFILE%\Documents\ai_clothing_models\`

3. Subsequent runs use local cache (instant startup)

### Pre-Cache Models (Optional):
To avoid first-run delays, cache models before distribution:

```python
# Run once on build machine to pre-cache
python -c "from torchvision import models; models.resnet50(pretrained=True)"
```

Then include `C:\Users\<username>\AppData\Local\torch\` in distribution.

---

## Build Options

### Option 1: GUI Only (Recommended)
- User-friendly interface
- Automatic model management
- Settings caching
- Current spec file already configured

### Option 2: CLI Only
Edit `build_exe.spec`, change:
```python
a = Analysis(['main.py'], ...)  # Instead of gui.py
console=True,  # Show command window
```

### Option 3: Both (Advanced)
Create launcher that offers both modes (requires custom Python script).

---

## File Size Estimates

| Component | Size |
|-----------|------|
| Executable | ~50 MB |
| Python runtime | ~30 MB |
| Dependencies | ~80 MB |
| **Total (base)** | **~160 MB** |
| + ResNet50 model | +162 MB |
| **Full install** | **~320 MB** |

---

## Distribution Options

### Option A: Standalone Executable (Current)
- **Pros:** No installation needed, works on any Windows 10/11
- **Cons:** Large file, first-run delay for models
- **Steps:**
  1. Run `build_windows.bat`
  2. Zip `release/` folder
  3. Users extract and run `AI_Clothing_Sorter.exe`

### Option B: Windows Installer (NSIS)
- **Pros:** Professional, easier for end users
- **Cons:** Requires NSIS tool (~2 MB download)
- **Setup:** See section below

### Option C: GitHub Release
- **Pros:** Version control, automatic deployment
- **Cons:** Requires GitHub account
- **Steps:**
  1. Tag release: `git tag v1.0.0`
  2. Push: `git push origin v1.0.0`
  3. Upload exe to GitHub Releases

---

## Creating NSIS Installer (Windows Installer .msi/.exe)

1. **Download NSIS:** https://nsis.sourceforge.io/

2. **Create installer script** (`installer.nsi`):
```nsis
; NSIS Installer script
!include "MUI2.nsh"

Name "AI Clothing Photo Sorter"
OutFile "AI_Clothing_Sorter_v1.0.0_Setup.exe"
InstallDir "$PROGRAMFILES\AIClothingSorter"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\AI_Clothing_Sorter\AI_Clothing_Sorter.exe"
  File "README.md"
  CreateDirectory "$SMPROGRAMS\AI Clothing Sorter"
  CreateShortCut "$SMPROGRAMS\AI Clothing Sorter\AI Clothing Sorter.lnk" \
                 "$INSTDIR\AI_Clothing_Sorter.exe"
  CreateShortCut "$DESKTOP\AI Clothing Sorter.lnk" \
                 "$INSTDIR\AI_Clothing_Sorter.exe"
SectionEnd
```

3. **Compile:** Right-click `installer.nsi` → Compile NSIS script

4. **Result:** Creates `AI_Clothing_Sorter_v1.0.0_Setup.exe` installer

---

## Troubleshooting

### Build fails: "Module not found"
- Ensure all `hiddenimports` in `build_exe.spec` are included
- Run: `python -m pip install -r requirements.txt`

### Executable won't launch
- Check: `dist/AI_Clothing_Sorter/_internal/` for missing DLLs
- Run with: `.exe 2>&1 | find "Error"` to see error messages
- Regenerate spec: `pyi-makespec gui.py`

### Model download fails
- Ensure internet connection on first run
- Check: `%USERPROFILE%\Documents\ai_clothing_models\` permissions
- Manual download: Use `config.py` to set model path

### File too large
- Use `UPX` compression (included in PyInstaller)
- Remove optional models from `config.py`
- Consider distributing models separately

---

## Release Checklist

- [ ] Run `build_windows.bat` successfully
- [ ] Test `dist/AI_Clothing_Sorter/AI_Clothing_Sorter.exe` on clean Windows machine
- [ ] Verify GUI loads and settings save
- [ ] Test image processing workflow
- [ ] Verify model download on first run
- [ ] Create GitHub release with version tag
- [ ] Upload `release/` folder as zip
- [ ] Update README with download link
- [ ] Post release notes

---

## Version Management

### Building New Versions:

1. **Update version in code:**
   - Edit `config.py`: `VERSION = "1.0.1"`
   - Edit `gui.py`: Update window title

2. **Rebuild:**
   ```powershell
   .\build_windows.bat
   ```

3. **Tag and push:**
   ```powershell
   git tag v1.0.1
   git push origin v1.0.1
   ```

4. **Create GitHub release** with `.exe` file

---

## Support & Feedback

Include these files with release:
- **README.md** - Full documentation
- **QUICKSTART.md** - Setup guide  
- **FEATURES_ADDED.md** - Feature list
- **ACCURACY_IMPROVEMENTS.md** - Technical details

---

## Advanced: Pre-Building PyTorch Models

For faster distribution without model downloads:

```python
# cache_models.py - Run once before building
import torch
from torchvision import models
import os

model_dir = os.path.expanduser("~/.cache/torch/hub")
os.makedirs(model_dir, exist_ok=True)

print("Caching ResNet50...")
models.resnet50(pretrained=True)

print("Caching EfficientNet-B7...")
models.efficientnet_b7(pretrained=True)

print("Caching ResNet18...")
models.resnet18(pretrained=True)

print("Done! Models cached in:", model_dir)
```

Then include cache folder with distribution (adds ~500MB but eliminates first-run download).

---

## Command Line For Advanced Users

### Manual build without batch script:
```powershell
pyinstaller build_exe.spec --noconfirm
```

### Clean rebuild:
```powershell
pyinstaller build_exe.spec --noconfirm --clean
```

### Debug mode (console window):
Edit `build_exe.spec`: `console=True`

### Add icon:
1. Add `icon.ico` to project root
2. Spec already references it: `icon='icon.ico'`
3. Rebuild

---

Generated: 2024
AI Clothing Photo Sorter - Windows Release Edition
