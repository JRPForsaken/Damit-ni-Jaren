# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for AI Clothing Photo Sorter
Generates standalone Windows executable
"""

import os
import sys
import torch

block_cipher = None

# Get PyTorch library path for bundling
torch_dir = os.path.dirname(torch.__file__)
torch_lib_path = os.path.join(torch_dir, 'lib')

# Build binaries list - include PyTorch libs
binaries_list = []
if os.path.exists(torch_lib_path):
    binaries_list.append((torch_lib_path, 'torch/lib'))

a = Analysis(
    ['gui.py'],
    pathex=[''],
    binaries=binaries_list,
    datas=[
        ('config.py', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        # PyTorch core and C++ bindings
        'torch',
        'torch._C',
        'torch.utils.cpp_extension',
        'torch.nn.modules.dropout',
        'torch.utils.data',
        'torchvision',
        'torchvision.models',
        'torchvision.transforms',
        'torchvision.models.resnet',
        'torchvision.models.efficientnet',
        # Image processing and ML libraries
        'PIL',
        'PIL.Image',
        'cv2',
        'numpy',
        'numpy.core.multiarray',
        'scipy',
        'scipy.spatial',
        'scipy.optimize',
        # Machine learning and clustering
        'sklearn',
        'sklearn.cluster',
        'sklearn.metrics',
        'sklearn.metrics.pairwise',
        'sklearn.preprocessing',
        # Utilities
        'pandas',
        'tqdm',
        # Project modules
        'src',
        'src.image_processor',
        'src.feature_extractor',
        'src.classifier',
        'src.pattern_detector',
        'src.size_detector',
        'src.shape_detector',
        'src.similarity_matcher',
        'src.organizer',
        'src.report_generator',
        'src.path_cache',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=['matplotlib', 'tkinter.test', 'tk'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI_Clothing_Sorter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = no console window, True = show console
)

# Bundle all binaries and data files together with the executable
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AI_Clothing_Sorter'
)
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='AI_Clothing_Sorter'
# )
