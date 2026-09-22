# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the Windows desktop app (onedir, no console)."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

spec_dir = Path(SPECPATH)
root = spec_dir.parent

datas = collect_data_files("matplotlib")
datas += collect_data_files("reportlab")
binaries = collect_dynamic_libs("cv2")

hiddenimports = [
    "Main_Folder_Walk",
    "Thorlabs_tif_stks",
    "image_stats_generator",
    "PDF_report_generator",
    "Read_TXT_SNRs",
    "version",
    "scipy.fftpack",
    "cv2",
    "reportlab.pdfgen.canvas",
    "tifffile",
    "imageio",
    "PIL",
    "matplotlib.backends.backend_agg",
    "numpy",
]

a = Analysis(
    [str(root / "app.py")],
    pathex=[str(root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ThorlabsDataOverview",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ThorlabsDataOverview",
)
