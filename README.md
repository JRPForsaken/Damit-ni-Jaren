# AI Clothing Photo Sorter

An intelligent Python application that uses AI and computer vision to automatically scan, classify, and organize bulk clothing photos.

It identifies clothing types and colors and intelligently groups the same item even when photographed from different angles.

---

## Features

- AI-powered image classification using deep learning (ResNet50)
- Automatic clothing type detection (shirts, pants, dresses, jackets, etc.)
- Dominant color recognition
- Multi-angle grouping for the same clothing item
- Smart folder organization by clothing type
- Intelligent file renaming (type_color_id)
- Detailed output reports (HTML, CSV, JSON)
- Graphical user interface (GUI) and command-line interface (CLI)
- Optional GPU acceleration with CUDA

---

## Requirements

- Python 3.8 or higher
- CUDA-capable GPU (optional, for faster processing)

---

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

On first run, the application will automatically download a pre-trained AI model (~100 MB).

---

## Usage

### GUI Mode (Recommended)

```bash
python gui.py
```

### Command-Line Mode

```bash
python main.py <input_folder> [options]
```

Example:

```bash
python main.py "C:/Photos/Clothes" --threshold 0.85 --method dbscan
```

---

## Output Structure

```text
sorted_clothes/
â”œâ”€â”€ shirt/
â”‚   â”œâ”€â”€ shirt_blue_g001_v1.jpg
â”‚   â”œâ”€â”€ shirt_blue_g001_v2.jpg
â”‚   â””â”€â”€ shirt_red_g002_v1.jpg
â”œâ”€â”€ pants/
â”‚   â”œâ”€â”€ pants_black_g001_v1.jpg
â”‚   â””â”€â”€ pants_blue_g002_v1.jpg
â”œâ”€â”€ dress/
â”‚   â””â”€â”€ ...
â”œâ”€â”€ sorting_report.html
â”œâ”€â”€ sorting_report.csv
â”œâ”€â”€ summary.json
â””â”€â”€ file_index.txt
```

### Filename Format

- type_color_g###_v#.ext (multi-angle items)
- type_color_id.ext (single items)

---

## How It Works

1. Scans the input folder for supported image files.
2. Extracts deep features using a ResNet50 CNN.
3. Classifies clothing type and dominant color.
4. Groups similar items using clustering algorithms (DBSCAN or K-Means).
5. Detects multiple views of the same item.
6. Organizes and renames files.
7. Generates detailed reports.

---

## Configuration

You can customize behavior in `config.py`:

```python
SIMILARITY_THRESHOLD = 0.85
CLUSTERING_METHOD = "dbscan"  # or "kmeans"
COPY_FILES = True             # False to move instead of copy

SUPPORTED_FORMATS = [
    ".jpg", ".jpeg", ".png", ".bmp",
    ".gif", ".tiff", ".webp"
]
```

---

## Troubleshooting

### No valid images found
- Ensure the folder contains supported image formats.
- Check file permissions.

### Slow processing
- Enable GPU acceleration if available.
- Reduce image resolution.
- Test with fewer images.

### Poor grouping results
- Adjust similarity threshold (recommended 0.8â€“0.95).
- Try a different clustering method.
- Use clear, well-lit images.

### Out of memory
- Reduce batch size in configuration.
- Disable GPU processing.
- Process images in smaller batches.

---

## Contributing

Contributions are welcome. You may:
- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

---

## License

This project is licensed under the MIT License.

---

Version: 1.0.0