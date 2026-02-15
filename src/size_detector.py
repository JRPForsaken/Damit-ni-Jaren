"""
Size Detector Module
Detects size/aspect ratio attributes of clothing images
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple
from pathlib import Path
import config


class SizeDetector:
    """Detect size and aspect ratio attributes of clothing items"""
    
    def __init__(self):
        """Initialize the size detector"""
        self.attributes = config.CLOTHING_ATTRIBUTES
        
    def detect_attribute(self, image: Image.Image) -> Dict[str, str]:
        """
        Detect size/attribute of a clothing item
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with attribute classifications
        """
        try:
            # Get image dimensions
            width, height = image.size
            aspect_ratio = width / height
            
            # Detect sleeve length
            sleeve_length = self._detect_sleeve_length(image)
            
            # Detect length category
            length_category = self._detect_length_category(aspect_ratio)
            
            # Detect fit type
            fit_type = self._detect_fit_type(image)
            
            return {
                'sleeve': sleeve_length,
                'length': length_category,
                'fit': fit_type,
                'aspect_ratio': aspect_ratio
            }
            
        except Exception as e:
            print(f"Error detecting size: {str(e)}")
            return {
                'sleeve': 'other',
                'length': 'other',
                'fit': 'regular_fit',
                'aspect_ratio': 1.0
            }
    
    def _detect_sleeve_length(self, image: Image.Image) -> str:
        """
        Detect sleeve length from image
        
        Args:
            image: PIL Image object
            
        Returns:
            Sleeve length category
        """
        try:
            # Resize for analysis
            img_small = image.resize((128, 128))
            img_array = np.array(img_small)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            h, w = gray.shape
            
            # Analyze top vs bottom regions
            # Sleeve length affects the upper portion of the image
            
            # Divide image into top, middle, bottom sections
            top_section = gray[:h//4, :]
            middle_section = gray[h//4:3*h//4, :]
            bottom_section = gray[3*h//4:, :]
            
            # Calculate variance in each section
            top_var = np.var(top_section)
            middle_var = np.var(middle_section)
            bottom_var = np.var(bottom_section)
            
            # Calculate edge density in each section
            from scipy import ndimage
            
            # Simple gradient
            grad_y = np.abs(np.diff(gray, axis=0))
            grad_x = np.abs(np.diff(gray, axis=1))
            
            # Top portion edge density (sleeves)
            top_edges = np.mean(grad_y[:h//4, :]) if h > 4 else 0
            middle_edges = np.mean(grad_y[h//4:3*h//4, :]) if h > 4 else 0
            bottom_edges = np.mean(grad_y[3*h//4:, :]) if h > 4 else 0
            
            # Analyze sleeve presence
            total_height = h
            
            # Sleeveless: low variance in top section, more skin-like
            if top_var < 500 and middle_var > 800:
                return 'sleeveless'
            
            # Short sleeve: moderate edges in top section
            if top_edges > middle_edges * 0.7:
                return 'short_sleeve'
            
            # Three quarter sleeve
            if top_edges > middle_edges * 0.4 and bottom_var > 1000:
                return 'three_quarter'
            
            # Cap sleeve (very short)
            if top_edges > middle_edges * 0.5 and top_var < middle_var:
                return 'cap_sleeve'
            
            # Long sleeve: high edge density in top section
            if top_edges > middle_edges * 0.5:
                return 'long_sleeve'
            
            # Default
            return 'short_sleeve'
            
        except Exception as e:
            print(f"Error detecting sleeve length: {str(e)}")
            return 'short_sleeve'
    
    def _detect_length_category(self, aspect_ratio: float) -> str:
        """
        Detect length category based on aspect ratio
        
        Args:
            aspect_ratio: Width/Height ratio
            
        Returns:
            Length category
        """
        # Aspect ratio interpretation:
        # < 0.5: Very tall item (long dress, gown)
        # 0.5 - 0.7: Moderate length (midi, pants)
        # 0.7 - 1.0: Standard (shirt, skirt)
        # > 1.0: Wide item (wide pants, cape)
        
        if aspect_ratio < 0.5:
            # Very long items
            return 'full_length'
        elif aspect_ratio < 0.65:
            # Below knee / Midi
            return 'below_knee'
        elif aspect_ratio < 0.8:
            # Above knee / Standard
            return 'above_knee'
        elif aspect_ratio < 1.2:
            # Regular length
            return 'regular_fit'
        else:
            # Very wide or cropped
            return 'cropped'
    
    def _detect_fit_type(self, image: Image.Image) -> str:
        """
        Detect fit type (slim, loose, regular, etc.)
        
        Args:
            image: PIL Image object
            
        Returns:
            Fit type category
        """
        try:
            # Resize for analysis
            img_small = image.resize((128, 128))
            img_array = np.array(img_small)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            h, w = gray.shape
            
            # Analyze edge density - tighter fit = more defined edges
            from scipy import ndimage
            
            # Sobel edges
            sobel_x = ndimage.sobel(gray, axis=1)
            sobel_y = ndimage.sobel(gray, axis=0)
            edges = np.sqrt(sobel_x**2 + sobel_y**2)
            
            edge_density = np.mean(edges > 20)
            edge_variance = np.var(edges)
            
            # Analyze center vs edges (for silhouette)
            center_h, center_w = h // 4, w // 4
            center_region = gray[center_h:h-center_h, center_w:w-center_w]
            edge_region_h = np.concatenate([gray[:h//4, :], gray[3*h//4:, :]])
            edge_region_w = np.concatenate([gray[:, :w//4], gray[:, 3*w//4:]], axis=0)
            
            center_variance = np.var(center_region)
            edge_variance_h = np.var(edge_region_h)
            
            # Fit detection
            if edge_density > 0.4 and edge_variance > 500:
                # High edge density suggests tailored/slim fit
                if edge_density > 0.6:
                    return 'slim_fit'
                else:
                    return 'tailored'
            elif edge_density < 0.2 and center_variance < 500:
                # Low edges, low variance = loose/baggy
                return 'loose_fit'
            elif edge_density > 0.5 and center_variance > 800:
                # High edges with high center variance = bulky/oversized
                return 'oversized'
            else:
                return 'regular_fit'
                
        except Exception as e:
            print(f"Error detecting fit type: {str(e)}")
            return 'regular_fit'
    
    def get_clothing_dimension_category(self, width: int, height: int) -> str:
        """
        Get dimension category based on actual pixel dimensions
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            Dimension category
        """
        aspect_ratio = width / height
        
        if aspect_ratio > 1.5:
            # Very wide (capes, wide pants)
            return 'extra_wide'
        elif aspect_ratio > 1.2:
            # Wide items
            return 'wide'
        elif aspect_ratio > 0.8:
            # Standard
            return 'standard'
        elif aspect_ratio > 0.6:
            # Tall items
            return 'tall'
        else:
            # Very tall
            return 'extra_tall'
    
    def batch_detect_attributes(self, image_paths: List[Path]) -> Dict[str, Dict[str, str]]:
        """
        Detect attributes for multiple images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            Dictionary mapping image path to attributes
        """
        from tqdm import tqdm
        
        results = {}
        for img_path in tqdm(image_paths, desc="Detecting sizes"):
            try:
                image = Image.open(img_path).convert('RGB')
                attributes = self.detect_attribute(image)
                results[str(img_path)] = attributes
            except Exception as e:
                print(f"Error processing {img_path.name}: {str(e)}")
                results[str(img_path)] = {
                    'sleeve': 'other',
                    'length': 'other',
                    'fit': 'regular_fit',
                    'aspect_ratio': 1.0
                }
        
        return results
    
    def get_attribute_distribution(self, attributes_list: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
        """
        Get distribution of attributes
        
        Args:
            attributes_list: List of attribute dictionaries
            
        Returns:
            Dictionary with distributions for each attribute type
        """
        sleeve_dist = {}
        length_dist = {}
        fit_dist = {}
        
        for attrs in attributes_list:
            sleeve = attrs.get('sleeve', 'other')
            length = attrs.get('length', 'other')
            fit = attrs.get('fit', 'regular_fit')
            
            sleeve_dist[sleeve] = sleeve_dist.get(sleeve, 0) + 1
            length_dist[length] = length_dist.get(length, 0) + 1
            fit_dist[fit] = fit_dist.get(fit, 0) + 1
        
        return {
            'sleeve': sleeve_dist,
            'length': length_dist,
            'fit': fit_dist
        }
    
    def estimate_real_world_size(self, image: Image.Image, known_item_type: str = None) -> Dict[str, str]:
        """
        Estimate real-world size based on aspect ratio and item type
        
        Args:
            image: PIL Image object
            known_item_type: Known clothing type (optional)
            
        Returns:
            Size estimation dictionary
        """
        width, height = image.size
        aspect_ratio = width / height
        
        # Base estimates on common clothing proportions
        estimates = {
            'estimated_category': self.get_clothing_dimension_category(width, height),
            'aspect_ratio': round(aspect_ratio, 2),
            'proportions': 'unknown'
        }
        
        # Refine based on known type if provided
        if known_item_type:
            if known_item_type in ['dress', 'gown', 'maxi', 'robe']:
                if aspect_ratio < 0.3:
                    estimates['proportions'] = 'maxi_gown'
                elif aspect_ratio < 0.5:
                    estimates['proportions'] = 'midi_dress'
                else:
                    estimates['proportions'] = 'mini_dress'
            elif known_item_type in ['pants', 'jeans', 'capri', 'shorts']:
                if aspect_ratio < 0.5:
                    estimates['proportions'] = 'shorts'
                elif aspect_ratio < 0.7:
                    estimates['proportions'] = 'capri'
                elif aspect_ratio < 1.0:
                    estimates['proportions'] = 'pants'
                else:
                    estimates['proportions'] = 'wide_leg_pants'
            elif known_item_type in ['skirt', 'mini', 'maxi']:
                if aspect_ratio < 0.5:
                    estimates['proportions'] = 'maxi_skirt'
                elif aspect_ratio < 0.8:
                    estimates['proportions'] = 'midi_skirt'
                else:
                    estimates['proportions'] = 'mini_skirt'
        
        return estimates
