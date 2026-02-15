"""
Shape Detector Module
Analyzes clothing shape/silhouette to improve classification accuracy
Handles incomplete/folded items and distinguishes similar textures
"""

import numpy as np
from PIL import Image
import cv2
from typing import Dict, Tuple, List
import config


class ShapeDetector:
    """Detect shape/silhouette characteristics of clothing items"""
    
    def __init__(self):
        """Initialize the shape detector"""
        self.min_area_ratio = 0.1  # Minimum clothing area % of image
        
    def detect_shape(self, image: Image.Image) -> Dict[str, any]:
        """
        Detect shape characteristics of clothing
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with shape analysis results
        """
        try:
            # Convert to numpy array
            img_array = np.array(image.convert('RGB'))
            
            # Get foreground (clothing area)
            foreground = self._extract_foreground(img_array)
            
            if foreground is None:
                return {
                    'shape_type': 'unknown',
                    'completeness': 0.5,
                    'aspect_ratio': image.size[0] / image.size[1],
                    'width_variation': 0.0,
                    'is_folded': False,
                    'detected_edges': 0,
                    'fill_ratio': 0.0
                }
            
            # Analyze shape characteristics
            shape_metrics = {
                'shape_type': self._classify_shape_type(foreground),
                'completeness': self._detect_completeness(foreground),
                'aspect_ratio': image.size[0] / image.size[1],
                'width_variation': self._detect_width_variation(foreground),
                'is_folded': self._detect_folding(foreground),
                'detected_edges': self._count_edges(foreground),
                'fill_ratio': self._calculate_fill_ratio(foreground),
                'symmetry': self._analyze_symmetry(foreground),
                'contour_complexity': self._calculate_contour_complexity(foreground)
            }
            
            return shape_metrics
            
        except Exception as e:
            print(f"Error detecting shape: {str(e)}")
            return {
                'shape_type': 'unknown',
                'completeness': 0.5,
                'aspect_ratio': image.size[0] / image.size[1],
                'width_variation': 0.0,
                'is_folded': False,
                'detected_edges': 0,
                'fill_ratio': 0.0
            }
    
    def _extract_foreground(self, img_array: np.ndarray) -> np.ndarray:
        """
        Extract foreground (clothing) from background
        
        Args:
            img_array: Image as numpy array
            
        Returns:
            Binary mask of foreground
        """
        try:
            # Convert to HSV for better background separation
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Create mask for non-background colors
            # Ignore pure white, pure black, and gray background
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])
            mask_white = cv2.inRange(hsv, lower_white, upper_white)
            
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([180, 255, 50])
            mask_black = cv2.inRange(hsv, lower_black, upper_black)
            
            # Combine masks - keep colored items, remove white/black background
            fg_mask = 255 - cv2.bitwise_or(mask_white, mask_black)
            
            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            
            return fg_mask
            
        except Exception as e:
            print(f"Error extracting foreground: {str(e)}")
            return None
    
    def _classify_shape_type(self, foreground: np.ndarray) -> str:
        """
        Classify shape type based on silhouette
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Shape type: 'shirt', 'pants', 'dress', 'folded', etc.
        """
        h, w = foreground.shape
        
        # Find contours
        contours, _ = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 'unknown'
        
        # Get largest contour
        main_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(main_contour)
        
        # Get bounding rectangle
        x, y, bbox_w, bbox_h = cv2.boundingRect(main_contour)
        
        # Aspect ratio of bounding box
        bbox_aspect = bbox_w / (bbox_h + 1)
        
        # Fill ratio (contour area vs bounding box area)
        fill_ratio = area / (bbox_w * bbox_h + 1) if (bbox_w * bbox_h) > 0 else 0
        
        # Fit ellipse if possible
        if len(main_contour) > 5:
            ellipse = cv2.fitEllipse(main_contour)
            ellipse_w, ellipse_h = ellipse[1]
            ellipse_aspect = ellipse_w / (ellipse_h + 1)
        else:
            ellipse_aspect = bbox_aspect
        
        # Classification logic
        # Tall and thin = pants/jeans
        if bbox_aspect < 0.7 and bbox_h > w * 0.6:
            return 'pants'
        
        # Square-ish and tall = shirt/blouse
        elif 0.6 < bbox_aspect < 1.2 and bbox_h < w * 0.8:
            return 'shirt'
        
        # Very tall and thin = long_dress
        elif bbox_aspect < 0.6 and bbox_h > w * 0.7:
            return 'dress'
        
        # Wide and short = shorts/skirt
        elif bbox_aspect > 1.0 and bbox_h < w * 0.5:
            return 'shorts'
        
        # Wide and medium height = jacket/coat
        elif bbox_aspect > 1.0 and 0.4 < fill_ratio < 0.8:
            return 'jacket'
        
        return 'unknown'
    
    def _detect_completeness(self, foreground: np.ndarray) -> float:
        """
        Detect how complete/intact the clothing item is
        Incomplete items return lower score (e.g., cropped edges)
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Completeness score (0-1), where 1 is complete
        """
        h, w = foreground.shape
        
        # Check if clothing touches edges (suggests cropping/incompleteness)
        top_edge = np.sum(foreground[0:2, :]) > 0
        bottom_edge = np.sum(foreground[-2:, :]) > 0
        left_edge = np.sum(foreground[:, 0:2]) > 0
        right_edge = np.sum(foreground[:, -2:]) > 0
        
        # Count edges touched
        edges_touched = sum([top_edge, bottom_edge, left_edge, right_edge])
        
        # More edges touched = less complete
        completeness = 1.0 - (edges_touched * 0.15)
        
        # Check for large holes (suggests folding or damage)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        filled = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, kernel)
        
        holes = np.sum(filled > 0) - np.sum(foreground > 0)
        hole_ratio = holes / (np.sum(filled > 0) + 1)
        
        if hole_ratio > 0.1:
            completeness *= 0.8  # Reduce completeness if significant holes
        
        return max(0.0, min(1.0, completeness))
    
    def _detect_width_variation(self, foreground: np.ndarray) -> float:
        """
        Detect variation in width across height
        High variation = pants/jeans; Low variation = shirt
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Width variation score (0-1)
        """
        h, w = foreground.shape
        
        # Divide into horizontal sections
        section_height = max(1, h // 10)
        widths = []
        
        for i in range(0, h, section_height):
            section = foreground[i:min(i+section_height, h), :]
            width = np.sum(np.any(section > 0, axis=0))
            widths.append(width)
        
        if not widths or len(widths) < 2:
            return 0.0
        
        # Calculate coefficient of variation
        widths = np.array(widths)
        if np.mean(widths) == 0:
            return 0.0
        
        variation = np.std(widths) / (np.mean(widths) + 1)
        
        return min(1.0, variation)
    
    def _detect_folding(self, foreground: np.ndarray) -> bool:
        """
        Detect if clothing is folded (multiple overlapping layers)
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            True if likely folded, False otherwise
        """
        try:
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(foreground.astype(np.uint8), (11, 11), 0)
            
            # Detect edges
            edges = cv2.Canny(blurred, 50, 150)
            
            # Count edge pixels - high count suggests folding/layering
            edge_density = np.sum(edges > 0) / (foreground.shape[0] * foreground.shape[1])
            
            # If lots of edges, likely folded
            is_folded = edge_density > 0.15
            
            return is_folded
        except:
            return False
    
    def _count_edges(self, foreground: np.ndarray) -> int:
        """
        Count number of contour edges (detect multiple layers)
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Number of distinct edges/contours detected
        """
        contours, _ = cv2.findContours(foreground, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter by area to get meaningful contours
        min_area = np.sum(foreground > 0) * 0.05
        significant_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        return len(significant_contours)
    
    def _calculate_fill_ratio(self, foreground: np.ndarray) -> float:
        """
        Calculate how much of the image is filled with clothing
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Fill ratio (0-1)
        """
        total_pixels = foreground.shape[0] * foreground.shape[1]
        filled_pixels = np.sum(foreground > 0)
        
        return filled_pixels / (total_pixels + 1)
    
    def _analyze_symmetry(self, foreground: np.ndarray) -> float:
        """
        Analyze vertical symmetry (shirts more symmetric than pants)
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Symmetry score (0-1), where 1 is perfectly symmetric
        """
        h, w = foreground.shape
        
        # Split into left and right halves
        mid = w // 2
        left_half = foreground[:, :mid]
        right_half = np.fliplr(foreground[:, mid:])
        
        # Resize right half to match left if needed
        if right_half.shape[1] != left_half.shape[1]:
            right_half = right_half[:, :left_half.shape[1]]
        
        # Calculate similarity
        total_pixels = np.sum(np.logical_or(left_half > 0, right_half > 0))
        matching_pixels = np.sum(np.logical_and(left_half > 0, right_half > 0))
        
        symmetry = matching_pixels / (total_pixels + 1)
        
        return symmetry
    
    def _calculate_contour_complexity(self, foreground: np.ndarray) -> float:
        """
        Calculate complexity of contour (simple = shirt, complex = jacket with details)
        
        Args:
            foreground: Binary mask of foreground
            
        Returns:
            Complexity score (0-1)
        """
        contours, _ = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0.0
        
        main_contour = max(contours, key=cv2.contourArea)
        
        # Calculate perimeter and area
        perimeter = cv2.arcLength(main_contour, True)
        area = cv2.contourArea(main_contour)
        
        # Contour complexity = perimeter^2 / area (isoperimetric quotient)
        if area > 0:
            complexity = (perimeter ** 2) / (4 * np.pi * area)
            # Normalize to 0-1 range (circle has complexity ~1, complex shapes have higher)
            complexity = min(1.0, complexity / 5)
        else:
            complexity = 0.0
        
        return complexity
    
    def integrate_with_classification(self, shape_result: Dict, 
                                     current_type: str) -> str:
        """
        Refine clothing type classification using shape information
        
        Args:
            shape_result: Shape detection results
            current_type: Initially classified clothing type
            
        Returns:
            Refined clothing type
        """
        shape_type = shape_result.get('shape_type', 'unknown')
        completeness = shape_result.get('completeness', 0.5)
        width_variation = shape_result.get('width_variation', 0.0)
        is_folded = shape_result.get('is_folded', False)
        symmetry = shape_result.get('symmetry', 0.5)
        contour_complexity = shape_result.get('contour_complexity', 0.0)
        
        # If incomplete/folded, boost base detection
        if not is_folded and completeness > 0.8:
            # Use shape type if confident
            if shape_type in ['shirt', 'pants', 'dress', 'shorts', 'jacket']:
                return shape_type
        
        # High width variation with tall shape = pants/jeans not shorts
        if width_variation > 0.3 and shape_type == 'pants':
            return 'pants'
        
        # Wide with low width variation and medium height = shorts
        if width_variation < 0.25 and shape_type == 'shorts':
            return 'shorts'
        
        # Distinguish jacket from shirt by complexity and fill
        if shape_type == 'jacket' or current_type == 'jacket':
            if contour_complexity > 0.4 or is_folded:
                return 'jacket'
            elif symmetry > 0.7:
                return 'shirt'
        
        # Return original if shape doesn't give clear signal
        return current_type
