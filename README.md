# AI Clothing Photo Sorter

An intelligent Python application that uses AI and computer vision to automatically scan, classify, and organize bulk clothing photos.

It identifies clothing types and colors and intelligently groups the same item even when photographed from different angles.

---

## Features

- **AI-powered image classification** using deep learning (ResNet50, EfficientNet-B7, ResNet18)
- **Automatic clothing type detection** (30+ practical clothing types optimized for Philippine context)
- **Advanced shape/silhouette detection** to distinguish similar items (jeans vs shorts, jackets vs shirts)
- **HSV-based color recognition** (11 color categories with lighting-invariant matching)
- **Pattern detection** (13 pattern types: solid, striped, checked, floral, polka dots, tie-dye, etc.)
- **Size/attribute detection** (sleeve length, garment length, fit type, aspect ratio)
- **Completeness detection** for cropped, folded, or incomplete items
- **Multi-angle grouping** for the same clothing item (different camera angles detected)
- **Enhanced multi-attribute similarity matching** combining visual features, patterns, sizes, and shapes
- **Smart folder organization** by clothing type, with optional pattern/size sub-grouping
- **Intelligent file renaming** (type_color_id or type_color_group_version)
- **Path caching system** to remember your last-used folders and preferences
- **Multiple model options** for speed vs accuracy trade-off
- **Detailed output reports** (HTML with charts, CSV exports, JSON summaries)
- **Dual interface** - Graphical user interface (GUI) and command-line interface (CLI)
- **Optional GPU acceleration** with CUDA support
- **Batch processing** with configurable parameters

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
2. Extracts deep features using selected AI model (ResNet50/EfficientNet-B7/ResNet18).
3. **Analyzes silhouette and shape** (width variation, completeness, contour complexity).
4. Detects patterns in clothing (stripes, checks, flowers, tie-dye, etc.).
5. Analyzes size/fit attributes (sleeve type, length, fit style).
6. **HSV-based color detection** (lighting-invariant matching for accurate color identification).
7. Classifies clothing type using **multi-factor analysis**:
   - Feature vectors from CNN
   - Shape characteristics (distinguishes jeans from shorts, jackets from shirts)
   - Aspect ratio and completeness
8. Groups similar items using **multi-attribute clustering**:
   - Visual feature similarity (CNN-based)
   - Pattern compatibility matching
   - Size/fit attribute alignment
   - Shape coherence validation
9. Detects multiple views of the same item using high-similarity threshold.
10. Handles incomplete/folded items gracefully with completeness scoring.
11. Organizes and renames files with meaningful names.
12. Generates detailed reports (HTML, CSV, JSON).

### Advanced Classification Pipeline

```
IMAGE → Silhouette Analysis
         ├─ Width Variance: High (>0.3) = Pants, Low (<0.25) = Shorts
         ├─ Complexity: High = Jacket, Low = Shirt
         ├─ Symmetry: >0.7 = Shirt-like, Asymmetric = Pants-like
         └─ Completeness: Full vs Cropped/Folded detection
         ↓
       → HSV Color Matching (Lighting-invariant)
         ├─ Hue: Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown
         ├─ Saturation: Vivid vs Pastel distinction
         └─ Value: Brightness adjustment
         ↓
       → Multi-Attribute Similarity
         ├─ Visual (50%) + Pattern (25%) + Size (25%)
         └─ Shape validation ensures type coherence
         ↓
       → OUTPUT: Accurate Classification & Grouping
```

### Shape Detection Advantages

- **Jeans vs Shorts**: Width variation analysis distinguishes tapered bottoms
- **Jacket vs Shirt**: Contour complexity detects structured layers
- **Incomplete Items**: Completeness scoring handles cropped/folded photos
- **Lighting Invariance**: Shape works across different lighting conditions

---

## Configuration

You can customize behavior in `config.py`:

```python
# Clustering Settings
SIMILARITY_THRESHOLD = 0.85          # Cosine similarity threshold
CLUSTERING_METHOD = "dbscan"         # or "kmeans"
MIN_CLUSTER_SIZE = 2                 # Minimum images per cluster

# Similarity Matching Weights
VISUAL_WEIGHT = 0.5                  # Visual feature importance
PATTERN_WEIGHT = 0.25                # Pattern matching importance
SIZE_WEIGHT = 0.25                   # Size/fit importance

# Pattern Detection (13 types)
CLOTHING_PATTERNS = [
    'solid', 'striped', 'checked', 'plaid', 'floral', 
    'polka_dots', 'paisley', 'geometric', 'abstract', 
    'gradient', 'tie_dye', 'embroidered', 'printed'
]

# Size Attributes
CLOTHING_ATTRIBUTES = [
    'short_sleeve', 'long_sleeve', 'sleeveless', 'three_quarter',
    'full_length', 'cropped', 'above_knee', 'below_knee',
    'regular_fit', 'slim_fit', 'loose_fit', 'oversized'
]

# File Organization
COPY_FILES = True                    # False to move instead of copy
CREATE_SUBFOLDERS = True             # Create subfolders by type
GROUP_SIMILAR_ITEMS = True           # Group same items from different angles

# AI Model Selection
MODEL_NAME = 'resnet50'              # or 'efficientnet_b7', 'resnet18'

SUPPORTED_FORMATS = [
    ".jpg", ".jpeg", ".png", ".bmp",
    ".gif", ".tiff", ".webp"
]
```

### Advanced Configuration

**Use Pattern Matching:**
```python
# In your code:
matcher = SimilarityMatcher(use_pattern=True, use_size=True)
```

**Pattern Similarity Thresholds:**
- `PATTERN_EXACT_MATCH = 1.0` - Same pattern
- `PATTERN_SIMILAR_MATCH = 0.8` - Related patterns (striped ≈ checked)
- `PATTERN_DIFFERENT_MATCH = 0.3` - Unrelated patterns

---

## Module Architecture

### Core Processing Modules (`src/`)

| Module | Purpose | Features |
|--------|---------|----------|
| `feature_extractor.py` | Deep learning feature extraction | ResNet50, EfficientNet-B7, ResNet18 models |
| `classifier.py` | Multi-attribute clothing classification | Type, color (HSV), pattern, size classification |
| `pattern_detector.py` | Pattern/texture detection | 13 pattern types (solid, striped, floral, tie-dye, etc.) |
| `size_detector.py` | Size/attribute detection | Sleeve, length, fit, aspect ratio analysis |
| **`shape_detector.py`** | **Silhouette analysis** | **Width variance, complexity, symmetry, completeness** |
| `similarity_matcher.py` | Multi-attribute clustering | Visual + Pattern + Size + Shape similarity |
| `image_processor.py` | Image I/O and preprocessing | Loading, resizing, validation |
| `organizer.py` | File organization and renaming | Folder creation, intelligent naming |
| `report_generator.py` | Report generation | HTML, CSV, JSON outputs |
| `path_cache.py` | Settings persistence | Remembers user preferences |

### Classification Factors (in order of application)

1. **Filename matching** - Quick identification from filenames
2. **Feature-based** - CNN embeddings (2048-dim vectors)
3. **Shape-based** - Silhouette analysis (width, complexity, symmetry)
4. **Color-based** - HSV color space matching
5. **Pattern-based** - Texture analysis
6. **Size-based** - Attribute consistency
7. **Similarity-based** - Multi-attribute clustering

---

### Core Methods

**Compute Weighted Similarity Matrix**
```python
from src.similarity_matcher import SimilarityMatcher
from src.pattern_detector import PatternDetector
from src.size_detector import SizeDetector

matcher = SimilarityMatcher(use_pattern=True, use_size=True)

# Compute combined similarity matrix
weighted_sim = matcher.compute_weighted_similarity_matrix(
    features=feature_vectors,
    patterns=detected_patterns,
    size_attributes=detected_sizes
)
```

**Refine Groups with Attributes**
```python
# Re-cluster groups using pattern and size information
refined_groups = matcher.refine_groups_with_attributes(
    groups=initial_groups,
    features=feature_vectors,
    image_paths=image_paths,
    patterns=patterns,
    size_attributes=sizes
)
```

**Validate Group Coherence**
```python
# Check quality of grouping
validation = matcher.validate_group_coherence(
    group_paths=group_paths,
    features=feature_vectors,
    image_paths=image_paths,
    patterns=patterns,
    size_attributes=sizes
)
# Returns: {coherence_score, is_coherent, issues, pattern_diversity}
```

**Get Detailed Similarity Scores**
```python
# Debug: See breakdown of why two items are grouped
scores = matcher.get_detailed_similarity_scores(
    image_path1=path1,
    image_path2=path2,
    features=feature_vectors,
    image_paths=image_paths,
    patterns=patterns,
    size_attributes=sizes
)
# Returns: {visual_similarity, pattern_similarity, size_similarity, combined_similarity}
```

### Pattern Compatibility

Related patterns are automatically considered compatible:
- `solid` ↔ `gradient` (solid colors pair well)
- `striped` ↔ `checked` ↔ `plaid` (geometric patterns)
- `floral` ↔ `botanical` (nature patterns)
- `tie_dye` ↔ `abstract` (artistic patterns)
- `polka_dots` ↔ `geometric` (repeating patterns)

### Size/Fit Matching

Groups ensure coherence in:
- **Sleeve type** (short, long, sleeveless, three-quarter)
- **Length** (cropped, above knee, below knee, full length)
- **Fit** (slim, regular, loose, oversized)
- **Aspect ratio** (body proportion match, ±20% tolerance)

---

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