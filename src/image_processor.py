"""
Image Processor Module
Handles loading, preprocessing, and validation of images
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np
from tqdm import tqdm
import config


class ImageProcessor:
    """Process and prepare images for AI analysis"""
    
    def __init__(self, input_folder: str):
        """
        Initialize the image processor
        
        Args:
            input_folder: Path to folder containing images
        """
        self.input_folder = Path(input_folder)
        self.supported_formats = config.SUPPORTED_FORMATS
        self.image_size = config.IMAGE_SIZE
        self.image_paths = []
        self.valid_images = []
        
    def scan_images(self) -> List[Path]:
        """
        Scan the input folder for valid image files
        
        Returns:
            List of valid image file paths
        """
        print(f"Scanning folder: {self.input_folder}")
        
        if not self.input_folder.exists():
            raise FileNotFoundError(f"Input folder not found: {self.input_folder}")
        
        # Find all image files
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(self.input_folder.rglob(f"*{ext}"))
            image_files.extend(self.input_folder.rglob(f"*{ext.upper()}"))
        
        # Remove duplicates and sort
        image_files = sorted(set(image_files))
        
        print(f"Found {len(image_files)} image files")
        
        # Validate images
        self.image_paths = []
        for img_path in tqdm(image_files, desc="Validating images"):
            if self._validate_image(img_path):
                self.image_paths.append(img_path)
        
        print(f"Valid images: {len(self.image_paths)}")
        return self.image_paths
    
    def _validate_image(self, image_path: Path) -> bool:
        """
        Validate if an image can be opened and processed
        
        Args:
            image_path: Path to image file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            print(f"Invalid image {image_path.name}: {str(e)}")
            return False
    
    def load_image(self, image_path: Path) -> Optional[Image.Image]:
        """
        Load and preprocess a single image
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image object or None if failed
        """
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            return img
        except Exception as e:
            print(f"Error loading {image_path.name}: {str(e)}")
            return None
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array
        """
        # Resize image
        img_resized = image.resize(self.image_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img_resized, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Normalize using ImageNet statistics
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_array = (img_array - mean) / std
        
        return img_array
    
    def load_and_preprocess(self, image_path: Path) -> Optional[Tuple[np.ndarray, Image.Image]]:
        """
        Load and preprocess an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (preprocessed array, original image) or None if failed
        """
        img = self.load_image(image_path)
        if img is None:
            return None
        
        preprocessed = self.preprocess_image(img)
        return preprocessed, img
    
    def get_image_info(self, image_path: Path) -> dict:
        """
        Get metadata about an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with image information
        """
        try:
            img = Image.open(image_path)
            return {
                'path': str(image_path),
                'filename': image_path.name,
                'size': img.size,
                'mode': img.mode,
                'format': img.format,
                'file_size': image_path.stat().st_size
            }
        except Exception as e:
            return {
                'path': str(image_path),
                'filename': image_path.name,
                'error': str(e)
            }
    
    def batch_load_images(self, image_paths: List[Path], batch_size: int = None) -> List[Tuple[Path, np.ndarray]]:
        """
        Load and preprocess multiple images in batches
        
        Args:
            image_paths: List of image paths
            batch_size: Number of images to process at once
            
        Returns:
            List of tuples (path, preprocessed_array)
        """
        if batch_size is None:
            batch_size = config.BATCH_SIZE
        
        results = []
        for img_path in tqdm(image_paths, desc="Loading images"):
            result = self.load_and_preprocess(img_path)
            if result is not None:
                preprocessed, _ = result
                results.append((img_path, preprocessed))
        
        return results
    
    def get_dominant_colors(self, image: Image.Image, n_colors: int = 3) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors from an image
        
        Args:
            image: PIL Image object
            n_colors: Number of dominant colors to extract
            
        Returns:
            List of RGB tuples
        """
        # Resize for faster processing
        img_small = image.resize((100, 100))
        img_array = np.array(img_small)
        
        # Reshape to list of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Simple clustering to find dominant colors
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        return [tuple(color) for color in colors]
