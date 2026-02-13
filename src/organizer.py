"""
File Organizer Module
Organizes and renames clothing images based on classification and grouping
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import config


class FileOrganizer:
    """Organize and rename clothing image files"""
    
    def __init__(self, output_folder: str = None):
        """
        Initialize the file organizer
        
        Args:
            output_folder: Path to output folder
        """
        self.output_folder = Path(output_folder) if output_folder else Path(config.OUTPUT_FOLDER_NAME)
        self.copy_files = config.COPY_FILES
        self.create_subfolders = config.CREATE_SUBFOLDERS
        self.rename_pattern = config.RENAME_PATTERN
        
        # Track organized files
        self.organized_files = []
        self.file_mapping = {}
    
    def create_output_structure(self, clothing_types: List[str]):
        """
        Create output folder structure
        
        Args:
            clothing_types: List of clothing types to create folders for
        """
        # Create main output folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        print(f"Created output folder: {self.output_folder}")
        
        if self.create_subfolders:
            # Create subfolders for each clothing type
            for clothing_type in clothing_types:
                type_folder = self.output_folder / clothing_type
                type_folder.mkdir(exist_ok=True)
                print(f"Created subfolder: {type_folder}")
    
    def generate_filename(self, clothing_type: str, color: str, 
                         item_id: int, original_ext: str) -> str:
        """
        Generate new filename based on pattern
        
        Args:
            clothing_type: Type of clothing
            color: Color of clothing
            item_id: Unique item ID
            original_ext: Original file extension
            
        Returns:
            New filename
        """
        # Use configured pattern
        filename = self.rename_pattern.format(
            type=clothing_type,
            color=color,
            id=item_id
        )
        
        return f"{filename}{original_ext}"
    
    def organize_by_type(self, image_paths: List[Path], 
                        classifications: List[Dict[str, str]]) -> Dict[str, List[Path]]:
        """
        Organize images by clothing type
        
        Args:
            image_paths: List of image paths
            classifications: List of classification results
            
        Returns:
            Dictionary mapping type to list of (old_path, new_path) tuples
        """
        organized = {}
        type_counters = {}
        
        print("Organizing files by type...")
        
        for img_path, classification in zip(image_paths, classifications):
            clothing_type = classification['type']
            color = classification['color']
            
            # Initialize counter for this type
            if clothing_type not in type_counters:
                type_counters[clothing_type] = 1
            
            item_id = type_counters[clothing_type]
            type_counters[clothing_type] += 1
            
            # Generate new filename
            original_ext = img_path.suffix
            new_filename = self.generate_filename(clothing_type, color, item_id, original_ext)
            
            # Determine destination path
            if self.create_subfolders:
                dest_path = self.output_folder / clothing_type / new_filename
            else:
                dest_path = self.output_folder / new_filename
            
            # Store mapping
            if clothing_type not in organized:
                organized[clothing_type] = []
            
            organized[clothing_type].append((img_path, dest_path))
            self.file_mapping[str(img_path)] = str(dest_path)
        
        return organized
    
    def organize_by_groups(self, groups: Dict[str, Dict[int, List[Path]]], 
                          classifications: List[Dict[str, str]],
                          image_paths: List[Path]) -> Dict[str, List[tuple]]:
        """
        Organize images by type and similarity groups
        
        Args:
            groups: Refined groups (type -> group_id -> paths)
            classifications: List of classification results
            image_paths: List of all image paths
            
        Returns:
            Dictionary mapping type to list of (old_path, new_path) tuples
        """
        # Create path to classification mapping
        path_to_class = {
            str(path): classification 
            for path, classification in zip(image_paths, classifications)
        }
        
        organized = {}
        
        print("Organizing files by type and groups...")
        
        for clothing_type, type_groups in groups.items():
            organized[clothing_type] = []
            group_counter = 1
            
            for group_id, group_paths in type_groups.items():
                # Sort paths for consistent ordering
                group_paths = sorted(group_paths, key=lambda p: p.name)
                
                for angle_idx, img_path in enumerate(group_paths, 1):
                    classification = path_to_class.get(str(img_path), {'color': 'other'})
                    color = classification['color']
                    
                    # Generate filename with group info
                    original_ext = img_path.suffix
                    
                    # Include angle/view number if multiple images in group
                    if len(group_paths) > 1:
                        filename = f"{clothing_type}_{color}_g{group_counter:03d}_v{angle_idx}{original_ext}"
                    else:
                        filename = f"{clothing_type}_{color}_{group_counter:04d}{original_ext}"
                    
                    # Determine destination path
                    if self.create_subfolders:
                        dest_path = self.output_folder / clothing_type / filename
                    else:
                        dest_path = self.output_folder / filename
                    
                    organized[clothing_type].append((img_path, dest_path))
                    self.file_mapping[str(img_path)] = str(dest_path)
                
                group_counter += 1
        
        return organized
    
    def copy_or_move_files(self, organized: Dict[str, List[tuple]]) -> int:
        """
        Copy or move files to organized structure
        
        Args:
            organized: Dictionary of organized file mappings
            
        Returns:
            Number of files successfully organized
        """
        from tqdm import tqdm
        
        total_files = sum(len(files) for files in organized.values())
        success_count = 0
        
        action = "Copying" if self.copy_files else "Moving"
        print(f"{action} {total_files} files...")
        
        for clothing_type, file_pairs in organized.items():
            for old_path, new_path in tqdm(file_pairs, desc=f"{action} {clothing_type}"):
                try:
                    # Ensure destination directory exists
                    new_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy or move file
                    if self.copy_files:
                        shutil.copy2(old_path, new_path)
                    else:
                        shutil.move(str(old_path), str(new_path))
                    
                    self.organized_files.append(str(new_path))
                    success_count += 1
                    
                except Exception as e:
                    print(f"Error organizing {old_path.name}: {str(e)}")
        
        print(f"Successfully organized {success_count}/{total_files} files")
        return success_count
    
    def create_index_file(self, organized: Dict[str, List[tuple]],
                         classifications: List[Dict[str, str]],
                         image_paths: List[Path]):
        """
        Create an index file mapping old to new filenames
        
        Args:
            organized: Dictionary of organized file mappings
            classifications: List of classification results
            image_paths: List of image paths
        """
        index_path = self.output_folder / "file_index.txt"
        
        # Create path to classification mapping
        path_to_class = {
            str(path): classification 
            for path, classification in zip(image_paths, classifications)
        }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"File Organization Index\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files: {sum(len(files) for files in organized.values())}\n")
            f.write("=" * 80 + "\n\n")
            
            for clothing_type, file_pairs in sorted(organized.items()):
                f.write(f"\n{clothing_type.upper()}\n")
                f.write("-" * 80 + "\n")
                
                for old_path, new_path in file_pairs:
                    classification = path_to_class.get(str(old_path), {})
                    color = classification.get('color', 'unknown')
                    
                    f.write(f"Original: {old_path.name}\n")
                    f.write(f"New:      {new_path.name}\n")
                    f.write(f"Type:     {clothing_type}\n")
                    f.write(f"Color:    {color}\n")
                    f.write("\n")
        
        print(f"Created index file: {index_path}")
    
    def get_organization_summary(self, organized: Dict[str, List[tuple]]) -> Dict[str, any]:
        """
        Get summary statistics of organization
        
        Args:
            organized: Dictionary of organized file mappings
            
        Returns:
            Summary dictionary
        """
        summary = {
            'total_files': sum(len(files) for files in organized.values()),
            'types': {},
            'output_folder': str(self.output_folder),
            'action': 'copied' if self.copy_files else 'moved'
        }
        
        for clothing_type, file_pairs in organized.items():
            summary['types'][clothing_type] = len(file_pairs)
        
        return summary
    
    def cleanup_empty_folders(self):
        """Remove empty folders in output directory"""
        for folder in self.output_folder.rglob('*'):
            if folder.is_dir() and not any(folder.iterdir()):
                try:
                    folder.rmdir()
                    print(f"Removed empty folder: {folder}")
                except Exception as e:
                    print(f"Could not remove {folder}: {str(e)}")
