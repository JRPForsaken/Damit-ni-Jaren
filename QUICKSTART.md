# 🚀 Quick Start Guide

Get started with AI Clothing Photo Sorter in 3 easy steps!

## Step 1: Install Dependencies

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

This will install all necessary packages including PyTorch, Pillow, and scikit-learn.

**Note**: The first time you run the app, it will automatically download the AI model (~100MB). This is a one-time download.

## Step 2: Prepare Your Photos

1. Gather all your clothing photos in one folder
2. Supported formats: JPG, PNG, BMP, GIF, TIFF, WEBP
3. Any number of photos (the more, the better the AI learns!)

## Step 3: Run the Application

### Option A: GUI (Easiest) 🖥️

```bash
python gui.py
```

Then:
1. Click "Browse..." next to Input Folder
2. Select your folder with clothing photos
3. (Optional) Adjust settings
4. Click "🚀 Start Sorting"
5. Wait for completion and check the results!

### Option B: Command Line 💻

```bash
python main.py "path/to/your/photos"
```

Example:
```bash
python main.py "C:/Users/YourName/Pictures/Clothes"
```

## 📊 Check Your Results

After processing, you'll find:

1. **Organized folders** in `sorted_clothes/` directory
   - Each clothing type has its own folder
   - Files are renamed systematically

2. **Reports**:
   - `sorting_report.html` - Open in browser for visual report
   - `sorting_report.csv` - Open in Excel/Sheets
   - `summary.json` - Machine-readable summary

## 💡 Tips for Best Results

1. **Good lighting**: Clear, well-lit photos work best
2. **Clean background**: Plain backgrounds help the AI focus on clothing
3. **Multiple angles**: The app will group same items from different angles
4. **Consistent quality**: Similar photo quality across all images

## ⚙️ Common Settings

### Similarity Threshold
- **0.95**: Very strict (only nearly identical items grouped)
- **0.85**: Balanced (default, recommended)
- **0.75**: Loose (more items grouped together)

### Clustering Method
- **DBSCAN**: Better for varying group sizes (default)
- **K-Means**: Faster, creates equal-sized groups

### Copy vs Move
- **Copy** (default): Keeps original files intact
- **Move**: Moves files to new location (saves space)

## 🆘 Need Help?

**Problem**: "No valid images found"
- Check if folder path is correct
- Ensure images are in supported formats

**Problem**: Slow processing
- Use `--no-gpu` flag if GPU causes issues
- Process fewer images first to test

**Problem**: Poor grouping
- Adjust similarity threshold
- Try different clustering method

## 📖 Full Documentation

For detailed information, see [README.md](README.md)

## 🎯 Example Workflow

```bash
# 1. Install (one time only)
pip install -r requirements.txt

# 2. Run with your photos
python gui.py

# Or use command line
python main.py "C:/MyPhotos/Clothes" --output "organized_wardrobe"

# 3. Check results
# Open sorted_clothes/sorting_report.html in your browser
```

## 🎉 That's It!

You're ready to organize your clothing photos with AI!

---

**Questions?** Check the [README.md](README.md) for more details.
