# -*- mode: python ; coding: utf-8 -*-
# v3.53 Python3.12 + .venv312 (paddlepaddle-gpu 2.6.2, 项目环境统一3.12)
# (v3.46~v3.51曾切换RapidOCR/Python3.12, 因档案大图CPU推理慢于paddle约3倍回退)
from PyInstaller.utils.hooks import collect_all

datas = [('ofd_writer.py', '.'), ('ocr_models', 'ocr_models'), ('TMToolMan.ico', '.')]
binaries = [('.venv312/Lib/site-packages/paddle/libs/*.dll', 'paddle/libs')]
hiddenimports = ['cv2', 'fitz', 'fontTools', 'ofd_writer', 'paddleocr', 'paddle', 'imghdr', 'requests']
# PyMuPDF 2.0: pymupdf.layout 子包 import 时自动加载布局模型资源
# (pymupdf/layout/resources/onnx/*.yaml+onnx), 缺失则exe启动即FileNotFoundError
# (v3.48发现v3.52回退时丢失, v3.53补回)
tmp_ret = collect_all('pymupdf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('cv2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('paddleocr')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('Cython')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pyclipper')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('skimage')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('scipy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('imgaug')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('shapely')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('lmdb')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('astor')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['TMToolMan.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'easyofd'],
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
    name='TMToolMan',
    icon='TMToolMan.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
