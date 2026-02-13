"""
AI Clothing Photo Sorter - GUI Application
Graphical user interface for easy access
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
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


class ClothingSorterGUI:
    """GUI Application for Clothing Photo Sorter"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("AI Clothing Photo Sorter")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar(value=config.OUTPUT_FOLDER_NAME)
        self.similarity_threshold = tk.DoubleVar(value=config.SIMILARITY_THRESHOLD)
        self.clustering_method = tk.StringVar(value=config.CLUSTERING_METHOD)
        self.use_gpu = tk.BooleanVar(value=config.USE_GPU)
        self.copy_files = tk.BooleanVar(value=config.COPY_FILES)
        
        self.is_processing = False
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎨 AI Clothing Photo Sorter",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input folder selection
        input_frame = tk.LabelFrame(main_frame, text="Input Folder", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_entry = tk.Entry(input_frame, textvariable=self.input_folder, width=60)
        input_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        input_btn = tk.Button(
            input_frame,
            text="Browse...",
            command=self.browse_input_folder,
            bg="#3498db",
            fg="white",
            padx=15
        )
        input_btn.pack(side=tk.LEFT)
        
        # Output folder selection
        output_frame = tk.LabelFrame(main_frame, text="Output Folder", padx=10, pady=10)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_entry = tk.Entry(output_frame, textvariable=self.output_folder, width=60)
        output_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        output_btn = tk.Button(
            output_frame,
            text="Browse...",
            command=self.browse_output_folder,
            bg="#3498db",
            fg="white",
            padx=15
        )
        output_btn.pack(side=tk.LEFT)
        
        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="Settings", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Similarity threshold
        threshold_frame = tk.Frame(settings_frame)
        threshold_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(threshold_frame, text="Similarity Threshold:", width=20, anchor='w').pack(side=tk.LEFT)
        threshold_scale = tk.Scale(
            threshold_frame,
            from_=0.5,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            variable=self.similarity_threshold,
            length=300
        )
        threshold_scale.pack(side=tk.LEFT, padx=10)
        tk.Label(threshold_frame, textvariable=self.similarity_threshold).pack(side=tk.LEFT)
        
        # Clustering method
        method_frame = tk.Frame(settings_frame)
        method_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(method_frame, text="Clustering Method:", width=20, anchor='w').pack(side=tk.LEFT)
        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.clustering_method,
            values=['dbscan', 'kmeans'],
            state='readonly',
            width=15
        )
        method_combo.pack(side=tk.LEFT, padx=10)
        
        # Checkboxes
        checkbox_frame = tk.Frame(settings_frame)
        checkbox_frame.pack(fill=tk.X, pady=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Use GPU (if available)",
            variable=self.use_gpu
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(
            checkbox_frame,
            text="Copy files (uncheck to move)",
            variable=self.copy_files
        ).pack(side=tk.LEFT)
        
        # Progress frame
        progress_frame = tk.LabelFrame(main_frame, text="Progress", padx=10, pady=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_btn = tk.Button(
            button_frame,
            text="🚀 Start Sorting",
            command=self.start_sorting,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop_sorting,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10
        )
        clear_btn.pack(side=tk.RIGHT)
        
    def browse_input_folder(self):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            self.log(f"Selected input folder: {folder}")
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
            self.log(f"Selected output folder: {folder}")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
    
    def start_sorting(self):
        """Start the sorting process"""
        
        # Validate input
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select an input folder!")
            return
        
        input_path = Path(self.input_folder.get())
        if not input_path.exists():
            messagebox.showerror("Error", "Input folder does not exist!")
            return
        
        # Disable start button, enable stop button
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        self.is_processing = True
        
        # Run sorting in separate thread
        thread = threading.Thread(target=self.run_sorting, daemon=True)
        thread.start()
    
    def stop_sorting(self):
        """Stop the sorting process"""
        self.is_processing = False
        self.log("\n⚠️ Stopping process...")
    
    def run_sorting(self):
        """Run the sorting process"""
        try:
            start_time = time.time()
            
            self.log("="*60)
            self.log("🎨 AI CLOTHING PHOTO SORTER")
            self.log("="*60 + "\n")
            
            # Step 1: Scan images
            self.log("STEP 1: Scanning images...")
            processor = ImageProcessor(self.input_folder.get())
            image_paths = processor.scan_images()
            
            if not image_paths:
                self.log("❌ No valid images found!")
                self.finish_processing(False)
                return
            
            self.log(f"✅ Found {len(image_paths)} valid images\n")
            
            if not self.is_processing:
                self.finish_processing(False)
                return
            
            # Step 2: Extract features
            self.log("STEP 2: Extracting AI features...")
            extractor = FeatureExtractor(use_gpu=self.use_gpu.get())
            image_paths, features = extractor.process_image_files_batch(image_paths)
            self.log(f"✅ Extracted features from {len(image_paths)} images\n")
            
            if not self.is_processing:
                self.finish_processing(False)
                return
            
            # Step 3: Classify
            self.log("STEP 3: Classifying clothing...")
            classifier = ClothingClassifier()
            classifications = classifier.batch_classify(image_paths, features)
            self.log(f"✅ Classified {len(classifications)} images\n")
            
            if not self.is_processing:
                self.finish_processing(False)
                return
            
            # Step 4: Group similar items
            self.log("STEP 4: Grouping similar items...")
            matcher = SimilarityMatcher(
                similarity_threshold=self.similarity_threshold.get(),
                clustering_method=self.clustering_method.get()
            )
            labels = matcher.cluster_images(features)
            groups = matcher.find_similar_groups(image_paths, features, labels)
            refined_groups = matcher.refine_groups_by_type(groups, classifications, image_paths)
            
            stats = matcher.get_group_statistics(groups)
            self.log(f"✅ Created {stats['n_groups']} groups\n")
            
            if not self.is_processing:
                self.finish_processing(False)
                return
            
            # Step 5: Organize files
            self.log("STEP 5: Organizing files...")
            organizer = FileOrganizer(self.output_folder.get())
            organizer.copy_files = self.copy_files.get()
            
            clothing_types = list(refined_groups.keys())
            organizer.create_output_structure(clothing_types)
            
            organized = organizer.organize_by_groups(refined_groups, classifications, image_paths)
            success_count = organizer.copy_or_move_files(organized)
            organizer.create_index_file(organized, classifications, image_paths)
            
            self.log(f"✅ Organized {success_count} files\n")
            
            if not self.is_processing:
                self.finish_processing(False)
                return
            
            # Step 6: Generate reports
            self.log("STEP 6: Generating reports...")
            processing_time = time.time() - start_time
            
            report_gen = ReportGenerator(self.output_folder.get())
            report_gen.generate_report(
                image_paths,
                classifications,
                refined_groups,
                organized,
                processing_time
            )
            
            self.log(f"✅ Reports generated\n")
            
            # Summary
            self.log("="*60)
            self.log("\n🎉 SORTING COMPLETE! 🎉\n")
            self.log(f"⏱️  Total time: {processing_time:.2f} seconds")
            self.log(f"📊 Processed: {len(image_paths)} images")
            self.log(f"📁 Output: {self.output_folder.get()}")
            self.log("\n" + "="*60 + "\n")
            
            self.finish_processing(True)
            
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.finish_processing(False)
    
    def finish_processing(self, success):
        """Finish processing and update UI"""
        self.progress_bar.stop()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.is_processing = False
        
        if success:
            messagebox.showinfo(
                "Success",
                f"Sorting completed successfully!\n\nOutput folder: {self.output_folder.get()}"
            )


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = ClothingSorterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
