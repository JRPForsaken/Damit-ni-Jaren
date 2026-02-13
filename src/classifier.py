"""
Clothing Classifier Module
Classifies clothing items by type and color
"""

import numpy as np
from typing import List, Tuple, Dict
from pathlib import Path
from PIL import Image
import config


class ClothingClassifier:
    """Classify clothing items by type and color"""
    
    def __init__(self):
        """Initialize the classifier"""
        self.clothing_types = config.CLOTHING_TYPES
        self.color_categories = config.COLOR_CATEGORIES
        
        # Color ranges in RGB for basic classification
        self.color_ranges = {
            'red': ([150, 0, 0], [255, 100, 100]),
            'blue': ([0, 0, 150], [100, 100, 255]),
            'green': ([0, 150, 0], [100, 255, 100]),
            'yellow': ([200, 200, 0], [255, 255, 100]),
            'black': ([0, 0, 0], [50, 50, 50]),
            'white': ([200, 200, 200], [255, 255, 255]),
            'gray': ([50, 50, 50], [200, 200, 200]),
            'brown': ([100, 50, 0], [180, 120, 80]),
            'pink': ([200, 100, 150], [255, 200, 230]),
            'purple': ([100, 0, 150], [200, 100, 255]),
            'orange': ([200, 100, 0], [255, 180, 100]),
        }
    
    def classify_type_from_features(self, features: np.ndarray) -> str:
        """
        Classify clothing type based on deep learning features
        Uses simple heuristics based on feature patterns
        
        Args:
            features: Feature vector from CNN
            
        Returns:
            Predicted clothing type
        """
        # This is a simplified approach
        # In production, you'd train a classifier on labeled data
        # For now, we'll use feature clustering to assign types
        
        # Calculate feature statistics
        feature_mean = np.mean(features)
        feature_std = np.std(features)
        feature_max = np.max(features)
        
        # Simple heuristic-based classification
        # These thresholds would be learned from training data in production
        if feature_mean > 0.15 and feature_std > 0.2:
            return 'jacket'
        elif feature_mean > 0.1 and feature_max > 0.8:
            return 'dress'
        elif feature_std < 0.15:
            return 't-shirt'
        elif feature_mean < 0.05:
            return 'pants'
        else:
            return 'shirt'
    
    def classify_type_from_filename(self, filename: str) -> str:
        """
        Try to classify clothing type from filename
        
        Args:
            filename: Image filename
            
        Returns:
            Predicted clothing type or 'other'
        """
        filename_lower = filename.lower()
        
        for clothing_type in self.clothing_types:
            if clothing_type in filename_lower:
                return clothing_type
        
        return 'other'
    
    def classify_color(self, image: Image.Image) -> str:
        """
        Classify the dominant color of clothing
        
        Args:
            image: PIL Image object
            
        Returns:
            Color category name
        """
        # Get dominant colors
        dominant_colors = self._get_dominant_colors(image, n_colors=1)
        
        if not dominant_colors:
            return 'other'
        
        main_color = dominant_colors[0]
        
        # Match to color category
        return self._match_color_category(main_color)
    
    def _get_dominant_colors(self, image: Image.Image, n_colors: int = 3) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors from image
        
        Args:
            image: PIL Image object
            n_colors: Number of colors to extract
            
        Returns:
            List of RGB tuples
        """
        # Resize for faster processing
        img_small = image.resize((100, 100))
        img_array = np.array(img_small)
        
        # Reshape to list of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Remove very dark and very light pixels (likely background)
        mask = np.logical_and(
            np.all(pixels > 20, axis=1),
            np.all(pixels < 235, axis=1)
        )
        filtered_pixels = pixels[mask]
        
        if len(filtered_pixels) == 0:
            filtered_pixels = pixels
        
        # Simple clustering to find dominant colors
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=min(n_colors, len(filtered_pixels)), 
                          random_state=42, n_init=10)
            kmeans.fit(filtered_pixels)
            colors = kmeans.cluster_centers_.astype(int)
            return [tuple(color) for color in colors]
        except:
            # Fallback: return mean color
            mean_color = np.mean(filtered_pixels, axis=0).astype(int)
            return [tuple(mean_color)]
    
    def _match_color_category(self, rgb: Tuple[int, int, int]) -> str:
        """
        Match RGB color to predefined category
        
        Args:
            rgb: RGB tuple
            
        Returns:
            Color category name
        """
        r, g, b = rgb
        
        # Check each color range
        for color_name, (min_rgb, max_rgb) in self.color_ranges.items():
            if (min_rgb[0] <= r <= max_rgb[0] and
                min_rgb[1] <= g <= max_rgb[1] and
                min_rgb[2] <= b <= max_rgb[2]):
                return color_name
        
        # Check for multicolor (high variance)
        if max(r, g, b) - min(r, g, b) > 100:
            return 'multicolor'
        
        return 'other'
    
    def classify_image(self, image_path: Path, features: np.ndarray = None) -> Dict[str, str]:
        """
        Classify both type and color of clothing image
        
        Args:
            image_path: Path to image file
            features: Optional pre-extracted features
            
        Returns:
            Dictionary with 'type' and 'color' classifications
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Classify type
            # First try from filename
            clothing_type = self.classify_type_from_filename(image_path.name)
            
            # If not found in filename and features provided, use features
            if clothing_type == 'other' and features is not None:
                clothing_type = self.classify_type_from_features(features)
            
            # Classify color
            color = self.classify_color(image)
            
            return {
                'type': clothing_type,
                'color': color
            }
        except Exception as e:
            print(f"Error classifying {image_path.name}: {str(e)}")
            return {
                'type': 'other',
                'color': 'other'
            }
    
    def batch_classify(self, image_paths: List[Path], 
                      features_list: List[np.ndarray] = None) -> List[Dict[str, str]]:
        """
        Classify multiple images
        
        Args:
            image_paths: List of image paths
            features_list: Optional list of pre-extracted features
            
        Returns:
            List of classification dictionaries
        """
        from tqdm import tqdm
        
        results = []
        for i, img_path in enumerate(tqdm(image_paths, desc="Classifying images")):
            features = features_list[i] if features_list is not None else None
            classification = self.classify_image(img_path, features)
            results.append(classification)
        
        return results
    
    def get_color_distribution(self, image: Image.Image) -> Dict[str, float]:
        """
        Get distribution of colors in image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary mapping color names to percentages
        """
        # Get multiple dominant colors
        dominant_colors = self._get_dominant_colors(image, n_colors=5)
        
        # Match each to category
        color_counts = {}
        for color in dominant_colors:
            category = self._match_color_category(color)
            color_counts[category] = color_counts.get(category, 0) + 1
        
        # Convert to percentages
        total = sum(color_counts.values())
        color_distribution = {
            color: (count / total) * 100 
            for color, count in color_counts.items()
        }
        
        return color_distribution
