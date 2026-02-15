"""
Configuration file for AI Clothing Photo Sorter
"""

import os

# Application Settings
APP_NAME = "AI Clothing Photo Sorter"
APP_VERSION = "1.0.0"

# Image Processing Settings
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
IMAGE_SIZE = (224, 224)  # Standard size for ResNet
BATCH_SIZE = 32

# AI Model Settings
MODEL_NAME = 'resnet50'  # Pre-trained model
FEATURE_DIM = 2048  # ResNet50 feature dimension
USE_GPU = True  # Use GPU if available

# Clustering Settings
SIMILARITY_THRESHOLD = 0.85  # Cosine similarity threshold for grouping same items
MIN_CLUSTER_SIZE = 2  # Minimum images to form a cluster
CLUSTERING_METHOD = 'dbscan'  # 'dbscan' or 'kmeans'

# Clothing Categories - Philippine Context (Common Types)
CLOTHING_TYPES = [
    'shirt',          # Most common - casual/formal shirts
    'polo',           # Very popular in Philippines
    't-shirt',        # Everyday wear
    'blouse',         # Women's casual/formal
    'pants',          # Trousers
    'jeans',          # Denim pants
    'shorts',         # Short pants
    'skirt',          # Women's bottoms
    'dress',          # One-piece dress
    'long_dress',     # Maxi-style dress
    'short_dress',    # Mini-style dress
    'romper',         # Casual one-piece
    'jacket',         # Light jacket/blazer
    'cardigan',       # Sweater cardigan
    'sweater',        # Pullover sweater
    'hoodie',         # Hood sweater
    'vest',           # Sleeveless shirt
    'tank_top',       # Sleeveless casual
    'sando',          # Undershirt/tank top (Filipino term)
    'barong',         # Traditional formal shirt (Philippines)
    'terno',          # Formal dress ensemble (Philippines)
    'duster',         # Long light cover-up
    'shawl',          # Wrap/shawl
    'kimono',         # Asian casual wear
    'suit',           # Formal suit
    'coat',           # Heavy outer wear
    'leggings',       # Tight pants
    'bermuda',        # Knee-length shorts
    'cargo',          # Multi-pocket pants/shorts
    'other'           # Unclassified
]

# Clothing Patterns
CLOTHING_PATTERNS = [
    'solid',
    'striped',
    'checked',
    'plaid',
    'floral',
    'polka_dots',
    'paisley',
    'geometric',
    'abstract',
    'gradient',
    'tie_dye',
    'embroidered',
    'printed',
    'other'
]

# Clothing Attributes (Size/Length)
CLOTHING_ATTRIBUTES = [
    'short_sleeve',
    'long_sleeve',
    'sleeveless',
    'three_quarter',
    'cap_sleeve',
    'full_length',
    'cropped',
    'above_knee',
    'below_knee',
    'ankle_length',
    'regular_fit',
    'slim_fit',
    'loose_fit',
    'oversized',
    'tailored'
]

# Color Categories - Improved for accuracy
COLOR_CATEGORIES = [
    'red',
    'orange', 
    'yellow',
    'green',
    'blue',
    'purple',
    'pink',
    'brown',
    'black',
    'white',
    'gray'
]

# Output Settings
OUTPUT_FOLDER_NAME = "sorted_clothes"
REPORT_FORMAT = 'both'  # 'csv', 'html', or 'both'
RENAME_PATTERN = "{type}_{color}_{id:04d}"  # e.g., shirt_blue_0001.jpg

# File Organization
COPY_FILES = True  # True to copy, False to move
CREATE_SUBFOLDERS = True  # Create subfolders for each clothing type
GROUP_SIMILAR_ITEMS = True  # Group same items from different angles

# Logging
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = 'clothing_sorter.log'

# Performance
MAX_WORKERS = 4  # Number of parallel workers for processing
CACHE_FEATURES = True  # Cache extracted features to speed up re-runs

# Path Caching
CACHE_FILE = '.clothing_sorter_cache.json'  # File to store last used paths
SAVE_LAST_PATHS = True  # Save last used input/output paths

# Advanced AI Models
AVAILABLE_MODELS = {
    'resnet50': {
        'name': 'ResNet50 (Fast)',
        'feature_dim': 2048,
        'speed': 'fast',
        'accuracy': 'good',
        'description': 'Balanced speed and accuracy - recommended for most users'
    },
    'efficientnet_b7': {
        'name': 'EfficientNet-B7 (Accurate)',
        'feature_dim': 2560,
        'speed': 'slow',
        'accuracy': 'excellent',
        'description': 'Slower but more accurate - best for professional use'
    },
    'resnet18': {
        'name': 'ResNet18 (Very Fast)',
        'feature_dim': 512,
        'speed': 'very_fast',
        'accuracy': 'moderate',
        'description': 'Fastest option - good for quick sorting of large batches'
    }
}
DEFAULT_MODEL = 'resnet50'  # Default model for new users
