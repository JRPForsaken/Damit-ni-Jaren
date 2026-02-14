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
                'last_clustering_method': config.CLUSTERING_METHOD
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
                'last_clustering_method': config.CLUSTERING_METHOD
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
    
    def save_all(self, input_folder: str = None, output_folder: str = None,
                 model: str = None, similarity_threshold: float = None,
                 clustering_method: str = None):
        """
        Save multiple settings at once
        
        Args:
            input_folder: Input folder path
            output_folder: Output folder path
            model: Model name
            similarity_threshold: Similarity threshold
            clustering_method: Clustering method
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
        
        self._save_cache()
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache_data = {
            'last_input_folder': '',
            'last_output_folder': '',
            'last_model': config.DEFAULT_MODEL,
            'last_similarity_threshold': config.SIMILARITY_THRESHOLD,
            'last_clustering_method': config.CLUSTERING_METHOD
        }
        self._save_cache()
