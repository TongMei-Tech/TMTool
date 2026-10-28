# -*- mode: python ; coding: utf-8 -*-
# v3.48: 新打包spec——Python 3.12 + .venv312 (RapidOCR/ONNXRuntime, 无paddle)
# 相比旧版(.venv/paddle, 636MB): 无paddle框架依赖, 产物预计~150MB级。
from PyInstaller.utils.hooks import collect_all

datas = [('ofd_writer.py', '.'), ('TMToolMan.ico', '.')]
binaries = []
hiddenimports = ['cv2', 'ofd_writer', 'rapidocr_onnxruntime',
                 'onnxruntime', 'fontTools']
# RapidOCR: 模型(onnx)与config.yaml都在包内, collect_all 确保完整带入
# (已知坑: 只按依赖分析会漏 config.yaml → 运行时找不到配置)
tmp_ret = collect_all('rapidocr_onnxruntime')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# PyMuPDF 2.0: pymupdf.layout 子包 import 时自动加载布局模型资源
# (pymupdf/layout/resources/onnx/*.yaml+onnx), 不带会在目标机报
# FileNotFoundError: ..._MEIxxxx\pymupdf\layout/resources/onnx/layout_rf....yaml
tmp_ret = collect_all('pymupdf')
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
    excludes=['tkinter', 'test', 'easyofd',
              # 未随 venv312 安装的包, 显式排除加速分析
              'paddle', 'paddleocr'],
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
