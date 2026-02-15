# Windows .exe Release Package Setup

## Complete Build & Distribution Files Created

This document tracks all files created for Windows executable release.

---

## Files Generated

### Build Configuration:

1. **`build_exe.spec`** — PyInstaller specification file
   - Entry point: `gui.py`
   - Console: Disabled (no command window)
   - Bundled modules: All 8 src modules + PyTorch + dependencies
   - Hidden imports: Tkinter, torch, all optional dependencies
   - Size: GUI window + PyTorch runtime (~50 MB executable)

2. **`build_windows.bat`** — Batch build script (for Command Prompt)
   - Auto-installs PyInstaller if missing
   - Cleans previous builds
   - Runs PyInstaller with spec file
   - Creates release package
   - Shows build summary with file sizes

3. **`build_windows.ps1`** — PowerShell build script (modern, recommended)
   - Same functionality as batch script
   - Better error handling
   - File size reporting
   - Prettier output formatting

### Documentation:

4. **`WINDOWS_EXE_BUILD_GUIDE.md`** — Comprehensive build guide
   - Quick start (5 minutes)
   - Build options (GUI, CLI, both)
   - Distribution options (standalone, NSIS installer, GitHub)
   - NSIS installer script example
   - Troubleshooting guide
   - Pre-caching models for distribution
   - Version management
   - File size estimates

5. **`RELEASE_README.md`** — End-user focused documentation
   - Quick start (30 seconds)
   - System requirements
   - How to use workflow
   - Features list
   - Models explained
   - Clothing types (30 types)
   - Color categories (11 colors)
   - Pattern detection (13 patterns)
   - Troubleshooting guide
   - Performance tips
   - Technical details

---

## Build Workflow

### Step 1: Prepare (On Windows Machine)
```bash
python -m pip install pyinstaller
```

### Step 2: Build Executable
Choose one:
```bash
# Option A: Batch script (simple)
build_windows.bat

# Option B: PowerShell (modern)
.\build_windows.ps1

# Option C: Manual (advanced)
pyinstaller build_exe.spec --noconfirm
```

### Step 3: Output Structure
```
dist/
├── AI_Clothing_Sorter/
│   ├── AI_Clothing_Sorter.exe      ← Main application (~50 MB)
│   ├── config.py                   ← Configuration
│   └── [Python runtime + DLLs]
│
release/
├── AI_Clothing_Sorter.exe          ← For distribution
├── README.txt
├── QUICKSTART.txt
└── requirements.txt
```

### Step 4: Distribute
- **Standalone:** Zip `release/` folder, users extract and run
- **Installer:** Use NSIS to create professional Windows installer
- **GitHub:** Upload `release/AI_Clothing_Sorter.exe` to GitHub Releases

---

## What Each File Does

| File | Purpose | When Needed |
|------|---------|------------|
| `build_exe.spec` | PyInstaller config | [REQUIRED] For building |
| `build_windows.bat` | Build automation (Windows) | [REQUIRED] To build .exe |
| `build_windows.ps1` | Build automation (PowerShell) | [OPTIONAL] Alternative to .bat |
| `WINDOWS_EXE_BUILD_GUIDE.md` | Technical build guide | [REFERENCE] Developer docs |
| `RELEASE_README.md` | User documentation | [INCLUDE] With release |

---

## Distribution Checklist

### Before Building:
- [ ] All code committed to git
- [ ] Version bumped in config.py
- [ ] RELEASE_README.md reviewed
- [ ] Requirements.txt up to date

### Building:
- [ ] PyInstaller installed
- [ ] Run build script (bat or ps1)
- [ ] Verify `dist/AI_Clothing_Sorter/AI_Clothing_Sorter.exe` exists
- [ ] Check `release/` folder created

### Testing on Clean Machine:
- [ ] Copy `release/` folder to clean Windows 10/11
- [ ] Run `.exe` file
- [ ] Test model download (first run)
- [ ] Test image processing
- [ ] Verify all features work
- [ ] Check settings persist between runs

### Distribution:
- [ ] Create release tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub Release
- [ ] Upload `release/` zip file
- [ ] Write release notes
- [ ] Update project README with download link

---

## Estimated Sizes

| Component | Size |
|-----------|------|
| Python runtime | ~30 MB |
| PyTorch (bundled) | ~50 MB |
| Dependencies | ~30 MB |
| **Executable + DLLs** | **~110 MB** |
| **Full dist/ folder** | **~180-200 MB** |
|  |  |
| **Release zip** | **~60 MB** (compressed) |
| After install | **~500 MB** (with models) |

---

## First-Run Experience

When user runs `.exe` for first time:

1. **Startup** (2-3 seconds)
2. **Model check** — Looks for cached models
3. **Model download** — If missing (~2-3 minutes, one-time)
   - ResNet50: 162 MB
   - Total downloads: ~320 MB (models cached)
4. **First use** — UI responsive, ready for processing

Subsequent runs: Instant startup (models cached).

---

## Advanced Options

### Pre-Cache Models:
For distribution without model downloads:
1. Run `cache_models.py` on build machine
2. Include torch cache folder with distribution
3. Adds ~500 MB but eliminates first-run delay

### Custom Icon:
1. Add `icon.ico` to project root
2. `build_exe.spec` already references it
3. Rebuild to include custom icon

### Create Installer:
1. Download NSIS: https://nsis.sourceforge.io/
2. Use example script in `WINDOWS_EXE_BUILD_GUIDE.md`
3. Creates professional Windows installer

### Version Updates:
1. Update version in code
2. Rebuild with build script
3. Tag and push to GitHub
4. Create new GitHub Release

---

## Next Steps

### To Build Now:
```powershell
# Run on Windows machine with all dependencies installed
.\build_windows.ps1
```

### To Distribute:
1. Test .exe on clean Windows machine (critical!)
2. Zip `release/` folder
3. Upload to GitHub Releases
4. Share download link with users

### To Create Installer:
See "Creating NSIS Installer" section in `WINDOWS_EXE_BUILD_GUIDE.md`

---

## Troubleshooting Build Issues

### "PyInstaller not found"
```powershell
python -m pip install pyinstaller --upgrade
```

### "Module not found" error
- Ensure all modules in `hidden_imports` are installed
- Run: `python -m pip install -r requirements.txt`

### Executable won't start
- Check Windows event viewer for errors
- Try running as Administrator
- Rebuild: `pyinstaller build_exe.spec --clean`

### File path issues
- Verify `config.py` is in same directory as `.exe`
- Check file permissions on output folder

---

## Support Resources

- **PyInstaller Docs:** https://pyinstaller.org/
- **NSIS Guide:** https://nsis.sourceforge.io/docs/
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github

---

Generated: 2024  
AI Clothing Photo Sorter - Windows Release Setup
