"""
Clothing Classifier Module
Classifies clothing items by type, color, pattern, and size attributes
"""

import numpy as np
from typing import List, Tuple, Dict
from pathlib import Path
from PIL import Image
import config

# Import new detection modules
try:
    from src.pattern_detector import PatternDetector
    from src.size_detector import SizeDetector
    from src.shape_detector import ShapeDetector
except ImportError:
    # Fallback if modules not available
    PatternDetector = None
    SizeDetector = None
    ShapeDetector = None


class ClothingClassifier:
    """Classify clothing items by type, color, pattern, and size"""
    
    def __init__(self):
        """Initialize the classifier"""
        self.clothing_types = config.CLOTHING_TYPES
        self.color_categories = config.COLOR_CATEGORIES
        
        # Initialize pattern and size detectors if available
        if PatternDetector is not None:
            self.pattern_detector = PatternDetector()
        else:
            self.pattern_detector = None
            
        if SizeDetector is not None:
            self.size_detector = SizeDetector()
        else:
            self.size_detector = None
        
        # Initialize shape detector if available
        if ShapeDetector is not None:
            self.shape_detector = ShapeDetector()
        else:
            self.shape_detector = None
        
        # HSV-based color ranges for more accurate detection
        # Format: (color_name, h_min, h_max, s_min, s_max, v_min, v_max)
        # This is more robust than RGB across different lighting
        self.hsv_color_ranges = [
            ('red', 0, 10, 40, 255, 40, 255),
            ('red_dark', 165, 180, 40, 255, 40, 255),
            ('orange', 10, 25, 50, 255, 50, 255),
            ('yellow', 25, 35, 40, 255, 50, 255),
            ('green', 35, 85, 40, 255, 40, 255),
            ('blue', 85, 130, 40, 255, 40, 255),
            ('purple', 130, 160, 40, 255, 40, 255),
            ('pink', 280, 320, 30, 100, 50, 255),
            ('brown', 10, 30, 50, 200, 30, 100),
            ('white', 0, 360, 0, 30, 200, 255),
            ('black', 0, 360, 0, 50, 0, 100),
            ('gray', 0, 360, 0, 50, 100, 200),
        ]
        
        # Type classification thresholds (simplified and more robust)
        # These are used for feature-based fallback only
        self.type_thresholds = {}
    
    def classify_type_from_features(self, features: np.ndarray, aspect_ratio: float = None) -> str:
        """
        Classify clothing type based on deep learning features
        Uses improved heuristics optimized for common types
        
        Args:
            features: Feature vector from CNN
            aspect_ratio: Optional aspect ratio hint from image dimensions
            
        Returns:
            Predicted clothing type
        """
        # Normalize features
        feature_norm = features / (np.linalg.norm(features) + 1e-8)
        
        # Calculate statistics on normalized features
        feature_mean = np.mean(feature_norm)
        feature_std = np.std(feature_norm)
        feature_max = np.max(feature_norm)
        feature_min = np.min(feature_norm)
        
        # Calculate energy (sum of absolute values)
        feature_energy = np.sum(np.abs(feature_norm))
        
        # Improved thresholds for better accuracy
        scores = {}
        
        # Aspect ratio clues
        is_tall = aspect_ratio < 0.6 if aspect_ratio else False
        is_wide = aspect_ratio > 1.6 if aspect_ratio else False
        
        # Type classification logic
        if is_tall:
            # Tall images likely pants, long_dress, or skirt
            if feature_std > 0.25:
                scores['long_dress'] = 0.8
                scores['dress'] = 0.6
            else:
                scores['pants'] = 0.8
                scores['jeans'] = 0.7
        elif is_wide:
            # Wide images likely shorts or shirts
            if feature_mean > 0.15:
                scores['shorts'] = 0.7
            else:
                scores['shirt'] = 0.7
                scores['t-shirt'] = 0.6
        
        # Energy-based classification
        if feature_energy > np.percentile(feature_norm, 75) * len(feature_norm):
            # High energy suggests structured clothing (jacket, suit)
            scores['jacket'] = 0.6
            scores['suit'] = 0.5
        
        # Standard deviation clues
        if feature_std < 0.1:
            # Low variance = solid/simple clothing
            scores['t-shirt'] = scores.get('t-shirt', 0) + 0.5
            scores['sando'] = scores.get('sando', 0) + 0.5
        elif feature_std > 0.3:
            # High variance = complex patterns/structured
            scores['dress'] = scores.get('dress', 0) + 0.5
            scores['blouse'] = scores.get('blouse', 0) + 0.3
        
        # Default scores for common types
        if not scores:
            scores = {
                'shirt': 0.8,
                'polo': 0.7,
                't-shirt': 0.6,
                'pants': 0.6,
                'dress': 0.5
            }
        
        # Return best match
        best_type = max(scores, key=scores.get)
        return best_type if scores[best_type] > 0.3 else 'shirt'
    
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
    
    def classify_pattern(self, image: Image.Image) -> str:
        """
        Classify the pattern of clothing
        
        Args:
            image: PIL Image object
            
        Returns:
            Pattern category name
        """
        if self.pattern_detector is None:
            return 'solid'  # Default fallback
            
        try:
            return self.pattern_detector.detect_pattern(image)
        except Exception as e:
            print(f"Error detecting pattern: {str(e)}")
            return 'other'
    
    def classify_size_attributes(self, image: Image.Image) -> Dict[str, str]:
        """
        Classify size attributes of clothing
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with size attributes
        """
        if self.size_detector is None:
            return {
                'sleeve': 'short_sleeve',
                'length': 'regular_fit',
                'fit': 'regular_fit',
                'aspect_ratio': 1.0
            }
            
        try:
            return self.size_detector.detect_attribute(image)
        except Exception as e:
            print(f"Error detecting size: {str(e)}")
            return {
                'sleeve': 'short_sleeve',
                'length': 'regular_fit',
                'fit': 'regular_fit',
                'aspect_ratio': 1.0
            }
    
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
        Match RGB color to predefined category using HSV color space
        More accurate than RGB matching due to lighting invariance
        
        Args:
            rgb: RGB tuple
            
        Returns:
            Color category name
        """
        from colorsys import rgb_to_hsv
        
        r, g, b = rgb
        
        # Normalize RGB to 0-1 range
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        # Convert to HSV
        h, s, v = rgb_to_hsv(r_norm, g_norm, b_norm)
        
        # Convert to 0-360, 0-255, 0-255 scale
        h = h * 360
        s = s * 255
        v = v * 255
        
        # Check each HSV range
        best_match = 'gray'  # Default fallback
        closest_distance = float('inf')
        
        for color_name, h_min, h_max, s_min, s_max, v_min, v_max in self.hsv_color_ranges:
            # Check if color is within HSV range
            h_match = False
            
            # Handle red wrap-around (0-10 and 165-180)
            if h_min > h_max:  # Wrap-around case (red)
                h_match = (h >= h_min or h <= h_max)
            else:
                h_match = (h_min <= h <= h_max)
            
            s_match = (s_min <= s <= s_max)
            v_match = (v_min <= v <= v_max)
            
            if h_match and s_match and v_match:
                # Perfect match
                return color_name
            
            # Calculate distance for fuzzy matching
            if s_match and v_match:  # Value and saturation match
                if h_min <= h_max:
                    h_dist = min(abs(h - h_min), abs(h - h_max))
                else:  # Wrap-around
                    h_dist = min(min(abs(h - h_min), abs(h - h_max)), 
                                min(abs(h + 360 - h_min), abs(h - 360 - h_max)))
                
                if h_dist < closest_distance:
                    closest_distance = h_dist
                    best_match = color_name
        
        return best_match
    
    def classify_image(self, image_path: Path, features: np.ndarray = None) -> Dict[str, str]:
        """
        Classify type, color, pattern, and size of clothing image
        Now includes advanced shape-based refinement
        
        Args:
            image_path: Path to image file
            features: Optional pre-extracted features
            
        Returns:
            Dictionary with 'type', 'color', 'pattern', and 'size' classifications
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Get aspect ratio for better classification
            width, height = image.size
            aspect_ratio = width / height
            
            # Classify type - first try from filename
            clothing_type = self.classify_type_from_filename(image_path.name)
            
            # If not found in filename and features provided, use features
            if clothing_type == 'other' and features is not None:
                clothing_type = self.classify_type_from_features(features, aspect_ratio)
            
            # SHAPE-BASED REFINEMENT - NEW
            if self.shape_detector is not None:
                try:
                    shape_result = self.shape_detector.detect_shape(image)
                    # Integrate shape detection to refine classification
                    clothing_type = self.shape_detector.integrate_with_classification(
                        shape_result, clothing_type
                    )
                except Exception as e:
                    print(f"Shape detection error (non-critical): {str(e)}")
            
            # Classify color
            color = self.classify_color(image)
            
            # Classify pattern
            pattern = self.classify_pattern(image)
            
            # Classify size attributes
            size_attrs = self.classify_size_attributes(image)
            
            return {
                'type': clothing_type,
                'color': color,
                'pattern': pattern,
                'size': size_attrs.get('length', 'regular_fit'),
                'sleeve': size_attrs.get('sleeve', 'short_sleeve'),
                'fit': size_attrs.get('fit', 'regular_fit'),
                'aspect_ratio': size_attrs.get('aspect_ratio', 1.0)
            }
        except Exception as e:
            print(f"Error classifying {image_path.name}: {str(e)}")
            return {
                'type': 'other',
                'color': 'other',
                'pattern': 'solid',
                'size': 'regular_fit',
                'sleeve': 'short_sleeve',
                'fit': 'regular_fit',
                'aspect_ratio': 1.0
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
