# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for AI Clothing Photo Sorter
Generates standalone Windows executable
"""

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[''],
    binaries=[],
    datas=[
        ('config.py', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'torch',
        'torchvision',
        'torchvision.models',
        'PIL',
        'cv2',
        'scipy',
        'sklearn',
        'sklearn.cluster',
        'sklearn.metrics.pairwise',
        'numpy',
        'pandas',
        'tqdm',
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
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_Clothing_Sorter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = no console window, True = show console
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Add your icon here if available
)

# Optional: Create a distribution folder
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='AI_Clothing_Sorter'
# )
