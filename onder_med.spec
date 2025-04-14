# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src\\main.py'],
    pathex=['.', 'src'],  # Her iki dizini de ekle
    binaries=[],
    datas=[
        # Kaynak dosyaları
        ('src\\resources\\images\\*', 'resources\\images'),
        
        # Python modülleri
        ('src\\ui\\*.py', 'ui'),
        ('src\\ui\\tabs\\*.py', 'ui\\tabs'),
        ('src\\ui\\widgets\\*.py', 'ui\\widgets'),
        ('src\\ai\\*.py', 'ai'),
        ('src\\utils\\*.py', 'utils'),
        ('src\\database\\*.py', 'database'),
        ('src\\models\\*.py', 'models'),
        
        # __init__.py dosyaları
        ('src\\__init__.py', '.'),
        ('src\\ui\\__init__.py', 'ui'),
        ('src\\ui\\tabs\\__init__.py', 'ui\\tabs'),
        ('src\\ui\\widgets\\__init__.py', 'ui\\widgets'),
        ('src\\ai\\__init__.py', 'ai'),
        ('src\\utils\\__init__.py', 'utils'),
        ('src\\database\\__init__.py', 'database'),
        ('src\\models\\__init__.py', 'models'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'google.generativeai',
        'dotenv',
        'sqlite3',
        'ui',
        'ui.main_window',
        'ui.tabs',
        'ui.widgets',
        'ai',
        'utils',
        'database',
        'models',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='OnderMed',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src\\resources\\images\\logo_small.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OnderMed'
) 