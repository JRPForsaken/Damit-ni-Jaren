"""
Path Cache Module
Saves and loads last used folder paths for convenience
"""

import json
from pathlib import Path
from typing import Dict, Optional
import config


class PathCache:
    """Manage caching of last used paths"""
    
    def __init__(self, cache_file: str = None):
        """
        Initialize path cache
        
        Args:
            cache_file: Path to cache file
        """
        self.cache_file = Path(cache_file or config.CACHE_FILE)
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """
        Load cache from file
        
        Returns:
            Cache dictionary
        """
        if not self.cache_file.exists():
            return {
                'last_input_folder': '',
                'last_output_folder': '',
                'last_model': config.DEFAULT_MODEL,
                'last_similarity_threshold': config.SIMILARITY_THRESHOLD,
                'last_clustering_method': config.CLUSTERING_METHOD,
                'last_use_gpu': config.USE_GPU,
                'last_copy_files': config.COPY_FILES,
                'last_create_subfolders': config.CREATE_SUBFOLDERS,
                'last_group_similar': config.GROUP_SIMILAR_ITEMS,
                'last_min_cluster_size': config.MIN_CLUSTER_SIZE,
                'last_max_workers': config.MAX_WORKERS
            }
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return {
                'last_input_folder': '',
                'last_output_folder': '',
                'last_model': config.DEFAULT_MODEL,
                'last_similarity_threshold': config.SIMILARITY_THRESHOLD,
                'last_clustering_method': config.CLUSTERING_METHOD,
                'last_use_gpu': config.USE_GPU,
                'last_copy_files': config.COPY_FILES,
                'last_create_subfolders': config.CREATE_SUBFOLDERS,
                'last_group_similar': config.GROUP_SIMILAR_ITEMS,
                'last_min_cluster_size': config.MIN_CLUSTER_SIZE,
                'last_max_workers': config.MAX_WORKERS
            }
    
    def _save_cache(self):
        """Save cache to file"""
        if not config.SAVE_LAST_PATHS:
            return
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def get_last_input_folder(self) -> str:
        """Get last used input folder"""
        return self.cache_data.get('last_input_folder', '')
    
    def get_last_output_folder(self) -> str:
        """Get last used output folder"""
        return self.cache_data.get('last_output_folder', '')
    
    def get_last_model(self) -> str:
        """Get last used AI model"""
        return self.cache_data.get('last_model', config.DEFAULT_MODEL)
    
    def get_last_similarity_threshold(self) -> float:
        """Get last used similarity threshold"""
        return self.cache_data.get('last_similarity_threshold', config.SIMILARITY_THRESHOLD)
    
    def get_last_clustering_method(self) -> str:
        """Get last used clustering method"""
        return self.cache_data.get('last_clustering_method', config.CLUSTERING_METHOD)
    
    def get_last_use_gpu(self) -> bool:
        """Get last used GPU setting"""
        return self.cache_data.get('last_use_gpu', config.USE_GPU)
    
    def get_last_copy_files(self) -> bool:
        """Get last used copy/move files setting"""
        return self.cache_data.get('last_copy_files', config.COPY_FILES)
    
    def get_last_create_subfolders(self) -> bool:
        """Get last used create subfolders setting"""
        return self.cache_data.get('last_create_subfolders', config.CREATE_SUBFOLDERS)
    
    def get_last_group_similar(self) -> bool:
        """Get last used group similar items setting"""
        return self.cache_data.get('last_group_similar', config.GROUP_SIMILAR_ITEMS)
    
    def get_last_min_cluster_size(self) -> int:
        """Get last used min cluster size"""
        return self.cache_data.get('last_min_cluster_size', config.MIN_CLUSTER_SIZE)
    
    def get_last_max_workers(self) -> int:
        """Get last used max workers setting"""
        return self.cache_data.get('last_max_workers', config.MAX_WORKERS)
    
    def save_input_folder(self, folder: str):
        """
        Save input folder to cache
        
        Args:
            folder: Input folder path
        """
        self.cache_data['last_input_folder'] = folder
        self._save_cache()
    
    def save_output_folder(self, folder: str):
        """
        Save output folder to cache
        
        Args:
            folder: Output folder path
        """
        self.cache_data['last_output_folder'] = folder
        self._save_cache()
    
    def save_model(self, model: str):
        """
        Save AI model to cache
        
        Args:
            model: Model name
        """
        self.cache_data['last_model'] = model
        self._save_cache()
    
    def save_similarity_threshold(self, threshold: float):
        """
        Save similarity threshold to cache
        
        Args:
            threshold: Similarity threshold value
        """
        self.cache_data['last_similarity_threshold'] = threshold
        self._save_cache()
    
    def save_clustering_method(self, method: str):
        """
        Save clustering method to cache
        
        Args:
            method: Clustering method name
        """
        self.cache_data['last_clustering_method'] = method
        self._save_cache()
    
    def save_use_gpu(self, use_gpu: bool):
        """
        Save GPU usage setting to cache
        
        Args:
            use_gpu: Whether to use GPU
        """
        self.cache_data['last_use_gpu'] = use_gpu
        self._save_cache()
    
    def save_copy_files(self, copy_files: bool):
        """
        Save copy/move files setting to cache
        
        Args:
            copy_files: True to copy, False to move
        """
        self.cache_data['last_copy_files'] = copy_files
        self._save_cache()
    
    def save_create_subfolders(self, create_subfolders: bool):
        """
        Save create subfolders setting to cache
        
        Args:
            create_subfolders: Whether to create subfolders
        """
        self.cache_data['last_create_subfolders'] = create_subfolders
        self._save_cache()
    
    def save_group_similar(self, group_similar: bool):
        """
        Save group similar items setting to cache
        
        Args:
            group_similar: Whether to group similar items
        """
        self.cache_data['last_group_similar'] = group_similar
        self._save_cache()
    
    def save_min_cluster_size(self, min_cluster_size: int):
        """
        Save min cluster size setting to cache
        
        Args:
            min_cluster_size: Minimum cluster size
        """
        self.cache_data['last_min_cluster_size'] = min_cluster_size
        self._save_cache()
    
    def save_max_workers(self, max_workers: int):
        """
        Save max workers setting to cache
        
        Args:
            max_workers: Maximum number of workers
        """
        self.cache_data['last_max_workers'] = max_workers
        self._save_cache()
    
    def save_all(self, input_folder: str = None, output_folder: str = None,
                 model: str = None, similarity_threshold: float = None,
                 clustering_method: str = None, use_gpu: bool = None,
                 copy_files: bool = None, create_subfolders: bool = None,
                 group_similar: bool = None, min_cluster_size: int = None,
                 max_workers: int = None):
        """
        Save multiple settings at once
        
        Args:
            input_folder: Input folder path
            output_folder: Output folder path
            model: Model name
            similarity_threshold: Similarity threshold
            clustering_method: Clustering method
            use_gpu: Whether to use GPU
            copy_files: True to copy, False to move
            create_subfolders: Whether to create subfolders
            group_similar: Whether to group similar items
            min_cluster_size: Minimum cluster size
            max_workers: Maximum number of workers
        """
        if input_folder is not None:
            self.cache_data['last_input_folder'] = input_folder
        if output_folder is not None:
            self.cache_data['last_output_folder'] = output_folder
        if model is not None:
            self.cache_data['last_model'] = model
        if similarity_threshold is not None:
            self.cache_data['last_similarity_threshold'] = similarity_threshold
        if clustering_method is not None:
            self.cache_data['last_clustering_method'] = clustering_method
        if use_gpu is not None:
            self.cache_data['last_use_gpu'] = use_gpu
        if copy_files is not None:
            self.cache_data['last_copy_files'] = copy_files
        if create_subfolders is not None:
            self.cache_data['last_create_subfolders'] = create_subfolders
        if group_similar is not None:
            self.cache_data['last_group_similar'] = group_similar
        if min_cluster_size is not None:
            self.cache_data['last_min_cluster_size'] = min_cluster_size
        if max_workers is not None:
            self.cache_data['last_max_workers'] = max_workers
        
        self._save_cache()
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache_data = {
            'last_input_folder': '',
            'last_output_folder': '',
            'last_model': config.DEFAULT_MODEL,
            'last_similarity_threshold': config.SIMILARITY_THRESHOLD,
            'last_clustering_method': config.CLUSTERING_METHOD,
            'last_use_gpu': config.USE_GPU,
            'last_copy_files': config.COPY_FILES,
            'last_create_subfolders': config.CREATE_SUBFOLDERS,
            'last_group_similar': config.GROUP_SIMILAR_ITEMS,
            'last_min_cluster_size': config.MIN_CLUSTER_SIZE,
            'last_max_workers': config.MAX_WORKERS
        }
        self._save_cache()
