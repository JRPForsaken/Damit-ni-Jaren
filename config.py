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

# Clothing Categories
CLOTHING_TYPES = [
    'shirt',
    'pants',
    'dress',
    'skirt',
    'jacket',
    'coat',
    'sweater',
    'shorts',
    'jeans',
    'blouse',
    't-shirt',
    'hoodie',
    'suit',
    'other'
]

# Color Categories
COLOR_CATEGORIES = [
    'red',
    'blue',
    'green',
    'yellow',
    'black',
    'white',
    'gray',
    'brown',
    'pink',
    'purple',
    'orange',
    'multicolor'
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
