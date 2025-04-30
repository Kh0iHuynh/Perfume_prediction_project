# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['window_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('perfume_cnn_model.keras', 'perfume_cnn_model.keras'), ('tokenizer.pkl', 'tokenizer.pkl'), ('winning_note_proportions.tsv', 'winning_note_proportions.tsv')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='window_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
