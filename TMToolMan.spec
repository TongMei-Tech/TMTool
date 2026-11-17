# -*- mode: python ; coding: utf-8 -*-
# v3.53 Python3.12 + .venv312 (paddlepaddle-gpu 2.6.2, 项目环境统一3.12)
# (v3.46~v3.51曾切换RapidOCR/Python3.12, 因档案大图CPU推理慢于paddle约3倍回退)
from PyInstaller.utils.hooks import collect_all

datas = [('ofd_writer.py', '.'), ('ocr_models', 'ocr_models'), ('TMToolMan.ico', '.'),
         # v3.65: 档案馆标准目录内置模板(科技档案案卷级/文件级)
         ('档案馆科技档案案卷级目录.xlsx', '.'),
         ('档案馆科技档案文件级目录.xlsx', '.')]
binaries = [('.venv312/Lib/site-packages/paddle/libs/*.dll', 'paddle/libs')]
# v3.59: 显式打入VC++运行库(vcruntime140/msvcp140及_1/_2变体)——Python3.12的
# 标准库C扩展(_socket.pyd等)与python312.dll依赖这些DLL, PyInstaller onedir默认
# 未收集到_internal顶层, 客户机(未装VC Redistributable)加载_socket.pyd时报
# 'No module named _socket'。取自PyQt5自带的Qt5/bin副本。
binaries += [('.venv312/Lib/site-packages/PyQt5/Qt5/bin/vcruntime140*.dll', '.'),
             ('.venv312/Lib/site-packages/PyQt5/Qt5/bin/msvcp140*.dll', '.')]
# v3.53b方案B: 内置全套CUDA运行库(cudnn8.9+cudart/cublas/cufft/curand/cusolver/cusparse cu12)
# ——exe自带CUDA, GPU机器无需安装CUDA/cuDNN(仅需N卡+驱动)。DLL放exe顶层(_MEI根)
# 供paddle运行时加载(修复用户机器cudnn64_8.dll未配置错误)。
# v3.58: nvidia/*/bin 现同时含 cu11 与 cu12 两套(nvidia-*-cu11 系 pip 包已补装)——
# paddle 2.6.2 为 cu118 构建, 实际加载 cublas64_11/cudart64_110/nvrtc64_112_0/
# cufft64_10/cusparse64_11 等 cu11 命名; cuDNN 8.9 来自 cu12 包(cudnn64_8.dll 两代同名)。
# 通配一把抓, 无需区分, 打包体积相应 +约1GB。
binaries += [('.venv312/Lib/site-packages/nvidia/*/bin/*.dll', '.')]
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

# v3.57b: onedir模式——内置CUDA后依赖达3GB+, onefile单文件(3.6GB)bootloader
# 解压不稳定且启动需数分钟; onedir输出为TMToolMan文件夹(整夹分发), 启动即用。
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TMToolMan',
    icon='TMToolMan.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='TMToolMan',
)
