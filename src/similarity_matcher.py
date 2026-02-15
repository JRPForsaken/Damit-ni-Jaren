"""
Similarity Matcher Module
Groups similar clothing items using clustering algorithms
"""

import numpy as np
from typing import List, Dict, Tuple
from pathlib import Path
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics.pairwise import cosine_similarity
import config

# Import pattern and size detection modules
try:
    from src.pattern_detector import PatternDetector
    from src.size_detector import SizeDetector
    from src.shape_detector import ShapeDetector
except ImportError:
    PatternDetector = None
    SizeDetector = None
    ShapeDetector = None


class SimilarityMatcher:
    """Match and group similar clothing items with enhanced attributes"""
    
    def __init__(self, similarity_threshold: float = None, 
                 clustering_method: str = None,
                 use_pattern: bool = True,
                 use_size: bool = True):
        """
        Initialize the similarity matcher
        
        Args:
            similarity_threshold: Threshold for considering items similar
            clustering_method: 'dbscan' or 'kmeans'
            use_pattern: Whether to consider pattern in similarity
            use_size: Whether to consider size in similarity
        """
        self.similarity_threshold = similarity_threshold or config.SIMILARITY_THRESHOLD
        self.clustering_method = clustering_method or config.CLUSTERING_METHOD
        self.min_cluster_size = config.MIN_CLUSTER_SIZE
        self.use_pattern = use_pattern
        self.use_size = use_size
        
        # Weights for combined similarity
        self.visual_weight = 0.5
        self.pattern_weight = 0.25 if use_pattern else 0
        self.size_weight = 0.25 if use_size else 0
        
        # Initialize pattern and size detectors
        self.pattern_detector = PatternDetector() if PatternDetector else None
        self.size_detector = SizeDetector() if SizeDetector else None
        
        # Initialize shape detector for advanced matching
        self.shape_detector = ShapeDetector() if ShapeDetector else None
        
        # Pattern similarity thresholds
        self.pattern_exact_match = 1.0
        self.pattern_similar_match = 0.8
        self.pattern_different_match = 0.3
    
    def extract_patterns_from_images(self, image_paths: List[Path]) -> List[str]:
        """
        Extract patterns from a list of images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of pattern names
        """
        if not self.pattern_detector:
            print("Warning: PatternDetector not available, returning 'unknown' patterns")
            return ['unknown'] * len(image_paths)
        
        from PIL import Image
        patterns = []
        
        for path in image_paths:
            try:
                image = Image.open(path)
                pattern = self.pattern_detector.detect_pattern(image)
                patterns.append(pattern)
            except Exception as e:
                print(f"Error detecting pattern for {path}: {str(e)}")
                patterns.append('unknown')
        
        return patterns
    
    def extract_size_attributes_from_images(self, image_paths: List[Path]) -> List[Dict]:
        """
        Extract size attributes from a list of images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of size attribute dictionaries
        """
        if not self.size_detector:
            print("Warning: SizeDetector not available, returning default attributes")
            return [{'sleeve': 'unknown', 'length': 'unknown', 'fit': 'regular_fit', 'aspect_ratio': 1.0} 
                    for _ in image_paths]
        
        from PIL import Image
        size_attrs = []
        
        for path in image_paths:
            try:
                image = Image.open(path)
                attrs = self.size_detector.detect_attribute(image)
                size_attrs.append(attrs)
            except Exception as e:
                print(f"Error detecting size for {path}: {str(e)}")
                size_attrs.append({'sleeve': 'unknown', 'length': 'unknown', 'fit': 'regular_fit', 'aspect_ratio': 1.0})
        
        return size_attrs
    
    def extract_shape_attributes_from_images(self, image_paths: List[Path]) -> List[Dict]:
        """
        Extract shape attributes from a list of images
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of shape attribute dictionaries
        """
        if not self.shape_detector:
            print("Warning: ShapeDetector not available, returning default attributes")
            return [{'shape_type': 'unknown', 'completeness': 0.5, 'is_folded': False} 
                    for _ in image_paths]
        
        from PIL import Image
        shape_attrs = []
        
        for path in image_paths:
            try:
                image = Image.open(path)
                attrs = self.shape_detector.detect_shape(image)
                shape_attrs.append(attrs)
            except Exception as e:
                print(f"Error detecting shape for {path}: {str(e)}")
                shape_attrs.append({'shape_type': 'unknown', 'completeness': 0.5, 'is_folded': False})
        
        return shape_attrs
    
    def cluster_with_attributes(self, features: np.ndarray, 
                               image_paths: List[Path]) -> Tuple[np.ndarray, List[str], List[Dict], List[Dict]]:
        """
        Complete clustering pipeline with pattern, size, and shape detection
        
        Args:
            features: Feature matrix
            image_paths: List of image paths
            
        Returns:
            Tuple of (cluster_labels, patterns, size_attributes, shape_attributes)
        """
        print("Extracting patterns from images...")
        patterns = self.extract_patterns_from_images(image_paths)
        
        print("Extracting size attributes from images...")
        size_attrs = self.extract_size_attributes_from_images(image_paths)
        
        print("Extracting shape attributes from images...")
        shape_attrs = self.extract_shape_attributes_from_images(image_paths)
        
        print("Computing clusters with multi-attribute weighting...")
        labels = self.cluster_images(features)
        
        return labels, patterns, size_attrs, shape_attrs
    
    def compute_similarity_matrix(self, features: np.ndarray) -> np.ndarray:
        """
        Compute pairwise similarity matrix for all images
        
        Args:
            features: Feature matrix (n_images x feature_dim)
            
        Returns:
            Similarity matrix (n_images x n_images)
        """
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(features)
        return similarity_matrix
    
    def cluster_images_dbscan(self, features: np.ndarray) -> np.ndarray:
        """
        Cluster images using DBSCAN algorithm
        Good for finding arbitrary-shaped clusters
        
        Args:
            features: Feature matrix
            
        Returns:
            Cluster labels for each image
        """
        # Convert similarity threshold to distance threshold
        # Distance = 1 - similarity
        eps = 1 - self.similarity_threshold
        
        # Ensure eps is valid (must be > 0)
        if eps <= 0:
            eps = 0.01  # Use small value for very high similarity threshold
        
        # Apply DBSCAN
        clustering = DBSCAN(
            eps=eps,
            min_samples=self.min_cluster_size,
            metric='cosine'
        )
        
        labels = clustering.fit_predict(features)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        print(f"DBSCAN found {n_clusters} clusters and {n_noise} noise points")
        
        return labels
    
    def cluster_images_kmeans(self, features: np.ndarray, 
                             n_clusters: int = None) -> np.ndarray:
        """
        Cluster images using K-Means algorithm
        
        Args:
            features: Feature matrix
            n_clusters: Number of clusters (auto-estimated if None)
            
        Returns:
            Cluster labels for each image
        """
        if n_clusters is None:
            # Estimate number of clusters based on dataset size
            n_images = features.shape[0]
            n_clusters = max(2, min(n_images // 10, 50))
        
        clustering = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        
        labels = clustering.fit_predict(features)
        
        print(f"K-Means created {n_clusters} clusters")
        
        return labels
    
    def cluster_images(self, features: np.ndarray) -> np.ndarray:
        """
        Cluster images using configured method
        
        Args:
            features: Feature matrix
            
        Returns:
            Cluster labels for each image
        """
        print(f"Clustering images using {self.clustering_method}...")
        
        if self.clustering_method == 'dbscan':
            return self.cluster_images_dbscan(features)
        elif self.clustering_method == 'kmeans':
            return self.cluster_images_kmeans(features)
        else:
            raise ValueError(f"Unknown clustering method: {self.clustering_method}")
    
    def find_similar_groups(self, image_paths: List[Path], 
                           features: np.ndarray,
                           labels: np.ndarray) -> Dict[int, List[Path]]:
        """
        Group images by cluster labels
        
        Args:
            image_paths: List of image paths
            features: Feature matrix
            labels: Cluster labels
            
        Returns:
            Dictionary mapping cluster_id to list of image paths
        """
        groups = {}
        
        for i, (path, label) in enumerate(zip(image_paths, labels)):
            if label == -1:  # Noise point in DBSCAN
                # Create individual group for noise points
                label = f"single_{i}"
            
            if label not in groups:
                groups[label] = []
            
            groups[label].append(path)
        
        return groups
    
    def refine_groups_by_type(self, groups: Dict[int, List[Path]], 
                             classifications: List[Dict[str, str]],
                             image_paths: List[Path]) -> Dict[str, Dict[int, List[Path]]]:
        """
        Refine groups by separating different clothing types
        
        Args:
            groups: Initial groups from clustering
            classifications: List of classification results
            image_paths: List of image paths
            
        Returns:
            Dictionary mapping type -> group_id -> image paths
        """
        # Create path to classification mapping
        path_to_class = {
            str(path): classification 
            for path, classification in zip(image_paths, classifications)
        }
        
        refined_groups = {}
        
        for group_id, paths in groups.items():
            # Group by clothing type within cluster
            type_groups = {}
            
            for path in paths:
                classification = path_to_class.get(str(path), {'type': 'other'})
                clothing_type = classification['type']
                
                if clothing_type not in type_groups:
                    type_groups[clothing_type] = []
                
                type_groups[clothing_type].append(path)
            
            # Add to refined groups
            for clothing_type, type_paths in type_groups.items():
                if clothing_type not in refined_groups:
                    refined_groups[clothing_type] = {}
                
                refined_groups[clothing_type][group_id] = type_paths
        
        return refined_groups
    
    def find_duplicate_angles(self, group_paths: List[Path], 
                             features: np.ndarray,
                             image_paths: List[Path]) -> List[List[Path]]:
        """
        Within a group, find images that are likely the same item from different angles
        
        Args:
            group_paths: Paths of images in the group
            features: All features
            image_paths: All image paths
            
        Returns:
            List of sub-groups (same item, different angles)
        """
        # Get indices of group images
        path_to_idx = {str(path): i for i, path in enumerate(image_paths)}
        group_indices = [path_to_idx[str(path)] for path in group_paths]
        
        # Get features for this group
        group_features = features[group_indices]
        
        # Compute similarity within group
        similarity_matrix = cosine_similarity(group_features)
        
        # Find very similar images (likely same item, different angle)
        high_similarity_threshold = 0.95
        
        # Use connected components to find sub-groups
        visited = set()
        sub_groups = []
        
        for i in range(len(group_paths)):
            if i in visited:
                continue
            
            # Find all images similar to this one
            similar_indices = np.where(similarity_matrix[i] >= high_similarity_threshold)[0]
            
            sub_group = [group_paths[idx] for idx in similar_indices]
            sub_groups.append(sub_group)
            
            visited.update(similar_indices)
        
        return sub_groups
    
    def get_group_statistics(self, groups: Dict[int, List[Path]]) -> Dict[str, any]:
        """
        Get statistics about the groups
        
        Args:
            groups: Dictionary of groups
            
        Returns:
            Statistics dictionary
        """
        total_images = sum(len(paths) for paths in groups.values())
        n_groups = len(groups)
        
        group_sizes = [len(paths) for paths in groups.values()]
        
        stats = {
            'total_images': total_images,
            'n_groups': n_groups,
            'avg_group_size': np.mean(group_sizes) if group_sizes else 0,
            'min_group_size': min(group_sizes) if group_sizes else 0,
            'max_group_size': max(group_sizes) if group_sizes else 0,
            'single_items': sum(1 for size in group_sizes if size == 1)
        }
        
        return stats
    
    def merge_similar_groups(self, groups: Dict[int, List[Path]], 
                            features: np.ndarray,
                            image_paths: List[Path],
                            merge_threshold: float = 0.90) -> Dict[int, List[Path]]:
        """
        Merge groups that are very similar to each other
        
        Args:
            groups: Initial groups
            features: Feature matrix
            image_paths: List of image paths
            merge_threshold: Similarity threshold for merging
            
        Returns:
            Merged groups
        """
        path_to_idx = {str(path): i for i, path in enumerate(image_paths)}
        
        # Compute centroid for each group
        group_ids = list(groups.keys())
        centroids = []
        
        for group_id in group_ids:
            group_indices = [path_to_idx[str(path)] for path in groups[group_id]]
            group_features = features[group_indices]
            centroid = np.mean(group_features, axis=0)
            centroids.append(centroid)
        
        centroids = np.array(centroids)
        
        # Compute similarity between centroids
        centroid_similarity = cosine_similarity(centroids)
        
        # Merge similar groups
        merged = {}
        group_mapping = {}
        next_id = 0
        
        for i, group_id in enumerate(group_ids):
            if group_id in group_mapping:
                continue
            
            # Find groups to merge with this one
            similar_groups = np.where(centroid_similarity[i] >= merge_threshold)[0]
            
            # Merge all similar groups
            merged_paths = []
            for j in similar_groups:
                similar_group_id = group_ids[j]
                merged_paths.extend(groups[similar_group_id])
                group_mapping[similar_group_id] = next_id
            
            merged[next_id] = merged_paths
            next_id += 1
        
        print(f"Merged {len(groups)} groups into {len(merged)} groups")
        
        return merged
    
    def compute_pattern_similarity(self, pattern1: str, pattern2: str) -> float:
        """
        Compute similarity between two patterns
        
        Args:
            pattern1: First pattern name
            pattern2: Second pattern name
            
        Returns:
            Similarity score (0-1)
        """
        if pattern1 == pattern2:
            return self.pattern_exact_match
        
        # Related patterns that go well together
        related_patterns = {
            'solid': ['solid', 'gradient'],
            'striped': ['striped', 'checked', 'plaid'],
            'checked': ['checked', 'plaid', 'striped'],
            'plaid': ['plaid', 'checked', 'geometric'],
            'floral': ['floral', 'garden', 'botanical'],
            'polka_dots': ['polka_dots', 'geometric'],
            'geometric': ['geometric', 'plaid', 'polka_dots'],
            'abstract': ['abstract', 'painted', 'tie_dye'],
            'tie_dye': ['tie_dye', 'abstract', 'painted'],
            'embroidered': ['embroidered', 'printed', 'solid'],
            'printed': ['printed', 'embroidered', 'solid'],
            'gradient': ['gradient', 'solid'],
            'paisley': ['paisley', 'abstract', 'floral']
        }
        
        # Check if patterns are related
        if pattern1 in related_patterns:
            if pattern2 in related_patterns[pattern1]:
                return self.pattern_similar_match
        
        return self.pattern_different_match
    
    def compute_size_similarity(self, size_attrs1: Dict, size_attrs2: Dict) -> float:
        """
        Compute similarity between two size/attribute profiles
        
        Args:
            size_attrs1: Size attributes dict {sleeve, length, fit, aspect_ratio}
            size_attrs2: Size attributes dict {sleeve, length, fit, aspect_ratio}
            
        Returns:
            Similarity score (0-1)
        """
        if not size_attrs1 or not size_attrs2:
            return 0.5
        
        score = 0.0
        weights = {'sleeve': 0.3, 'length': 0.3, 'fit': 0.2, 'aspect_ratio': 0.2}
        total_weight = 0.0
        
        # Compare sleeve length
        sleeve1 = size_attrs1.get('sleeve', 'other')
        sleeve2 = size_attrs2.get('sleeve', 'other')
        sleeve_match = 1.0 if sleeve1 == sleeve2 else (0.7 if sleeve1 != 'other' and sleeve2 != 'other' else 0.3)
        score += sleeve_match * weights['sleeve']
        total_weight += weights['sleeve']
        
        # Compare length
        length1 = size_attrs1.get('length', 'other')
        length2 = size_attrs2.get('length', 'other')
        length_match = 1.0 if length1 == length2 else (0.7 if length1 != 'other' and length2 != 'other' else 0.3)
        score += length_match * weights['length']
        total_weight += weights['length']
        
        # Compare fit
        fit1 = size_attrs1.get('fit', 'regular_fit')
        fit2 = size_attrs2.get('fit', 'regular_fit')
        fit_match = 1.0 if fit1 == fit2 else 0.6
        score += fit_match * weights['fit']
        total_weight += weights['fit']
        
        # Compare aspect ratio (allow small variation)
        aspect1 = size_attrs1.get('aspect_ratio', 1.0)
        aspect2 = size_attrs2.get('aspect_ratio', 1.0)
        aspect_diff = abs(aspect1 - aspect2)
        aspect_match = max(0, 1.0 - (aspect_diff * 0.5))  # Allow 20% variation
        score += aspect_match * weights['aspect_ratio']
        total_weight += weights['aspect_ratio']
        
        return score / total_weight if total_weight > 0 else 0.5
    
    def compute_combined_similarity(self, visual_sim: float, pattern1: str, pattern2: str,
                                   size_attrs1: Dict, size_attrs2: Dict) -> float:
        """
        Compute combined similarity using visual features, pattern, and size
        
        Args:
            visual_sim: Visual/feature similarity score
            pattern1: First pattern
            pattern2: Second pattern
            size_attrs1: First size attributes
            size_attrs2: Second size attributes
            
        Returns:
            Combined similarity score (0-1)
        """
        combined_score = 0.0
        
        # Visual similarity component
        combined_score += visual_sim * self.visual_weight
        
        # Pattern similarity component
        if self.use_pattern and pattern1 and pattern2:
            pattern_sim = self.compute_pattern_similarity(pattern1, pattern2)
            combined_score += pattern_sim * self.pattern_weight
        
        # Size/attribute similarity component
        if self.use_size and size_attrs1 and size_attrs2:
            size_sim = self.compute_size_similarity(size_attrs1, size_attrs2)
            combined_score += size_sim * self.size_weight
        
        return combined_score
    
    def compute_weighted_similarity_matrix(self, features: np.ndarray, 
                                          patterns: List[str] = None,
                                          size_attributes: List[Dict] = None) -> np.ndarray:
        """
        Compute weighted similarity matrix using visual, pattern, and size
        
        Args:
            features: Feature matrix (n_images x feature_dim)
            patterns: List of pattern names for each image
            size_attributes: List of size attribute dicts for each image
            
        Returns:
            Weighted similarity matrix (n_images x n_images)
        """
        n_images = features.shape[0]
        
        # Compute base visual similarity
        visual_similarity = cosine_similarity(features)
        
        # If no pattern or size data, return visual similarity
        if patterns is None and size_attributes is None:
            return visual_similarity
        
        # Initialize weighted similarity matrix
        weighted_similarity = np.zeros((n_images, n_images))
        
        # Compute pairwise weighted similarities
        for i in range(n_images):
            for j in range(n_images):
                visual_sim = visual_similarity[i, j]
                
                pattern1 = patterns[i] if patterns else None
                pattern2 = patterns[j] if patterns else None
                
                size_attrs1 = size_attributes[i] if size_attributes else None
                size_attrs2 = size_attributes[j] if size_attributes else None
                
                weighted_sim = self.compute_combined_similarity(
                    visual_sim, pattern1, pattern2, size_attrs1, size_attrs2
                )
                
                weighted_similarity[i, j] = weighted_sim
        
        return weighted_similarity
    
    def refine_groups_with_attributes(self, groups: Dict[int, List[Path]], 
                                     features: np.ndarray,
                                     image_paths: List[Path],
                                     patterns: List[str] = None,
                                     size_attributes: List[Dict] = None) -> Dict[int, List[Path]]:
        """
        Refine groups by re-clustering using attribute information
        
        Args:
            groups: Initial groups from basic clustering
            features: Feature matrix
            image_paths: All image paths
            patterns: Pattern for each image
            size_attributes: Size attributes for each image
            
        Returns:
            Refined groups with better attribute alignment
        """
        refined_groups = {}
        group_id_counter = 0
        
        path_to_idx = {str(path): i for i, path in enumerate(image_paths)}
        
        # Process each existing group
        for _, group_paths in groups.items():
            if len(group_paths) <= 2:
                # Keep small groups as-is
                refined_groups[group_id_counter] = group_paths
                group_id_counter += 1
                continue
            
            # Get indices for this group
            group_indices = [path_to_idx[str(path)] for path in group_paths]
            
            # Get features for this group
            group_features = features[group_indices]
            
            # Get patterns and sizes for this group if available
            group_patterns = None
            group_sizes = None
            
            if patterns:
                group_patterns = [patterns[i] for i in group_indices]
            
            if size_attributes:
                group_sizes = [size_attributes[i] for i in group_indices]
            
            # Compute weighted similarity for subgroups
            if group_patterns or group_sizes:
                weighted_sim = self.compute_weighted_similarity_matrix(
                    group_features, group_patterns, group_sizes
                )
                
                # Use weighted similarity for sub-clustering
                eps = 1 - self.similarity_threshold
                if eps <= 0:
                    eps = 0.01
                
                clustering = DBSCAN(eps=eps, min_samples=1, metric='precomputed')
                sim_distances = 1 - weighted_sim
                sub_labels = clustering.fit_predict(sim_distances)
                
                # Create sub-groups
                for sub_label in set(sub_labels):
                    if sub_label == -1:
                        continue
                    
                    sub_indices = np.where(sub_labels == sub_label)[0]
                    sub_group = [group_paths[idx] for idx in sub_indices]
                    refined_groups[group_id_counter] = sub_group
                    group_id_counter += 1
            else:
                # No attribute data, keep group as-is
                refined_groups[group_id_counter] = group_paths
                group_id_counter += 1
        
        print(f"Refined {len(groups)} groups into {len(refined_groups)} groups with attributes")
        
        return refined_groups
    
    def group_by_attributes(self, group_paths: List[Path], 
                           patterns: List[str] = None,
                           size_attributes: List[Dict] = None) -> Dict[str, List[Path]]:
        """
        Further subdivide a group by pattern and size attributes
        
        Args:
            group_paths: Paths in the group
            patterns: Patterns for each path
            size_attributes: Size attributes for each path
            
        Returns:
            Dictionary mapping attribute combo to paths
        """
        if not patterns and not size_attributes:
            return {'all': group_paths}
        
        attribute_groups = {}
        
        for i, path in enumerate(group_paths):
            # Create attribute key
            pattern = patterns[i] if patterns else 'unknown'
            size_attr = size_attributes[i] if size_attributes else {}
            
            sleeve = size_attr.get('sleeve', 'unknown') if isinstance(size_attr, dict) else 'unknown'
            length = size_attr.get('length', 'unknown') if isinstance(size_attr, dict) else 'unknown'
            fit = size_attr.get('fit', 'regular') if isinstance(size_attr, dict) else 'regular'
            
            # Create key: pattern_sleeve_length_fit
            key = f"{pattern}_{sleeve}_{length}_{fit}"
            
            if key not in attribute_groups:
                attribute_groups[key] = []
            
            attribute_groups[key].append(path)
        
        return attribute_groups
    
    def validate_group_coherence(self, group_paths: List[Path], 
                                features: np.ndarray,
                                image_paths: List[Path],
                                patterns: List[str] = None,
                                size_attributes: List[Dict] = None) -> Dict[str, any]:
        """
        Validate coherence of a group using all attributes
        
        Args:
            group_paths: Paths in the group
            features: Feature matrix
            image_paths: All image paths
            patterns: Patterns for each image
            size_attributes: Size attributes for each image
            
        Returns:
            Coherence validation results
        """
        if len(group_paths) < 2:
            return {
                'coherence_score': 1.0,
                'is_coherent': True,
                'issues': [],
                'group_size': len(group_paths)
            }
        
        path_to_idx = {str(path): i for i, path in enumerate(image_paths)}
        group_indices = [path_to_idx[str(path)] for path in group_paths]
        
        # Get features for this group
        group_features = features[group_indices]
        
        # Compute pairwise visual similarities
        visual_sims = cosine_similarity(group_features)
        visual_coherence = np.mean([visual_sims[i, j] for i in range(len(group_paths)) 
                                   for j in range(i+1, len(group_paths))])
        
        issues = []
        attribute_coherence = 1.0
        
        # Check pattern consistency
        if patterns:
            group_patterns = [patterns[i] for i in group_indices]
            unique_patterns = set(group_patterns)
            if len(unique_patterns) > 2:
                issues.append(f"Multiple patterns in group: {unique_patterns}")
                attribute_coherence *= 0.8
            elif len(unique_patterns) == 2:
                # Two different patterns - check if compatible
                pattern_list = list(unique_patterns)
                pattern_sim = self.compute_pattern_similarity(pattern_list[0], pattern_list[1])
                if pattern_sim < self.pattern_similar_match:
                    issues.append(f"Incompatible patterns: {pattern_list[0]} vs {pattern_list[1]}")
                    attribute_coherence *= pattern_sim
        
        # Check size consistency
        if size_attributes:
            group_sizes = [size_attributes[i] for i in group_indices]
            
            # Check sleeve consistency
            sleeves = [s.get('sleeve') for s in group_sizes if isinstance(s, dict)]
            if sleeves and len(set(sleeves)) > 2:
                issues.append(f"Multiple sleeve types in group")
                attribute_coherence *= 0.85
            
            # Check length consistency
            lengths = [s.get('length') for s in group_sizes if isinstance(s, dict)]
            if lengths and len(set(lengths)) > 2:
                issues.append(f"Multiple lengths in group")
                attribute_coherence *= 0.85
        
        # Combined coherence score
        coherence_score = (visual_coherence * 0.7 + attribute_coherence * 0.3)
        
        return {
            'coherence_score': coherence_score,
            'visual_coherence': visual_coherence,
            'attribute_coherence': attribute_coherence,
            'is_coherent': coherence_score >= self.similarity_threshold,
            'issues': issues,
            'group_size': len(group_paths),
            'pattern_diversity': len(set(group_patterns)) if patterns else 0
        }
    
    def get_detailed_similarity_scores(self, image_path1: Path, image_path2: Path,
                                      features: np.ndarray,
                                      image_paths: List[Path],
                                      patterns: List[str] = None,
                                      size_attributes: List[Dict] = None) -> Dict[str, float]:
        """
        Get detailed similarity score breakdown between two images
        
        Args:
            image_path1: First image path
            image_path2: Second image path
            features: Feature matrix
            image_paths: All image paths
            patterns: Patterns for each image
            size_attributes: Size attributes for each image
            
        Returns:
            Dictionary with detailed similarity scores
        """
        path_to_idx = {str(path): i for i, path in enumerate(image_paths)}
        
        idx1 = path_to_idx.get(str(image_path1))
        idx2 = path_to_idx.get(str(image_path2))
        
        if idx1 is None or idx2 is None:
            return {'error': 'Image not found in path mapping'}
        
        # Visual similarity
        visual_sim = float(cosine_similarity([features[idx1]], [features[idx2]])[0][0])
        
        # Pattern similarity
        pattern_sim = 0.0
        if patterns and idx1 < len(patterns) and idx2 < len(patterns):
            pattern_sim = self.compute_pattern_similarity(patterns[idx1], patterns[idx2])
        
        # Size similarity
        size_sim = 0.0
        if size_attributes and idx1 < len(size_attributes) and idx2 < len(size_attributes):
            size_sim = self.compute_size_similarity(size_attributes[idx1], size_attributes[idx2])
        
        # Combined similarity
        combined_sim = self.compute_combined_similarity(
            visual_sim,
            patterns[idx1] if patterns else None,
            patterns[idx2] if patterns else None,
            size_attributes[idx1] if size_attributes else None,
            size_attributes[idx2] if size_attributes else None
        )
        
        return {
            'visual_similarity': visual_sim,
            'pattern_similarity': pattern_sim,
            'size_similarity': size_sim,
            'combined_similarity': combined_sim,
            'pattern1': patterns[idx1] if patterns else 'unknown',
            'pattern2': patterns[idx2] if patterns else 'unknown',
            'sleeve1': size_attributes[idx1].get('sleeve') if size_attributes and isinstance(size_attributes[idx1], dict) else 'unknown',
            'sleeve2': size_attributes[idx2].get('sleeve') if size_attributes and isinstance(size_attributes[idx2], dict) else 'unknown'
        }
