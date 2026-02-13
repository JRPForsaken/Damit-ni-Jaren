"""
AI Clothing Photo Sorter - Main Application
Command-line interface for sorting clothing photos
"""

import argparse
import time
from pathlib import Path
import sys

from src.image_processor import ImageProcessor
from src.feature_extractor import FeatureExtractor
from src.classifier import ClothingClassifier
from src.similarity_matcher import SimilarityMatcher
from src.organizer import FileOrganizer
from src.report_generator import ReportGenerator
import config


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🎨 AI CLOTHING PHOTO SORTER 🎨                    ║
    ║                                                           ║
    ║        Organize your clothing photos with AI             ║
    ║        Version 1.0.0                                      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main application entry point"""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='AI-powered clothing photo sorter',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'input_folder',
        type=str,
        help='Path to folder containing clothing photos'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=config.OUTPUT_FOLDER_NAME,
        help=f'Output folder name (default: {config.OUTPUT_FOLDER_NAME})'
    )
    
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=config.SIMILARITY_THRESHOLD,
        help=f'Similarity threshold for grouping (default: {config.SIMILARITY_THRESHOLD})'
    )
    
    parser.add_argument(
        '-m', '--method',
        type=str,
        choices=['dbscan', 'kmeans'],
        default=config.CLUSTERING_METHOD,
        help=f'Clustering method (default: {config.CLUSTERING_METHOD})'
    )
    
    parser.add_argument(
        '--move',
        action='store_true',
        help='Move files instead of copying'
    )
    
    parser.add_argument(
        '--no-gpu',
        action='store_true',
        help='Disable GPU acceleration'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Validate input folder
    input_folder = Path(args.input_folder)
    if not input_folder.exists():
        print(f"❌ Error: Input folder not found: {input_folder}")
        sys.exit(1)
    
    print(f"📁 Input folder: {input_folder}")
    print(f"📁 Output folder: {args.output}")
    print(f"🎯 Similarity threshold: {args.threshold}")
    print(f"🔧 Clustering method: {args.method}")
    print(f"{'📦 Moving files' if args.move else '📋 Copying files'}")
    print("\n" + "="*60 + "\n")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Step 1: Scan and load images
        print("STEP 1: Scanning images...")
        processor = ImageProcessor(input_folder)
        image_paths = processor.scan_images()
        
        if not image_paths:
            print("❌ No valid images found in the input folder!")
            sys.exit(1)
        
        print(f"✅ Found {len(image_paths)} valid images\n")
        
        # Step 2: Extract features
        print("STEP 2: Extracting AI features...")
        extractor = FeatureExtractor(use_gpu=not args.no_gpu)
        image_paths, features = extractor.process_image_files_batch(image_paths)
        print(f"✅ Extracted features from {len(image_paths)} images\n")
        
        # Step 3: Classify clothing
        print("STEP 3: Classifying clothing types and colors...")
        classifier = ClothingClassifier()
        classifications = classifier.batch_classify(image_paths, features)
        print(f"✅ Classified {len(classifications)} images\n")
        
        # Step 4: Group similar items
        print("STEP 4: Grouping similar items...")
        matcher = SimilarityMatcher(
            similarity_threshold=args.threshold,
            clustering_method=args.method
        )
        labels = matcher.cluster_images(features)
        groups = matcher.find_similar_groups(image_paths, features, labels)
        
        # Refine groups by type
        refined_groups = matcher.refine_groups_by_type(groups, classifications, image_paths)
        
        # Print group statistics
        stats = matcher.get_group_statistics(groups)
        print(f"✅ Created {stats['n_groups']} groups")
        print(f"   Average group size: {stats['avg_group_size']:.1f}")
        print(f"   Single items: {stats['single_items']}\n")
        
        # Step 5: Organize files
        print("STEP 5: Organizing files...")
        organizer = FileOrganizer(args.output)
        
        # Update config for move/copy
        config.COPY_FILES = not args.move
        organizer.copy_files = not args.move
        
        # Create output structure
        clothing_types = list(refined_groups.keys())
        organizer.create_output_structure(clothing_types)
        
        # Organize by groups
        organized = organizer.organize_by_groups(refined_groups, classifications, image_paths)
        
        # Copy/move files
        success_count = organizer.copy_or_move_files(organized)
        
        # Create index file
        organizer.create_index_file(organized, classifications, image_paths)
        
        print(f"✅ Organized {success_count} files\n")
        
        # Step 6: Generate reports
        print("STEP 6: Generating reports...")
        processing_time = time.time() - start_time
        
        report_gen = ReportGenerator(args.output)
        report_gen.generate_report(
            image_paths,
            classifications,
            refined_groups,
            organized,
            processing_time
        )
        
        print(f"✅ Reports generated\n")
        
        # Print summary
        print("="*60)
        print("\n🎉 SORTING COMPLETE! 🎉\n")
        print(f"⏱️  Total time: {processing_time:.2f} seconds")
        print(f"📊 Processed: {len(image_paths)} images")
        print(f"📁 Output: {args.output}")
        print(f"📄 Reports: sorting_report.html, sorting_report.csv")
        print("\n" + "="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
