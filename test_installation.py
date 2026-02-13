"""
Test Installation Script
Verifies that all dependencies are installed correctly
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    
    print("Testing AI Clothing Photo Sorter Installation...")
    print("=" * 60)
    
    tests = []
    
    # Test Python version
    print("\n1. Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        tests.append(True)
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        tests.append(False)
    
    # Test PyTorch
    print("\n2. Checking PyTorch...")
    try:
        import torch
        print(f"   ✅ PyTorch {torch.__version__} installed")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            print(f"   ✅ CUDA available (GPU acceleration enabled)")
            print(f"      GPU: {torch.cuda.get_device_name(0)}")
        else:
            print(f"   ⚠️  CUDA not available (will use CPU)")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ PyTorch not installed: {e}")
        tests.append(False)
    
    # Test torchvision
    print("\n3. Checking torchvision...")
    try:
        import torchvision
        print(f"   ✅ torchvision {torchvision.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ torchvision not installed: {e}")
        tests.append(False)
    
    # Test PIL/Pillow
    print("\n4. Checking Pillow (PIL)...")
    try:
        from PIL import Image
        import PIL
        print(f"   ✅ Pillow {PIL.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ Pillow not installed: {e}")
        tests.append(False)
    
    # Test NumPy
    print("\n5. Checking NumPy...")
    try:
        import numpy as np
        print(f"   ✅ NumPy {np.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ NumPy not installed: {e}")
        tests.append(False)
    
    # Test pandas
    print("\n6. Checking pandas...")
    try:
        import pandas as pd
        print(f"   ✅ pandas {pd.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ pandas not installed: {e}")
        tests.append(False)
    
    # Test scikit-learn
    print("\n7. Checking scikit-learn...")
    try:
        import sklearn
        print(f"   ✅ scikit-learn {sklearn.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ scikit-learn not installed: {e}")
        tests.append(False)
    
    # Test OpenCV
    print("\n8. Checking OpenCV...")
    try:
        import cv2
        print(f"   ✅ OpenCV {cv2.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ OpenCV not installed: {e}")
        tests.append(False)
    
    # Test tqdm
    print("\n9. Checking tqdm...")
    try:
        import tqdm
        print(f"   ✅ tqdm {tqdm.__version__} installed")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ tqdm not installed: {e}")
        tests.append(False)
    
    # Test tkinter (for GUI)
    print("\n10. Checking tkinter (for GUI)...")
    try:
        import tkinter
        print(f"   ✅ tkinter installed (GUI available)")
        tests.append(True)
    except ImportError as e:
        print(f"   ⚠️  tkinter not installed (GUI won't work, CLI still available)")
        tests.append(False)
    
    # Test project modules
    print("\n11. Checking project modules...")
    try:
        from src.image_processor import ImageProcessor
        from src.feature_extractor import FeatureExtractor
        from src.classifier import ClothingClassifier
        from src.similarity_matcher import SimilarityMatcher
        from src.organizer import FileOrganizer
        from src.report_generator import ReportGenerator
        print(f"   ✅ All project modules can be imported")
        tests.append(True)
    except ImportError as e:
        print(f"   ❌ Error importing project modules: {e}")
        tests.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(tests)
    total = len(tests)
    
    if passed == total:
        print(f"\n🎉 SUCCESS! All {total} tests passed!")
        print("\nYou're ready to use AI Clothing Photo Sorter!")
        print("\nNext steps:")
        print("  - Run GUI: python gui.py")
        print("  - Run CLI: python main.py <folder_path>")
        print("  - Read: QUICKSTART.md for usage guide")
        return True
    else:
        print(f"\n⚠️  {passed}/{total} tests passed")
        print("\nSome dependencies are missing. Please run:")
        print("  pip install -r requirements.txt")
        return False


if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
