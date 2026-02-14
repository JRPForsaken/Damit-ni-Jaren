"""
Feature Extractor Module
Uses deep learning to extract features from clothing images
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
from typing import List, Tuple
from pathlib import Path
from tqdm import tqdm
import config


class FeatureExtractor:
    """Extract deep learning features from images using pre-trained CNN"""
    
    def __init__(self, model_name: str = None, use_gpu: bool = None):
        """
        Initialize the feature extractor
        
        Args:
            model_name: Name of pre-trained model to use
            use_gpu: Whether to use GPU if available
        """
        self.model_name = model_name or config.MODEL_NAME
        self.use_gpu = use_gpu if use_gpu is not None else config.USE_GPU
        
        # Set device
        self.device = torch.device('cuda' if torch.cuda.is_available() and self.use_gpu else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load model
        self.model = self._load_model()
        self.model.eval()
        
        # Image transforms
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Cache for features
        self.feature_cache = {}
    
    def _load_model(self) -> nn.Module:
        """
        Load pre-trained model and modify for feature extraction
        
        Returns:
            Modified PyTorch model
        """
        print(f"Loading {self.model_name} model...")
        
        if self.model_name == 'resnet50':
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
            # Remove final classification layer
            model = nn.Sequential(*list(model.children())[:-1])
        elif self.model_name == 'resnet18':
            model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            model = nn.Sequential(*list(model.children())[:-1])
        elif self.model_name == 'efficientnet_b0':
            model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
            model.classifier = nn.Identity()
        elif self.model_name == 'efficientnet_b7':
            print("Loading EfficientNet-B7 (this may take a moment, ~255MB download)...")
            model = models.efficientnet_b7(weights=models.EfficientNet_B7_Weights.IMAGENET1K_V1)
            model.classifier = nn.Identity()
        else:
            # Default to ResNet50
            print(f"Unknown model '{self.model_name}', defaulting to ResNet50")
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
            model = nn.Sequential(*list(model.children())[:-1])
        
        model = model.to(self.device)
        print("Model loaded successfully")
        return model
    
    def extract_features(self, image: torch.Tensor) -> np.ndarray:
        """
        Extract features from a single image
        
        Args:
            image: Preprocessed image tensor
            
        Returns:
            Feature vector as numpy array
        """
        with torch.no_grad():
            image = image.unsqueeze(0).to(self.device)
            features = self.model(image)
            features = features.squeeze().cpu().numpy()
            
            # Flatten if needed
            if len(features.shape) > 1:
                features = features.flatten()
            
            # Normalize features
            features = features / (np.linalg.norm(features) + 1e-8)
            
        return features
    
    def extract_features_batch(self, images: List[torch.Tensor]) -> np.ndarray:
        """
        Extract features from multiple images in batch
        
        Args:
            images: List of preprocessed image tensors
            
        Returns:
            Array of feature vectors
        """
        batch_size = config.BATCH_SIZE
        all_features = []
        
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            batch_tensor = torch.stack(batch).to(self.device)
            
            with torch.no_grad():
                features = self.model(batch_tensor)
                features = features.squeeze().cpu().numpy()
                
                # Handle single image case
                if len(features.shape) == 1:
                    features = features.reshape(1, -1)
                elif len(features.shape) > 2:
                    features = features.reshape(features.shape[0], -1)
                
                # Normalize each feature vector
                norms = np.linalg.norm(features, axis=1, keepdims=True) + 1e-8
                features = features / norms
                
                all_features.append(features)
        
        return np.vstack(all_features)
    
    def process_image_file(self, image_path: Path, from_pil=None) -> np.ndarray:
        """
        Process an image file and extract features
        
        Args:
            image_path: Path to image file
            from_pil: PIL Image object (optional, to avoid reloading)
            
        Returns:
            Feature vector
        """
        # Check cache
        cache_key = str(image_path)
        if config.CACHE_FEATURES and cache_key in self.feature_cache:
            return self.feature_cache[cache_key]
        
        # Load and transform image
        if from_pil is not None:
            image = from_pil
        else:
            from PIL import Image
            image = Image.open(image_path).convert('RGB')
        
        image_tensor = self.transform(image)
        
        # Extract features
        features = self.extract_features(image_tensor)
        
        # Cache features
        if config.CACHE_FEATURES:
            self.feature_cache[cache_key] = features
        
        return features
    
    def process_image_files_batch(self, image_paths: List[Path]) -> Tuple[List[Path], np.ndarray]:
        """
        Process multiple image files and extract features
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            Tuple of (valid_paths, feature_matrix)
        """
        from PIL import Image
        
        valid_paths = []
        image_tensors = []
        
        print("Loading and transforming images...")
        for img_path in tqdm(image_paths):
            try:
                # Check cache first
                cache_key = str(img_path)
                if config.CACHE_FEATURES and cache_key in self.feature_cache:
                    continue
                
                img = Image.open(img_path).convert('RGB')
                img_tensor = self.transform(img)
                image_tensors.append(img_tensor)
                valid_paths.append(img_path)
            except Exception as e:
                print(f"Error processing {img_path.name}: {str(e)}")
        
        if not image_tensors:
            # All images were cached
            cached_paths = [p for p in image_paths if str(p) in self.feature_cache]
            cached_features = [self.feature_cache[str(p)] for p in cached_paths]
            return cached_paths, np.array(cached_features)
        
        print(f"Extracting features from {len(image_tensors)} images...")
        features = self.extract_features_batch(image_tensors)
        
        # Cache new features
        if config.CACHE_FEATURES:
            for path, feat in zip(valid_paths, features):
                self.feature_cache[str(path)] = feat
        
        # Combine with cached features
        all_paths = []
        all_features = []
        
        for img_path in image_paths:
            cache_key = str(img_path)
            if cache_key in self.feature_cache:
                all_paths.append(img_path)
                all_features.append(self.feature_cache[cache_key])
        
        return all_paths, np.array(all_features)
    
    def compute_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Compute cosine similarity between two feature vectors
        
        Args:
            features1: First feature vector
            features2: Second feature vector
            
        Returns:
            Similarity score (0-1)
        """
        similarity = np.dot(features1, features2)
        return float(similarity)
    
    def find_similar_images(self, query_features: np.ndarray, 
                           all_features: np.ndarray, 
                           threshold: float = None) -> List[int]:
        """
        Find images similar to query based on features
        
        Args:
            query_features: Feature vector of query image
            all_features: Feature matrix of all images
            threshold: Similarity threshold
            
        Returns:
            List of indices of similar images
        """
        if threshold is None:
            threshold = config.SIMILARITY_THRESHOLD
        
        # Compute similarities
        similarities = np.dot(all_features, query_features)
        
        # Find similar images
        similar_indices = np.where(similarities >= threshold)[0]
        
        return similar_indices.tolist()
    
    def clear_cache(self):
        """Clear the feature cache"""
        self.feature_cache.clear()
        print("Feature cache cleared")
