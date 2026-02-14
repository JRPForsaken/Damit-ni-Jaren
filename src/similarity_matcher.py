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


class SimilarityMatcher:
    """Match and group similar clothing items"""
    
    def __init__(self, similarity_threshold: float = None, 
                 clustering_method: str = None):
        """
        Initialize the similarity matcher
        
        Args:
            similarity_threshold: Threshold for considering items similar
            clustering_method: 'dbscan' or 'kmeans'
        """
        self.similarity_threshold = similarity_threshold or config.SIMILARITY_THRESHOLD
        self.clustering_method = clustering_method or config.CLUSTERING_METHOD
        self.min_cluster_size = config.MIN_CLUSTER_SIZE
    
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
