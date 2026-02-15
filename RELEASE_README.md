# AI Clothing Photo Sorter - Release Edition

**A PyTorch-powered desktop application for intelligent photo organization and classification.**

---

## Quick Start (30 seconds)

1. **Extract** the zip file
2. **Double-click** `AI_Clothing_Sorter.exe`
3. **Wait** for first-run setup (~2-3 minutes for model download)
4. **Select folder** with clothing photos
5. **Click Organize** 

Done! Photos are now sorted by clothing type, color, and pattern.

---

## System Requirements

- **OS:** Windows 10 or Windows 11 (64-bit)
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 
  - App: ~160 MB
  - Models: ~320 MB (downloads automatically)
  - Total: ~500 MB
- **Internet:** First-run only (for model download)

### Optional GPU Acceleration:
- NVIDIA GPU: Install CUDA Toolkit for faster processing
- Without GPU: CPU processing works fine (slower)

---

## How to Use

### Main Workflow:

1. **Launch:** `AI_Clothing_Sorter.exe`

2. **Select Folder:** Click "Browse" and choose folder with photos

3. **Configure (Optional):**
   - Model: ResNet50 (default, recommended)
   - Min group size: 2 photos minimum
   - Similarity threshold: 0.5 (medium)
   - Keep originals: Usually Yes (recommended)

4. **Process:** Click "Organize" and wait

5. **Results:** Organized in new subfolder:
   ```
   Your_Folder_Organized/
   ├── jacket_black/
   ├── pants_blue/
   ├── t_shirt_white/
   └── ...
   ```

---

## Features

✓ **Intelligent Classification** - Recognizes 30 clothing types  
✓ **Color Detection** - Identifies dominant colors automatically  
✓ **Pattern Recognition** - Detects stripes, checks, flowers, etc.  
✓ **Shape Analysis** - Distinguishes similar items (jeans vs shorts, jackets vs shirts)  
✓ **Similarity Clustering** - Groups similar photos together  
✓ **Multiple AI Models** - Choose from ResNet50, EfficientNet-B7, ResNet18  
✓ **GPU Support** - Faster processing with NVIDIA GPUs  
✓ **Batch Processing** - Organize hundreds of photos automatically  

---

## Models Explained

### First Run Setup:

The app downloads pre-trained AI models on first launch. This is automatic and one-time:

- **ResNet50** (Default) — Fast & accurate, ~162 MB
- **EfficientNet-B7** — Highest accuracy, ~255 MB  
- **ResNet18** — Fastest, ~91 MB

All models automatically cached for instant startup next time.

---

## File Organization

### Input:
```
My_Photos/
├── photo1.jpg
├── photo2.jpg
├── photo3.jpg
└── ...
```

### Output:
```
My_Photos_Organized/
├── t_shirt_white_g001_v1.jpg   (type_color_groupID_variant)
├── t_shirt_white_g001_v2.jpg
├── pants_blue_g002_v1.jpg
├── jacket_black_g003_v1.jpg
├── jacket_black_g003_v2.jpg
└── report.txt                   (detailed classification report)
```

**Filename Format:** `type_color_g###_v#.jpg`
- `type` — Clothing type (t_shirt, pants, jacket, etc.)
- `color` — Dominant color (black, blue, white, etc.)
- `g###` — Group number (photos grouped together)
- `v#` — Variant within group (if similar variants exist)

---

## Clothing Types Recognized

**Tops:** t_shirt, polo, sando, long_sleeve, hoodie, sweater, barong, duster  
**Formal:** terno, vest, suit_jacket  
**Outerwear:** jacket, blazer, shawl, cape  
**Bottoms:** pants, jeans, shorts, skirt, bermuda, leggings  
**Dresses:** dress, maxi_dress  
**Undergarments:** bra, underwear  
**Active:** tank_top, sports_bra  
**Other:** uniform, custom_outfit

---

## Color Categories

Black, White, Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Gray

---

## Pattern Detection

Solid, Striped, Checked, Plaid, Floral, Polka Dots, Paisley, Geometric, Abstract, Gradient, Tie-Dye, Embroidered, Printed

---

## Troubleshooting

### Application won't start
- Ensure Windows 10/11 (64-bit)
- Try running as Administrator
- Check internet (first-run model download)

### Very slow on first photo
- First run downloads models (~5-10 min)
- Automatic caching makes following runs fast
- Check RAM usage (should be under 2 GB)

### Photos mislabeled
- AI isn't perfect - accuracy ~85% for clothing types
- Ensure good lighting in photos
- Avoid blurry or cropped images

### "Model download failed"
- Check internet connection
- Retry - models cache on disk for offline use
- Check: `%USERPROFILE%\Documents\ai_clothing_models\`

### Slow processing (CPU-only)
- Install CUDA Toolkit for GPU acceleration (NVIDIA only)
- Process fewer photos at once
- Try smaller ResNet18 model instead

---

## Performance Tips

1. **Good photos = Better results**
   - Clear, well-lit clothing photos
   - Avoid blurry or partial photos
   - White/neutral background preferred

2. **Batch size matters**
   - 50-100 photos: ~30 seconds
   - 500 photos: ~3-5 minutes
   - 2000+ photos: Process in batches

3. **GPU acceleration** (NVIDIA only)
   - Install: https://developer.nvidia.com/cuda-toolkit
   - 3-5x faster processing
   - Automatic if installed

---

## Advanced Usage

### Command Line Interface (CLI):

For advanced users, CLI mode available:
```powershell
AI_Clothing_Sorter.exe --input "C:\My\Photos" --output "C:\Output" --model resnet50
```

See `QUICKSTART.txt` for full CLI options.

---

## File Locations

Original organized photos stay in original folder (by default) with `_Organized` suffix:
```
C:\Users\YourName\Pictures\My_Clothes/
C:\Users\YourName\Pictures\My_Clothes_Organized/  ← Output here
```

### Model cache location:
```
C:\Users\YourName\Documents\ai_clothing_models\
```

(Automatic, you don't need to do anything)

---

## What Data is Used?

✓ **Only local** - All processing happens on your computer  
✓ **No cloud** - Photos never uploaded  
✓ **No tracking** - No analytics or telemetry  
✓ **Your control** - You choose input/output folders  

---

## Limitations

- **Accuracy:** ~85% for clothing types (varies by photo quality)
- **Photo types:** Best for clothing on hangers/flat lay; worse for full-body/group photos
- **Speed:** CPU-only slower than GPU (consider batching)
- **Languages:** UI in English only
- **Models:** Fixed models (not customizable)

---

## Support & Feedback

- **Issues?** Check troubleshooting section above
- **Feature requests?** See GitHub repo
- **Found a bug?** Screenshot + detailed description helps

---

## Technical Details

**Built with:**
- Python 3.12 + PyTorch 2.10 (deep learning)
- OpenCV 4.13 (computer vision)
- Tkinter (GUI)
- scikit-learn (clustering)

**Original repo:** Image-AI (GitHub)  
**License:** Check included LICENSE file  
**Version:** 1.0.0

---

## First Time? Start Here:

1. Extract files
2. Run `AI_Clothing_Sorter.exe`
3. Select a folder with clothing photos (10-50 to start)
4. Click "Organize"
5. Check results in folder ending with `_Organized`

**That's it!** 

For detailed guide, see `QUICKSTART.txt`

---

*Happy organizing!*

Version 1.0.0 | Windows Release | 2024
