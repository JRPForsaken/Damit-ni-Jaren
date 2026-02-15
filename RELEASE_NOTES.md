# AI Clothing Photo Sorter v1.0.0 - Release Notes

## What's Included

**AI Clothing Photo Sorter** - An intelligent desktop application for automatic organization and classification of clothing photos using deep learning (PyTorch) and computer vision (OpenCV).

### Key Features

✨ **Intelligent Classification** — 30 clothing types, 11 colors, 13 patterns  
🎨 **Shape Detection** — Distinguishes jeans from shorts, jackets from shirts  
📊 **Multi-Attribute Matching** — Groups similar photos together  
🖥️ **Tkinter GUI** — User-friendly Windows desktop interface  
🚀 **PyTorch Models** — ResNet50, EfficientNet-B7, ResNet18 support  
⚡ **GPU Support** — NVIDIA GPU acceleration (optional)  
🔄 **Batch Processing** — Organize hundreds of photos automatically  

## Installation

### Option 1: Standalone Executable (Recommended)
1. Download `AI_Clothing_Sorter.exe`
2. Double-click to launch
3. On first run, models download automatically (~2-3 GB, one-time)
4. Start organizing!

**No installation required. Works on Windows 10/11 (64-bit)**

### Option 2: From Source
```bash
git clone https://github.com/JRPForsaken/Damit-ni-Jaren.git
cd Image-AI
pip install -r requirements.txt
python gui.py
```

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 (64-bit) | Windows 11 (64-bit) |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB | 1 GB |
| GPU | None (CPU works) | NVIDIA GPU |

### First Run
- **Model Download:** ~320 MB (cached for instant startup next time)
- **Initial Setup:** 2-3 minutes
- **Subsequent Runs:** Instant startup

## Getting Started

### Quick Start (30 seconds)

1. Launch `AI_Clothing_Sorter.exe`
2. Click "Browse" to select folder with photos
3. Click "Organize" and wait
4. Check results in `Your_Folder_Organized/`

### File Organization

**Input:**
```
My_Photos/
├── photo1.jpg
├── photo2.jpg
└── ...
```

**Output:**
```
My_Photos_Organized/
├── t_shirt_white_g001_v1.jpg
├── pants_blue_g002_v1.jpg
├── jacket_black_g003_v1.jpg
├── report.txt
└── ...
```

## What's New in v1.0.0

### Core Features
- ✅ Windows .exe executable (232 MB, fully bundled)
- ✅ PyTorch 2.10 + torchvision for deep learning
- ✅ OpenCV 4.13 for advanced image processing
- ✅ Tkinter GUI with responsive interface
- ✅ Settings persistence across sessions

### Classification
- ✅ 30 Philippine-optimized clothing types
- ✅ 11 color categories (HSV-based, lighting-invariant)
- ✅ 13 pattern detection types
- ✅ Shape detection for similar items
- ✅ Multi-attribute similarity matching

### Advanced Features
- ✅ Pattern detector (striped, checked, floral, etc.)
- ✅ Size/fit attributes (sleeves, length, fit)
- ✅ Shape silhouette analysis
- ✅ Coherence validation for grouped photos
- ✅ Detailed classification reports
- ✅ GPU acceleration support (NVIDIA only)

## Supported Clothing Types

**30 Types:** t_shirt, polo, sando, long_sleeve, hoodie, sweater, barong, duster, terno, vest, suit_jacket, jacket, blazer, shawl, cape, pants, jeans, shorts, skirt, bermuda, leggings, dress, maxi_dress, bra, underwear, tank_top, sports_bra, uniform, custom_outfit, (and more)

## Color Categories

Black, White, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Gray

## Pattern Detection

Solid, Striped, Checked, Plaid, Floral, Polka Dots, Paisley, Geometric, Abstract, Gradient, Tie-Dye, Embroidered, Printed

## Technical Details

### Architecture
- **Backend:** PyTorch 2.10 with torchvision 0.25
- **Image Processing:** OpenCV 4.13 + PIL/Pillow 12.1
- **GUI Framework:** Tkinter (built-in with Python)
- **Clustering:** scikit-learn DBSCAN + K-Means
- **Python Version:** 3.12.1

### Models
- **ResNet50** (Default) — Fast & accurate, 162 MB
- **EfficientNet-B7** — Highest accuracy, 255 MB
- **ResNet18** — Fastest, 91 MB

### Performance
- Single photo: ~0.5 seconds (GPU) / ~2-3 seconds (CPU)
- 100 photos: ~30 seconds with GPU
- Batch processing: Automatic clustering and organization

## Accuracy

**Classification Accuracy:** ~85% for clothing types (varies by photo quality)

### Factors Affecting Accuracy
+ Good lighting ✓
+ Clear, uncrumpled clothing ✓
+ White/neutral background ✓
- Blurry photos ✗
- Crumpled/folded items ✗
- Poor lighting ✗
- Incomplete/cropped photos ✗

## Troubleshooting

### Application won't start
- Ensure Windows 10/11 (64-bit)
- Try running as Administrator
- Check internet for first-run setup

### Models fail to download
- Check internet connection
- Verify disk space (320 MB+)
- Check: `%USERPROFILE%\Documents\ai_clothing_models\` permissions

### Very slow processing
- On first run (normal, one-time)
- Upgrade to GPU for 3-5x speedup
- Use ResNet18 model (faster) instead of ResNet50
- Process fewer photos at once

### Photos mislabeled
- Improve photo quality (lighting, clarity)
- Use simple backgrounds
- Avoid heavily cropped/folded items
- Accuracy depends on AI model limitations (~85%)

## File Organization Details

### Filename Format
`type_color_g###_v#.jpg`

- `type` — Clothing type (t_shirt, pants, etc.)
- `color` — Dominant color
- `g###` — Group ID (photos grouped together)
- `v#` — Variant within group (1, 2, 3...)

### Output Report
`report.txt` — Detailed classification results:
- Total photos processed
- Classification breakdown
- Group statistics
- Processing time

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| User-friendly | ✓ | - |
| Browse interface | ✓ | - |
| Settings UI | ✓ | - |
| Batch scripts | - | ✓ |
| Automation | - | ✓ |
| Recommended | **Yes** | Advanced |

## License

**MIT License** — Use, modify, distribute freely. See LICENSE file.

## Support & Feedback

- **Issues?** Check troubleshooting section
- **Feature requests?** Open GitHub issue
- **Bug report?** Include screenshot + details

---

## Advanced: Building from Source

### Requirements
- Python 3.12+
- 4 GB RAM minimum
- 2 GB disk space for dependencies

### Setup
```bash
git clone https://github.com/JRPForsaken/Damit-ni-Jaren.git
cd Image-AI
pip install -r requirements.txt
```

### Run
```bash
# GUI mode (recommended)
python gui.py

# CLI mode (advanced)
python main.py --help
```

### Build .exe yourself
```bash
pip install pyinstaller
./build_windows.ps1
```

See `WINDOWS_EXE_BUILD_GUIDE.md` for detailed build instructions.

---

## Credits

**AI Clothing Photo Sorter v1.0.0**  
Powered by PyTorch, OpenCV, and scikit-learn  
Windows Release Edition  

---

## Version History

### v1.0.0 (February 15, 2026)
- Initial release
- Windows .exe with full PyTorch support
- 30 clothing types, 11 colors, 13 patterns
- Advanced shape detection
- Multi-attribute similarity matching
- MIT License

---

Download and enjoy! 🎉

For questions or issues, visit the GitHub repository.
