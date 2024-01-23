# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['nx/gui/gui_main.py'],
    pathex=['/Users/zeke/Documents/git/project/nx-cli'],
    binaries=[],
    datas=[('nx/assets/*', 'nx/assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='nx-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['nx/assets/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NetXchanger',
)
app = BUNDLE(
    coll,
    name='NetXchanger.app',
    icon='nx/assets/icon.icns',
    bundle_identifier=None,
)
