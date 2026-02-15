"""
Pattern Detector Module
Detects patterns in clothing images (stripes, checks, floral, solid, etc.)
"""

import numpy as np
from PIL import Image
from typing import Dict, List, Tuple
from pathlib import Path
import config


class PatternDetector:
    """Detect patterns in clothing images"""
    
    def __init__(self):
        """Initialize the pattern detector"""
        self.patterns = config.CLOTHING_PATTERNS
        
    def detect_pattern(self, image: Image.Image) -> str:
        """
        Detect the pattern of a clothing item
        
        Args:
            image: PIL Image object
            
        Returns:
            Pattern category name
        """
        try:
            # Resize for faster processing
            img_small = image.resize((128, 128))
            img_array = np.array(img_small)
            
            # Convert to grayscale for pattern analysis
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Analyze different pattern types
            pattern_scores = {
                'solid': self._detect_solid(gray),
                'striped': self._detect_stripes(gray),
                'checked': self._detect_checks(gray),
                'plaid': self._detect_plaid(gray),
                'floral': self._detect_floral(img_array),
                'polka_dots': self._detect_polka_dots(gray),
                'paisley': self._detect_paisley(gray),
                'geometric': self._detect_geometric(gray),
                'abstract': self._detect_abstract(img_array),
                'gradient': self._detect_gradient(gray),
                'tie_dye': self._detect_tie_dye(img_array),
                'embroidered': self._detect_embroidered(gray),
                'printed': self._detect_printed(gray)
            }
            
            # Return the pattern with highest score
            best_pattern = max(pattern_scores, key=pattern_scores.get)
            confidence = pattern_scores[best_pattern]
            
            # If confidence is too low, return 'other'
            if confidence < 0.3:
                return 'other'
                
            return best_pattern
            
        except Exception as e:
            print(f"Error detecting pattern: {str(e)}")
            return 'other'
    
    def _detect_solid(self, gray: np.ndarray) -> float:
        """
        Detect if image is solid color (no pattern)
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Calculate variance - low variance means solid color
        variance = np.var(gray)
        
        # Normalize to 0-1 range
        # Typical variance for solid colors is < 500
        score = max(0, 1 - (variance / 1000))
        return score
    
    def _detect_stripes(self, gray: np.ndarray) -> float:
        """
        Detect stripes (horizontal or vertical)
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Compute horizontal and vertical gradients
        h, w = gray.shape
        
        # Horizontal stripes - look for repeating pattern in rows
        horizontal_variance = np.var(gray, axis=1)
        horizontal_pattern = np.std(horizontal_variance)
        
        # Vertical stripes - look for repeating pattern in columns
        vertical_variance = np.var(gray, axis=0)
        vertical_pattern = np.std(vertical_variance)
        
        # Check for periodic patterns using FFT
        try:
            # Horizontal direction
            fft_h = np.abs(np.fft.fft(horizontal_variance - np.mean(horizontal_variance)))
            fft_h = fft_h[:len(fft_h)//2]
            peak_h = np.max(fft_h) if len(fft_h) > 0 else 0
            
            # Vertical direction
            fft_v = np.abs(np.fft.fft(vertical_variance - np.mean(vertical_variance)))
            fft_v = fft_v[:len(fft_v)//2]
            peak_v = np.max(fft_v) if len(fft_v) > 0 else 0
            
            # Combine scores
            score = min(1, (peak_h + peak_v) / 5000)
            return score
        except:
            return (horizontal_pattern + vertical_pattern) / 100
    
    def _detect_checks(self, gray: np.ndarray) -> float:
        """
        Detect checkered patterns
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Look for grid-like structure
        h, w = gray.shape
        
        # Divide into grid and check consistency
        grid_size = 16
        h_blocks = h // grid_size
        w_blocks = w // grid_size
        
        if h_blocks < 2 or w_blocks < 2:
            return 0.0
        
        # Calculate mean of each block
        block_means = np.zeros((h_blocks, w_blocks))
        for i in range(h_blocks):
            for j in range(w_blocks):
                block = gray[i*grid_size:(i+1)*grid_size, j*grid_size:(j+1)*grid_size]
                block_means[i, j] = np.mean(block)
        
        # Check for alternating pattern
        alternating_score = 0
        for i in range(h_blocks - 1):
            for j in range(w_blocks - 1):
                # Check if adjacent blocks have different values (check pattern)
                diff1 = abs(block_means[i, j] - block_means[i+1, j+1])
                diff2 = abs(block_means[i+1, j] - block_means[i, j+1])
                if diff1 > 20 and diff2 > 20:
                    alternating_score += 1
        
        total_pairs = (h_blocks - 1) * (w_blocks - 1)
        score = alternating_score / max(total_pairs, 1)
        
        return min(1, score * 2)
    
    def _detect_plaid(self, gray: np.ndarray) -> float:
        """
        Detect plaid patterns (overlapping stripes)
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Plaid is essentially overlapping stripes
        stripe_score = self._detect_stripes(gray)
        check_score = self._detect_checks(gray)
        
        # Plaid should have characteristics of both
        score = (stripe_score * 0.6 + check_score * 0.4)
        
        return min(1, score)
    
    def _detect_floral(self, rgb: np.ndarray) -> float:
        """
        Detect floral patterns
        
        Args:
            rgb: RGB image array
            
        Returns:
            Confidence score (0-1)
        """
        # Look for high frequency color variations (flowers)
        if len(rgb.shape) != 3:
            return 0.0
        
        h, w, c = rgb.shape
        
        # Convert to HSV-like representation
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        
        # Look for distinct color blobs
        color_variance = np.var(rgb, axis=(0,1))
        overall_variance = np.mean(color_variance)
        
        # High color variation with some spatial regularity could indicate floral
        if overall_variance > 500:
            # Check for blob-like structures
            small_blobs = 0
            for i in range(0, h-8, 8):
                for j in range(0, w-8, 8):
                    block = rgb[i:i+8, j:j+8]
                    block_mean = np.mean(block, axis=(0,1))
                    block_var = np.var(block, axis=(0,1))
                    if np.mean(block_var) > 500:
                        small_blobs += 1
            
            blob_ratio = small_blobs / max((h//8) * (w//8), 1)
            return min(1, blob_ratio * 3)
        
        return 0.0
    
    def _detect_polka_dots(self, gray: np.ndarray) -> float:
        """
        Detect polka dot patterns
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Look for regular circular patterns
        h, w = gray.shape
        
        # Compute local maxima (potential dots)
        from scipy import ndimage
        
        # Simple local contrast
        local_mean = ndimage.uniform_filter(gray, size=7)
        local_diff = np.abs(gray - local_mean)
        
        # Find local maxima
        threshold = np.mean(local_diff) + np.std(local_diff)
        dots = local_diff > threshold
        
        # Count dot-like regions
        labeled, num_features = ndimage.label(dots)
        
        if num_features == 0:
            return 0.0
        
        # Check if dots are roughly evenly spaced
        dot_positions = np.argwhere(dots)
        if len(dot_positions) < 4:
            return 0.0
        
        # Calculate average distance between dots
        avg_distance = 0
        for i in range(min(100, len(dot_positions))):
            distances = np.sqrt(np.sum((dot_positions - dot_positions[i])**2, axis=1))
            avg_distance += np.median(distances)
        
        avg_distance /= min(100, len(dot_positions))
        
        # Regular spacing suggests polka dots
        expected_dots = (h * w) / (avg_distance ** 2) if avg_distance > 0 else 0
        ratio = num_features / max(expected_dots, 1)
        
        return min(1, ratio)
    
    def _detect_paisley(self, gray: np.ndarray) -> float:
        """
        Detect paisley patterns (curved, teardrop shapes)
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Paisley is complex - detect using texture complexity
        from scipy import ndimage
        
        # Sobel edges
        sobel_x = ndimage.sobel(gray, axis=1)
        sobel_y = ndimage.sobel(gray, axis=0)
        edges = np.sqrt(sobel_x**2 + sobel_y**2)
        
        edge_density = np.mean(edges > 20)
        
        # High edge density with curved appearance
        if edge_density > 0.3 and edge_density < 0.7:
            return 0.5
        
        return 0.0
    
    def _detect_geometric(self, gray: np.ndarray) -> float:
        """
        Detect geometric patterns
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        from scipy import ndimage
        
        # Look for strong edges and regular shapes
        edges = ndimage.sobel(gray)
        edge_strength = np.mean(np.abs(edges))
        
        # Look for straight lines (Hough transform would be ideal, but use approximation)
        h, w = gray.shape
        
        # Check horizontal and vertical lines
        horizontal_lines = np.sum(np.abs(np.diff(gray, axis=1)) > 30) / (h * (w-1))
        vertical_lines = np.sum(np.abs(np.diff(gray, axis=0)) > 30) / ((h-1) * w)
        
        if edge_strength > 20 and (horizontal_lines > 0.1 or vertical_lines > 0.1):
            return min(1, (horizontal_lines + vertical_lines))
        
        return 0.0
    
    def _detect_abstract(self, rgb: np.ndarray) -> float:
        """
        Detect abstract patterns
        
        Args:
            rgb: RGB image array
            
        Returns:
            Confidence score (0-1)
        """
        # Abstract patterns are irregular and colorful
        if len(rgb.shape) != 3:
            return 0.0
        
        # High color variation but no regular structure
        color_variance = np.var(rgb, axis=(0,1))
        overall_variance = np.mean(color_variance)
        
        # Check for irregular texture
        gray = np.mean(rgb, axis=2)
        texture_variance = np.var(gray)
        
        if overall_variance > 300 and texture_variance > 500:
            # Not solid, not striped, not checks - could be abstract
            solid_score = self._detect_solid(gray)
            stripe_score = self._detect_stripes(gray)
            check_score = self._detect_checks(gray)
            
            if solid_score < 0.7 and stripe_score < 0.5 and check_score < 0.5:
                return 0.6
        
        return 0.0
    
    def _detect_gradient(self, gray: np.ndarray) -> float:
        """
        Detect gradient patterns
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        h, w = gray.shape
        
        # Check for smooth transitions
        # Horizontal gradient
        horizontal_diff = np.abs(np.diff(gray, axis=1))
        h_smoothness = np.mean(horizontal_diff < 10)
        
        # Vertical gradient
        vertical_diff = np.abs(np.diff(gray, axis=0))
        v_smoothness = np.mean(vertical_diff < 10)
        
        # Check if there's a clear direction of change
        h_mean = np.mean(horizontal_diff)
        v_mean = np.mean(vertical_diff)
        
        # Gradient should have smooth transitions
        if h_smoothness > 0.7 or v_smoothness > 0.7:
            # Check if there's actually some change (not completely flat)
            if np.var(gray) > 100:
                return 0.7
        
        return 0.0
    
    def _detect_tie_dye(self, rgb: np.ndarray) -> float:
        """
        Detect tie-dye patterns
        
        Args:
            rgb: RGB image array
            
        Returns:
            Confidence score (0-1)
        """
        if len(rgb.shape) != 3:
            return 0.0
        
        # Look for radial or circular color patterns
        h, w, _ = rgb.shape
        center_h, center_w = h // 2, w // 2
        
        # Calculate distance from center for each pixel
        y, x = np.ogrid[:h, :w]
        distances = np.sqrt((x - center_w)**2 + (y - center_h)**2)
        
        # Sample colors at different distances from center
        n_rings = 5
        ring_colors = []
        max_dist = np.sqrt(center_h**2 + center_w**2)
        
        for i in range(n_rings):
            mask = (distances > (max_dist * i / n_rings)) & (distances <= (max_dist * (i+1) / n_rings))
            if np.sum(mask) > 0:
                ring_colors.append(np.mean(rgb[mask], axis=0))
        
        if len(ring_colors) >= 3:
            # Check if colors change with distance (radial pattern)
            color_changes = sum(np.linalg.norm(ring_colors[i] - ring_colors[i+1]) 
                             for i in range(len(ring_colors)-1))
            if color_changes > 50:
                return min(1, color_changes / 200)
        
        return 0.0
    
    def _detect_embroidered(self, gray: np.ndarray) -> float:
        """
        Detect embroidered patterns (textured, raised look)
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        from scipy import ndimage
        
        # Look for high frequency texture
        # Emroidery has fine, detailed texture
        h, w = gray.shape
        
        # Small scale detail
        kernel = np.array([[-1, -1, -1],
                         [-1,  8, -1],
                         [-1, -1, -1]])
        
        detail = ndimage.convolve(gray.astype(float), kernel)
        detail_strength = np.mean(np.abs(detail) > 30)
        
        # Also check for bumpy texture
        variance_local = ndimage.uniform_filter(gray**2, size=5) - ndimage.uniform_filter(gray, size=5)**2
        texture_bumpiness = np.mean(variance_local > 100)
        
        if detail_strength > 0.1 or texture_bumpiness > 0.2:
            return min(1, (detail_strength + texture_bumpiness) / 2)
        
        return 0.0
    
    def _detect_printed(self, gray: np.ndarray) -> float:
        """
        Detect general printed patterns
        
        Args:
            gray: Grayscale image array
            
        Returns:
            Confidence score (0-1)
        """
        # Printed is a catch-all for patterns that aren't other specific types
        solid_score = self._detect_solid(gray)
        stripe_score = self._detect_stripes(gray)
        check_score = self._detect_checks(gray)
        
        # If it has some pattern but isn't clearly any specific type
        if solid_score < 0.8 and (stripe_score + check_score) < 0.5:
            return 0.5
        
        return 0.0
    
    def batch_detect_patterns(self, image_paths: List[Path]) -> Dict[str, str]:
        """
        Detect patterns for multiple images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            Dictionary mapping image path to pattern
        """
        from tqdm import tqdm
        
        results = {}
        for img_path in tqdm(image_paths, desc="Detecting patterns"):
            try:
                image = Image.open(img_path).convert('RGB')
                pattern = self.detect_pattern(image)
                results[str(img_path)] = pattern
            except Exception as e:
                print(f"Error processing {img_path.name}: {str(e)}")
                results[str(img_path)] = 'other'
        
        return results
    
    def get_pattern_distribution(self, patterns: List[str]) -> Dict[str, int]:
        """
        Get distribution of patterns in a list
        
        Args:
            patterns: List of pattern names
            
        Returns:
            Dictionary mapping pattern to count
        """
        distribution = {}
        for pattern in patterns:
            distribution[pattern] = distribution.get(pattern, 0) + 1
        return distribution
