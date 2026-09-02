# -*- coding: utf-8 -*-
"""
黑色圆圈检测与裁剪工具 - 检测并裁剪JPG文件左侧或右侧的黑色不规则圆圈
运行环境：Windows 7
依赖：PyQt5, Pillow (PIL), OpenCV (可选)
"""

# ============================ 版本与修改记录 ============================
# 规则：每次修改本文件后，必须递增 VERSION(修订号+1，功能大变时递增次版本号)，
# 并在 CHANGELOG 头部追加一条记录(版本号/日期/修改内容)；窗口标题会显示当前版本号，
# 便于区分不同打包版本。
VERSION = "3.3"

CHANGELOG = [
    # 新版本记录追加在此列表头部(最新在前)
    {
        "version": "3.3",
        "date": "2026-09-01",
        "changes": [
            "性能优化(输出像素逐位不变，8张样张实测16.65s→12.55s)：①消除重复计算——灰度图管线入口只算一次并传引用，各环节写像素后用与_gray_u8逐位一致的整除公式增量同步灰度，消除原先每页5+次重复灰度转换与逐环节PIL↔numpy往返；去黑边15×15模糊合并为双通道单次模糊(均值/平方均值)，竖带环节未改图时其局部标准差直接复用；②纠偏检测共享降采样——convert('L')只转一次贯穿各纠偏环节，1500px降采样图投影法/Hough/分区纠偏共用；③印章保护区域前置缓存——去黑边后算一次印章保护区，孔影/散点两环节共用(后续环节只删不加红/暗像素，缓存区只会更保守偏保护方向)，散点环节暗块掩码同源复用。另：中间档粗搜曾试改0.2°减半，实测0021-1样张角度漂移1.26→1.30不逐位一致，已改回0.1°并在代码内留注",
        ],
    },
    {
        "version": "3.2",
        "date": "2026-08-31",
        "changes": [
            "性能优化：散点清理环节逐候选的块掩码由全图布尔运算(7446组件页单张约3.1s)改为组件外接框/填充窗局部比较，块均值与填充语义逐位不变。实测 0152 页散点环节 10.3s→0.7s、整页 15.0s→4.4s；6张样张平均 5.9s→3.3s，输出像素零差异",
        ],
    },
    {
        "version": "3.1",
        "date": "2026-08-31",
        "changes": [
            "修复去孔影环节误擦章旁手写数字(实测0152右上角章旁手写150及带横线145被当孔影填掉, 而0219同类幸免)：手写笔画外围浅灰晕圈(灰度90~底色-15)会被软阴影掩码连成大块, 尺寸/均值/色散/成组校验全过关后被大半径填充圆覆盖。新增双重拦截：① 暗核拦截——连通块外接框外扩8px检查窗内暗像素(灰度<90)总量>=25即手写/污渍而非孔影(真孔已填白, 孔影纯渐变无暗核)；② 印章邻域保护——候选落入红章/黑章/残章保护区域(含邻域外延)整体跳过；带底色扫描图仅处理装订孔的保护(3.0)经实测有效保留",
        ],
    },
    {
        "version": "3.0",
        "date": "2026-08-31",
        "changes": [
            "新增空白区订书机孔散点清理: 主体文字区外的孤立实心小暗点(订书机冲孔/金属丝压痕, 实心近圆或细长低实心形态)用周边底色填充; 订书钉成排行带(同带5块以上+远离内容区)放宽尺寸限制清理钉帽残迹",
            "印章保护: 红色印章(红通道优势)/黑色规则印章(d>=60近圆)/残缺印章碎块(20-60低实心, 仅内容区附近)及其60px邻域全部跳过, 手写数字笔画群(100px邻域8块以上)同样保护, 实测0152/0219章旁手写150/145/190完整保留",
            "带底色扫描图保护: 整页底色非白(中位灰<235)的图只做装订孔检测填充, 跳过去黑边/色蕴/散点等清理环节(实测0006底色213图被误清117k像素, 现仅装订孔处理)",
        ],
    },
    {
        "version": "2.10",
        "date": "2026-08-28",
        "changes": [
            "撤销2.7的输出命名改动：恢复按输入目录相对路径输出——输出目录下按输入的子目录结构生成对应子目录再写文件，不再生成全路径编码的平铺文件名(用户此前反馈的输出问题实为界面输出框显示内容，非实际文件输出)；预览匹配与完成刷新同步恢复相对路径匹配；大小写冲突改名、终结输出核对、失败兜底拷贝均保留并改为基于相对路径",
        ],
    },
    {
        "version": "2.9",
        "date": "2026-08-28",
        "changes": [
            "处理失败文件兜底拷贝源文件: 终结输出核对发现输出缺失(图损坏/解码异常/写盘失败等)时, 自动将对应源文件拷贝到输出路径补齐, 保证输出目录永远不缺文件; 拷贝也失败(源被外部删除等)才计为真缺失并显式报错; 兜底成功计为成功并在日志标注原因",
        ],
    },
    {
        "version": "2.8",
        "date": "2026-08-27",
        "changes": [
            "修复三张实页小角度倾斜漏纠偏(D10文字左斜/D15题头左斜/D22表格右斜)：真实小角度倾斜(约1°)的投影法置信比常落在1.11-1.19弱区间被误判平整；现弱区间(1.1≤ratio<1.2)引入Hough双重印证——文字密集图全量线conf≥150、表格图线少conf≥40但两法同向(分歧<0.8°)即采信纠偏；印证不足仍判平整，红头保护与表格框线基准语义不变",
        ],
    },
    {
        "version": "2.7",
        "date": "2026-08-26",
        "changes": [
            "输出文件名改为包含源文件全路径：输出平铺在输出目录单层(不再保留输入目录结构)，文件名由源文件全路径编码而成(分隔符/盘符冒号替换为下划线，如 F__数据_档案_001.jpg)，每个输出可直接看出来源，同时天然避免不同子目录同名文件互覆盖；预览匹配同步适配并兼容旧版本结果回退",
        ],
    },
    {
        "version": "2.6",
        "date": "2026-08-26",
        "changes": [
            "新增批处理终结输出核对：批处理结束逐文件校验输出存在且非空，缺失/空文件显式报错并在完成提示中列出文件名，杜绝处理后文件丢失但无任何报错的静默缺失(用户现场排查075/091/134缺失触发)",
            "新增保存后落盘校验：输出写入后立即校验文件存在且大小>0，写盘失败(磁盘满/权限/杀软拦截)即时报失败不再静默",
            "新增输入相对路径大小写冲突检测：两个仅大小写不同的同名文件在Windows上会静默互覆盖，现自动为后者改名(加_重复N后缀)并写日志告警",
        ],
    },
    {
        "version": "2.5",
        "date": "2026-08-26",
        "changes": [
            "修复照片页被误纠偏：横线基准大角度(≥1°)须过Hough文字线印证，照片斜向边缘伪造的基准(实测照片页ruled=-3.6°/-3.4°但Hough近水平线=0°)作废退回常规判定，不纠偏",
            "修复分区纠偏小角度伪峰旋歪含印章页面：底部区有≥15根文字线时，大量近水平线否决投影法小角度倾斜判定(实测0054页27根水平线、投影伪峰-0.78°把含红章的下半页旋歪)，印章等原图内容不再被改动",
            "修复竖向暗带清理误填彩色印章：暗带必为无彩灰色渐变，填充前新增色散>30彩墨保护，蓝色阴影上的红章不再被当暗带填白(实测0054页右下红章约5800像素被改)",
        ],
    },
    {
        "version": "2.4",
        "date": "2026-08-26",
        "changes": [
            "新增垂直框线基准裁决(_vertical_frame_angle)：页面有左右两条清晰竖框线(三/四面包围手写的方框)且接近竖直时，投影法大角度(≥2°)判为框内手写写歪的伪峰，不纠偏(修复0040页三面边框被伪峰-2.58°旋歪的问题)",
        ],
    },
    {
        "version": "2.3",
        "date": "2026-08-26",
        "changes": [
            "性能优化：灰度转换统一改用整除快法(_gray_u8)，单次耗时降至原mean法的1/3且逐位结果完全一致，管线7处调用每页合计省约0.55s(约提速20%)，检测/填充语义不变",
        ],
    },
    {
        "version": "2.2",
        "date": "2026-08-26",
        "changes": [
            "修复分区纠偏路径一(S形手绘/图形页)大角度伪峰误旋：底部区|角度|>=2°时必须有Hough文字线印证，无文字内容印证则不纠偏(实测0017页框内S形手写被投影法伪峰+5.84°旋歪下半页)",
        ],
    },
    {
        "version": "2.1",
        "date": "2026-08-26",
        "changes": [
            "修复红/彩色封面装订孔漏检：_is_solid_dark_disk 新增判据3(中心<20+对比度>=55+盘芯填充率>=0.8)，红底外环对比度仅≈80的真孔不再被白底标定的>=100门槛误拒",
            "横线基准检测新增暗底/彩底页早退(灰度75分位<150返回None)，修复红封面散布伪角+3.4°被误纠偏的问题",
            "修复零度档行和切片错位：零度档直方图不带maxoff偏移，此前行和整体错位导致水平表格页零度闸门失守被误判-0.2°",
            "剪切投影法重写为前景像素散布直方图(bincount)，单页提速约4倍；横线基准每页只计算一次供纠偏各环节复用，消除重复扫描",
            "表格页纠偏统一按印刷框线基准整体进行，禁止表格内部分区纠偏(修复表格第2-4行被单独旋转的问题)",
            "窗口标题显示当前版本号，便于区分打包版本",
        ],
    },
]
# ========================================================================

import sys
import os
import re
import math
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QFileDialog, QTextEdit, QSpinBox, QComboBox,
                             QFormLayout, QGroupBox, QMessageBox, QCheckBox,
                             QProgressBar, QGraphicsView, QGraphicsScene,
                             QScrollArea, QDoubleSpinBox, QSplitter, QSizePolicy,
                             QFrame, QTabWidget, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal, QRectF, QSize
from PyQt5.QtGui import QFont, QImage, QPixmap, QPainter, QPen, QColor, QWheelEvent

# OpenCV 可用性(模块级探测一次)：打包环境缺 cv2 时纠偏/闭运算/去黑边自动切换
# 纯 Python 回退实现，启动日志记录状态便于排查环境问题。
try:
    import cv2 as _cv2_probe
    HAS_CV2 = True
except Exception:
    HAS_CV2 = False


def _gray_u8(arr):
    """快速灰度转换(返回 uint8 二维数组)。
    整除法比 arr.mean(axis=2).astype(uint8) 快约 3 倍(实测 2468x3512 页
    0.041s vs 0.124s)，且逐位完全一致：mean 的 astype(uint8) 是截断取整，
    与正数整除的向下取整结果相同(管线中每页 7+ 处灰度转换，是主要重复开销)。
    """
    if arr.ndim == 2:
        return arr.copy()
    return ((arr[:, :, 0].astype(np.uint16) + arr[:, :, 1] + arr[:, :, 2])
            // 3).astype(np.uint8)


def _projection_skew_cv2(small, max_angle):
    """
    投影方差法估计偏斜角(度)——cv2 实现(主路径)。
    输入为已降采样的灰度小图。预处理：Otsu 二值化 → 去过大连通域(黑斑/边框) →
    水平闭运算增强行信号。
    """
    import cv2
    sh, sw = small.shape[:2]
    _, otsu = cv2.threshold(small, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    mask = (otsu > 0).astype(np.uint8)

    # 去掉过大的连通域(黑斑/装订孔块/边框等干扰)，保留文字笔画
    n_cc, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    max_area = int(0.0015 * sw * sh)
    keep = np.ones(mask.shape, dtype=bool)
    for i in range(1, n_cc):
        if stats[i, cv2.CC_STAT_AREA] > max_area:
            keep[labels == i] = False
    mask = ((mask > 0) & keep).astype(np.uint8)

    # 水平闭运算：把同一行文字连成横向条带，增强行投影信号
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (41, 1))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    center = (sw / 2.0, sh / 2.0)

    def var_at(ang):
        M = cv2.getRotationMatrix2D(center, ang, 1.0)
        rot = cv2.warpAffine(mask, M, (sw, sh), flags=cv2.INTER_NEAREST)
        return int(rot.sum(axis=1).var())

    v0 = var_at(0.0)
    # 三级搜索：先 0.4° 大步长定位峰值区(投影方差-角度曲线为宽单峰，0.4° 不会漏峰)，
    # 再在峰值区±0.4°内 0.1° 细化(真峰距粗搜格点不超过0.05°)，最后±0.1°内 0.02° 精搜。
    # (中间档曾试改0.2°减半搜索，但实测0021-1角度漂移1.26→1.30不逐位一致，已改回0.1°保零差异)
    s1_idx = int(np.argmax([var_at(a) for a in np.arange(-max_angle, max_angle + 1e-6, 0.4)]))
    s1 = -max_angle + s1_idx * 0.4
    coarse_idx = int(np.argmax([var_at(a) for a in np.arange(s1 - 0.4, s1 + 0.4 + 1e-6, 0.1)]))
    coarse = (s1 - 0.4) + coarse_idx * 0.1                            # 粗搜 0.1°
    fine_idx = int(np.argmax([var_at(a) for a in np.arange(coarse - 0.1, coarse + 0.1 + 1e-6, 0.02)]))
    fine = (coarse - 0.1) + fine_idx * 0.02                                  # 细搜 0.02°
    ratio = (var_at(fine) / v0) if v0 > 0 else 1.0
    return round(float(fine), 2), round(ratio, 2)


def _projection_skew_pure(pil_img, max_angle=8.0, gray_l=None):
    """
    投影方差法估计偏斜角——无 cv2 回退版(纯 PIL + numpy)。
    与 cv2 版语义一致：PIL rotate 代替 warpAffine，直方图法代替 cv2.threshold(OTSU)，
    移位或运算代替闭运算，行/列投影占比代替连通域分析去除大块干扰。
    精度/速度略降(搜索步长 0.2°/0.05°)，打包环境缺 cv2 时保证纠偏功能不失效。
    gray_l：pil_img 的灰度 PIL 图(调用方共享，省去重复 convert('L'))。
    """
    gray = gray_l if gray_l is not None else pil_img.convert('L')
    W, H = gray.size
    sc = 1500.0 / max(W, H)  # 降采样加速(比 cv2 版更激进，纯 Python 旋转较慢)
    sw, sh = max(1, int(W * sc)), max(1, int(H * sc))
    img_s = gray.resize((sw, sh))
    small = np.array(img_s)

    # Otsu 阈值(直方图法)
    hist, _ = np.histogram(small, bins=256, range=(0, 256))
    total = float(hist.sum())
    w_b, s_b, thr_otsu, best = 0.0, 0.0, 127, -1.0
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        s_b += t * hist[t]
        m_b = s_b / w_b
        m_f = (small.sum() - s_b) / w_f
        var_b = w_b * w_f * (m_b - m_f) ** 2
        if var_b > best:
            best, thr_otsu = var_b, t
    mask_img = img_s.point(lambda v: 255 if v <= thr_otsu else 0)

    # 去除整行/整列被大块(黑斑/边框)占满的干扰，保留文字笔画
    ma = np.array(mask_img) > 0
    ma[(ma.mean(axis=1) > 0.7), :] = False
    ma[:, (ma.mean(axis=0) > 0.7)] = False
    mask_img = Image.fromarray((ma.astype(np.uint8) * 255))

    # 水平闭运算(移位或运算)：把同一行文字连成横向条带，增强行投影信号
    m = (np.array(mask_img) > 0).astype(np.uint8)
    for _ in range(3):
        d = m.copy()
        d[:, 2:] |= m[:, :-2]
        d[:, :-2] |= m[:, 2:]
        e = d.copy()
        e[:, 2:] &= d[:, :-2]
        e[:, :-2] &= d[:, 2:]
        m = e
    mask_img = Image.fromarray(m * 255)

    def var_at(ang):
        rot = np.array(mask_img.rotate(ang, resample=Image.BILINEAR,
                                       fillcolor=0))
        return int(rot.sum(axis=1).var())

    v0 = var_at(0.0)
    coarse_idx = int(np.argmax([var_at(a) for a in np.arange(-max_angle, max_angle + 1e-6, 0.2)]))
    coarse = -max_angle + coarse_idx * 0.2                                   # 粗搜 0.2°
    fine_idx = int(np.argmax([var_at(a) for a in np.arange(coarse - 0.2, coarse + 0.2 + 1e-6, 0.05)]))
    fine = (coarse - 0.2) + fine_idx * 0.05                                  # 细搜 0.05°
    ratio = (var_at(fine) / v0) if v0 > 0 else 1.0
    return round(float(fine), 2), round(ratio, 2)


def _small_gray(gray_img, cap=1500.0):
    """把 PIL 灰度图降采样为长边 cap 的 numpy 数组(纠偏各环节共享的降采样图)。
    与各环节原有公式一致：sc=cap/max(W,H)(小于 cap 的图同样按比例放大，保持既有语义)。"""
    W, H = gray_img.size
    sc = cap / max(W, H)
    sw, sh = max(1, int(W * sc)), max(1, int(H * sc))
    return np.array(gray_img.resize((sw, sh)))


def _projection_skew(pil_img, max_angle=8.0, gray_l=None, small=None):
    """
    投影方差法估计偏斜角(度)。返回 (最佳旋转角, 置信比)。
    旋转角 = 让内容水平所需的旋转角(PIL 语义：正值=逆时针)。精度约 0.02°。
    置信比 = 最佳角处水平投影方差 / 0°处方差；>1 真实偏斜，≈1 无偏斜/信号弱。
    有 cv2 用主路径；无 cv2 回退纯 Python 实现(不再静默放弃纠偏)。
    gray_l/small：调用方共享输入——gray_l 为 pil_img 的灰度 PIL 图(省重复
    convert('L'))；small 为已降采样的 1500px 灰度 numpy 数组(与 _hough_skew
    同源共享，省重复降采样)。
    """
    try:
        import cv2
    except ImportError:
        return _projection_skew_pure(pil_img, max_angle, gray_l=gray_l)

    if small is None:
        small = _small_gray(gray_l if gray_l is not None else pil_img.convert('L'))
    return _projection_skew_cv2(small, max_angle)


def _hough_skew(pil_img, min_count=30, gray_l=None, small=None):
    """
    Hough直线法估计偏斜角(度)。返回 (角度, 近水平线根数=置信度)。
    对投影法不敏感的小角度(约1°)文字/表单图更灵敏。
    角度已与 PIL rotate 对齐(正值=逆时针，直接用于纠偏)。需要 cv2；无 cv2 返回 (0, 0)。
    gray_l/small：调用方共享输入(与 _projection_skew 同源)——small 为已降采样
    1500px 灰度数组，缺省时自行转换/降采样。

    仅用于文字行方向检测(降采样全量近水平线中位数)，不作表格基准：
    表格横线基准由 _ruled_table_angle(剪切投影法)专责——Canny+Hough 长线的 maxLineGap
    会桥接字间/笔划间隙，使文字行边缘与手写笔划被误当“长线”伪造基准(实测送达回证页
    5 根手写长线伪造+1.04°基准，把原本水平的红色标题旋出左倾被用户投诉)。
    """
    try:
        import cv2
    except ImportError:
        return 0.0, 0

    # 降采样全量近水平线中位数(文字行密集图的主路径)
    if small is None:
        small = _small_gray(gray_l if gray_l is not None else pil_img.convert('L'))
    sh, sw = small.shape[:2]
    edges = cv2.Canny(small, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                            minLineLength=max(20, sw // 8), maxLineGap=20)
    angs = []
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            ang = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if ang > 90:
                ang -= 180
            elif ang <= -90:
                ang += 180
            if -8 < ang < 8:  # 近水平线(文字行方向)；真实偏斜<8°，更大角度是斜线/图形
                angs.append(ang)
    if len(angs) >= min_count:
        return round(float(np.median(angs)), 2), len(angs)
    return 0.0, len(angs)


def _vertical_frame_angle(pil_img, gray_l=None):
    """
    页面左右两条竖向框线(手写/印刷方框的左右边)的基准倾角(度，PIL 语义)；
    无清晰竖框时返回 None。
    手写页常见三/四面包住正文的方框：框内手写字可能整体写歪(实测 0040 页框竖直、
    框内手写行投影法测出 -2.58° 伪峰)，投影法/文字线中位数都被带偏；而两条清晰竖线是
    页面真实方向基准——竖线竖直则页面已正，不应纠偏。
    检测：按列找暗游程≥30%页高的长列，相邻5列内归组；框形要求≥2个窄带组且左右带中心距≥40%页宽；
    每带按行暗像素质心线性拟合测倾斜；两带角度一致(差≤1°)才返回中位角。
    排除(返回None)：暗底页(早退)、单侧孤线/边缘阴影带(间距不足)、整片暗区(带太宽)。
    """
    W, H = pil_img.size
    if max(W, H) > 1800:  # 降采样到长边1500提速(竖线几何不受影响)
        sc = 1500.0 / max(W, H)
        # resize 参数是(宽,高)，与 numpy shape(H,W)顺序相反，勿写反。
        # 保持既有“先缩放彩色图再转灰度”顺序(与转灰再缩放数值不同)；全尺寸灰度转换不再做。
        gray = np.array(pil_img.resize((max(1, int(W * sc)), max(1, int(H * sc)))).convert('L'))
        H, W = gray.shape
    else:
        gray = np.array(gray_l) if gray_l is not None else np.array(pil_img.convert('L'))
    if float(np.percentile(gray, 75)) < 150:
        return None  # 暗底/彩底扫描件不适用框线概念(与清理系列函数惯例一致)
    dark = gray < 160  # 竖线笔墨阈值(印刷/手写墨线均远暗于此，纸面噪点远高于此)
    pad = np.zeros((1, W), dtype=bool)
    d = np.diff(np.concatenate((pad, dark, pad), axis=0).astype(np.int8), axis=0)
    cols = []
    for x in range(W):  # 长暗游程列(手写竖线会小幅摆动，单列游程仍≥30%页高)
        en = np.flatnonzero(d[:, x] == -1)
        st = np.flatnonzero(d[:, x] == 1)
        if len(st) and int((en - st).max()) >= 0.30 * H:
            cols.append(x)
    if not cols:
        return None
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 5:
            groups[-1].append(x)
        else:
            groups.append([x])
    groups = [g for g in groups if len(g) <= 30]  # 过宽=整片暗区，不是竖线
    if len(groups) < 2:
        return None
    centers = [int(np.mean(g)) for g in groups]
    if max(centers) - min(centers) < 0.4 * W:
        return None  # 左右两带须远隔(构成方框左右边)；同侧聚团是边缘阴影/双线，不是框
    angs, rows_all = [], np.arange(H)
    for gc in centers:
        x0, x1 = max(0, gc - 15), min(W, gc + 16)
        band = dark[:, x0:x1]
        ink_rows = band.sum(axis=1)
        ys, xs = np.nonzero(band)
        if not len(ys):
            continue
        wsum = np.bincount(ys, weights=xs + x0, minlength=H)
        xc = wsum / np.maximum(ink_rows, 1)  # 每行竖线质心(无墨行置0不参与拟合)
        sel = ink_rows >= 2
        if sel.sum() < 0.30 * H:
            continue  # 覆盖不足30%页高：线太短不够作基准
        ys_, xc_ = rows_all[sel].astype(np.float64), xc[sel]
        a = float(np.polyfit(ys_, xc_, 1)[0])
        angs.append(np.degrees(np.arctan(a)))
    if len(angs) < 2:
        return None
    angs = sorted(angs)
    if angs[-1] - angs[0] > 1.0:
        return None  # 两线不平行：不是同一个框，不作基准(宁不纠偏)
    return float(np.median(angs))


def _ruled_table_angle(pil_img, gray_l=None):
    """
    页面印刷横线(表格框线/表单行线)基准倾角(度，PIL 语义)；无表格基准时返回 None。
    印刷框线是页面真实方向基准：表格内的手写/打印文字行本身可能写得歪斜(实测手写行与
    框线差达1°)，投影法与文字线中位数都会被它们带偏。

    检测用剪切投影法：对候选斜率(-4°~+4°，步长0.2°)逐列垂直剪切二值图，真横线被
    摊平成水平薄带、该行投影和出现强峰；横线压平后带厚仅数行，取带厚≤12行、行和≥65%
    页宽、≥3条作判据(文字行压平后仍高40+行自然排除——这是相对 Canny+Hough 长线检测的
    关键优势，后者会把文字行边缘/手写笔划误当长线伪造基准)。
    择优次序：薄带数最多 > |角度|最小(水平框线在±0.2°档易并列，小角度优先，防水平表格被量化噪声误旋)。
    教训(游程法为何不行)：倾斜横线在扫描行上的暗游程仅≈线宽/斜率(-2°时约100px)，
    永远够不着长游程门槛，逐行游程法只能检出近水平线、测不出倾角(实测审批表页框线-2°
    全部漏检)；剪切投影才能检出倾斜线并直接给出角度。但剪切档量化(0.2°步长)会在真值≈0°
    时偶然在±0.2°档多出薄带造成伪峰(实测审计表格页真值0°被误判-0.2°)：水平框线被剪切
    错档后行和只是略微稀释，淡线恰在真档跌破门槛、在邻档勉强达标，伪峰比真峰还多1条带。
    故小角度候选(|角|≤0.4°)须过“零度档对比闸门”：若零度档薄带数与最优档相差≤1，
    判为量化伪峰返回0°(宁可漏掉肉眼不可见的0.2°微倾，不可把水平表格旋歪——用户投诉的根源)；
    大角度候选不受此限(真倾斜页在零度档薄带数为0，无歧义)。
    gray_l：调用方共享的灰度 PIL 图(仅 W≤1400 分支使用；大页走彩色缩放路径以保数值不变)。
    """
    W, H = pil_img.size
    if W > 1400:  # 降采样2倍提速(0.2°角度分辨率不受影响)
        # resize 参数是(宽,高)，与 numpy shape(H,W)顺序相反，勿写反。
        # 保持既有“先缩放彩色图再转灰度”顺序(与转灰再缩放数值不同)；
        # 原实现在此分支前的全尺寸灰度转换被丢弃，现已省去。
        gray = np.array(pil_img.resize((W // 2, H // 2)).convert('L'))
        H, W = gray.shape
    else:
        gray = np.array(gray_l) if gray_l is not None else np.array(pil_img.convert('L'))
    if W < 200:
        return None
    # 暗底/彩底扫描件(封面、底纹页)早退：前景≈整页，横线检测退化成页边界/底纹噪声，
    # 会伪造大角度基准(实测0003红封面散布伪角+3.4°)。与清理系列函数的 page_bg<150 惯例一致。
    if float(np.percentile(gray, 75)) < 150:
        return None
    mask = (gray < 210).astype(np.int32)
    # 快速剪切投影：只对前景像素(白底页仅占页面约1%)做行直方图散布，不再全图高级索引剪切——
    # 后者每档要分配并求和 HxW 完整数组(实测单次调用即>1秒，41档×每页2次调用导致整批处理被用户投诉卡慢)。
    # 彩色封面/暗底扫描件前景≈整页(实测0003红封面2.1M点散布仍要1.5秒)，均匀降采样到上限并
    # 按同比例缩小行和门槛——行和是大量像素的统计量，降采样后薄带检出性质不变。
    # 最大剪切偏移有界(tan4°*W)，上下各留零填充行，越界像素自然落出页面。
    ys_f, xs_f = np.nonzero(mask)
    n_f = len(ys_f)
    cap = 600000
    if n_f > cap:
        sel = np.random.RandomState(42).choice(n_f, cap, replace=False)
        ys_f, xs_f = ys_f[sel], xs_f[sel]
        frac = cap / float(n_f)
    else:
        frac = 1.0
    thr_sum = int(0.65 * W * frac)
    maxoff = int(round(abs(np.tan(np.radians(4.0))) * W)) + 2
    # 零度档行和：ys_f 值域是 [0,H)，行和从索引0开始，不能加 maxoff 偏移——
    # 剪切档才需要偏移(散布后索引=行+maxoff-舍入斜移)。实测0070曾因错用偏移切片,
    # 零度档薄带数从4条变3条、零度闸门失守误判-0.2°。
    s0 = np.bincount(ys_f, minlength=H)

    def _band_count(s):
        hot = s >= thr_sum
        d = np.diff(np.concatenate(([0], hot.astype(np.int8), [0])))
        st = np.flatnonzero(d == 1)
        en = np.flatnonzero(d == -1)
        return int(((en - st) <= 12).sum())

    def _count_at(m):
        """给定斜率的剪切下，行和≥门槛的薄带(≤12行)数。"""
        if m == 0.0:
            return _band_count(s0)
        # 剪切语义与原全图版 mask[y+m*x, x] 一致：斜率s的线 ys=s*xs+c 被摊平到行 r=ys-m*xs=c，
        # 故散布取负偏移(方向写反会把检出角度符号翻转，实测018从-2°变+2°)。
        shift = maxoff - np.round(m * xs_f).astype(np.int64)
        # 必须用 bincount 累积：hist[idx]+=1 的花式索引会把落在同一行的多个像素丢失(实测018框线-2°漏检)
        hist = np.bincount(ys_f + shift, minlength=H + 2 * maxoff)
        return _band_count(hist[maxoff:maxoff + H])

    best = None  # (角度, 薄带数)
    for k in range(-20, 21):  # -4°..+4° step 0.2°
        n = _count_at(np.tan(np.radians(k * 0.2)))
        if n < 3:
            continue
        ang_k = k * 0.2
        # 择优: 薄带数多 > |角度|小(水平框线在±步长档易并列，小角度优先防水平表格被误旋)
        if best is None or (n, -abs(ang_k)) > (best[1], -abs(best[0])):
            best = (ang_k, n)
    if best is None:
        return None
    ang = float(best[0])
    # 零度档对比闸门：小角度候选可能是量化伪峰(水平框线在邻档的行和稀释极小，
    # 淡线恰在真档跌破门槛时伪峰反而多1条带，实测审计表格页真值0°被误判-0.2°)。
    # 零度档薄带数与最优档相差≤1 → 无法区分真伪 → 判0°(0.2°微倾肉眼不可见，误旋水平表格才是事故)。
    # 大角度候选不查：真倾斜页在零度档薄带数为0(线被摊成厚带)，无歧义。
    if 0.1 <= abs(ang) <= 0.4:
        n0 = _count_at(0.0)
        if best[1] - n0 <= 1:
            return 0.0
    return round(ang, 2)


_RULED_UNSET = object()  # 哨兵：表示横线基准尚未预计算(_deskew_image 内只算一次供两处复用)


def _estimate_skew(pil_img, max_angle=8.0, ruled=_RULED_UNSET, gray_l=None):
    """
    估计图像内容偏斜角(度)。返回 (旋转角, 置信比)，角度已与 PIL rotate 对齐。
    gray_l：调用方(_deskew_image)共享的全页灰度 PIL 图，其 1500px 降采样图在
    本函数内只算一次，供投影法与 Hough 复用(省去各环节重复 convert('L')+降采样)。

    检测优先级：
    0. 印刷横线基准(最高优先，先于投影法计算)：页面有表格框线时，框线角度是唯一可信的
       页面方向基准(_ruled_table_angle 剪切投影法)。表格内手写/打印文字行可能本身歪斜，
       投影法与 Hough 都会被带偏(实测送达回证页文字线+1°但框线水平，按文字线旋转把原本水平
       的红头标题旋出左倾被用户投诉)；投影法判平整但框线有倾角时也以框线为准整体纠偏。
    1. 投影方差法：ratio>=1.2 且 |角|>=0.1 为真倾斜；ratio≈1 判平整不旋转——
       平整页上按文字线中位数旋转会把局部微倾(红头水平、正文微倾)误当全局倾斜，
       把原本正常的红头/红线旋出可见倾斜。
    2. 投影法大角度低置信伪峰值(>=3°且ratio<1.4，宽表格图)改用 Hough 裁决。
    """
    # 全页灰度 + 1500px 降采样图只算一次，投影法与 Hough 共享(避免各环节重复转换)
    _gl = gray_l if gray_l is not None else pil_img.convert('L')
    _small = _small_gray(_gl)
    # 印刷横线基准(表格页)：优先级最高，检出则直接返回(不再跑投影法)
    if ruled is _RULED_UNSET:
        ruled = _ruled_table_angle(pil_img, gray_l=_gl)
    ang_r = ruled
    if ang_r is not None:
        if abs(ang_r) >= 1.0:
            # 大角度基准须过 Hough 印证：照片/图形页的斜向边缘会被剪切投影误检为“横线薄带”
            # 伪造大角度基准(实测照片页 ruled=-3.6°/-3.4° 而 Hough 有大量近水平线=0°——
            # 真倾斜≥1°的表格页其文字行同样倾斜，实测018页 Hough=-2.17 与 ruled=-2.0 一致)，
            # 不一致则基准作废，退回投影法常规判定(照片页投影判平整→不纠偏)。
            ang_h, conf = _hough_skew(pil_img, small=_small)
            if conf >= 30 and abs(ang_h - ang_r) > 0.8:
                ang_r = None
    if ang_r is not None:
        if abs(ang_r) >= 0.1:
            return ang_r, 2.0  # 框线有倾角：整体按框线纠偏(无论投影法判平整与否)
        return 0.0, 1.0  # 框线水平：页面方向已正，文字行歪斜是书写问题，不旋转(保护红头/框线)
    ang, ratio = _projection_skew(pil_img, max_angle, small=_small)
    if ratio >= 1.2 and abs(ang) >= 0.1:
        # 投影法“大角度+低置信比”可能是宽表格图伪峰值，改用 Hough 裁决。
        if abs(ang) >= 3.0 and ratio < 1.4:
            ang_h, conf = _hough_skew(pil_img, small=_small)
            if conf >= 50:
                # Hough 高置信：以其角度为准(表格图 Hough 可靠)
                return (ang_h, 2.0) if abs(ang_h) >= 0.1 else (0.0, 1.0)
            return 0.0, 1.0  # 两法都不可靠，不纠偏
        return ang, ratio
    # 投影法信号弱(1.1<=ratio<1.2)：真实小角度倾斜的投影信号常在此区间
    # (实测D10/D15/D22三页文字/表格倾斜0.9-1.75°，ratio仅1.11-1.19被判平整漏纠)。
    # Hough 全量近水平线高置信(conf>=150)且角度与投影一致(差<0.8°)时采信——
    # 两独立方法同向印证可信；conf不足或分歧大仍判平整(保持红头保护语义)。
    if 1.1 <= ratio < 1.2:
        ang_h, conf = _hough_skew(pil_img, small=_small)
        # conf>=150 直接可信；表格图线少(conf>=40)但与投影同向(差<0.8°)亦可信
        # (实测D22表格页45根线中位1.75、四分位[0.95,2.14]紧凑同向，投影1.34印证)。
        ok_conf = conf >= 150 or (conf >= 40 and abs(ang_h - ang) <= 0.8)
        if ok_conf and abs(ang_h) >= 0.1:
            return ang_h, 2.0
    # 投影法判平整：不旋转。全量文字线中位数在平整页上不可信(页面局部倾斜不一致时，
    # 如公文红头标题水平、正文微倾，不存在全局一致的倾斜角)，横线基准已在最前预检。
    return 0.0, 1.0


def _deskew_split(pil_img, fillcolor=(255, 255, 255), ruled=_RULED_UNSET, gray_l=None):
    """
    分区纠偏：页面整体无全局倾斜(投影法判平整)，但正文区存在明显倾斜时，
    保留顶部(红头标题/红线等本就水平的内容)原样，仅旋转切分线以下的正文区。
    典型场景：公文红头页——红头标题水平、正文右倾约1°，不存在能同时摆平两者
    的单一旋转角；全局不纠偏则正文保持偏斜(用户不接受)，全局纠偏则红头被旋
    出可见倾斜。两级路径：
    路径一(_deskew_split_bottom)：正文在页面下半部、下方区投影信号充足的常规布局；
    路径二(_deskew_split_lines)：内容集中在页面上部、下方大片空白(印章/日期/页码)
    导致下半区投影被空白稀释的稀疏布局——逐文字行测量、至少两行倾角共识后，
    旋转最上/最下倾斜行之间的条带。
    返回 (结果Image, 底部旋转角；未触发时为原图, 0.0)。
    """
    W, H = pil_img.size
    if H < 800 or W < 400:
        return pil_img, 0.0
    # 表格保护：页面有印刷横线(表格/表单)时禁止分区旋转——切分线无法保证不切穿表格，
    # 局部旋转会把表格内部上下错位/角度不一(实测表格第2-4行被单独旋转被用户投诉)，
    # 表格页只能由 _estimate_skew 按框线基准整体纠偏。
    if ruled is _RULED_UNSET:
        ruled = _ruled_table_angle(pil_img, gray_l=gray_l)
    if ruled is not None:
        return pil_img, 0.0
    out, ang = _deskew_split_bottom(pil_img, fillcolor, gray_l=gray_l)
    if ang != 0.0:
        return out, ang
    return _deskew_split_lines(pil_img, fillcolor, gray_l=gray_l)


def _deskew_split_bottom(pil_img, fillcolor=(255, 255, 255), gray_l=None):
    """
    分区纠偏路径一(常规布局)。
    触发条件(缺一不可)：
      1. 底部区(40%~100%高)投影法测得 |角度|>=0.5° 且置信比>=1.15；
      2. Hough 文字线与投影角度一致(差<=0.8°；无 cv2 时跳过交叉印证)；
      3. 页面上部(15%~50%高)存在宽>=8行的整行白底带(页眉结构，保证切分线不切穿内容)。
    切分线取页面上部的整行白底带(页眉与正文间的空隙)，接缝处是白底，旋转位移不可见。
    """
    W, H = pil_img.size
    # 1. 底部区倾斜测量(投影法 + Hough 交叉印证；底部区降采样图两法共享)
    bottom = pil_img.crop((0, int(H * 0.4), W, H))
    bottom_small = (_small_gray(gray_l.crop((0, int(H * 0.4), W, H)))
                    if gray_l is not None else None)
    ang_b, r_b = _projection_skew(bottom, 8.0, small=bottom_small)
    if abs(ang_b) < 0.5 or r_b < 1.15:
        return pil_img, 0.0
    ang_h, conf = _hough_skew(bottom, small=bottom_small)
    if abs(ang_b) >= 2.0:
        # 大角度必须有 Hough 文字线印证：投影法在图形化内容(如 S 形手绘画笔、
        # 大矩形框内的斜向笔画)上会产生强伪峰(实测 0017 页底部区伪峰 +5.84°/1.34，
        # Hough 近水平线为 0——真倾斜>=2°的正文页必有大量近水平文字线，实测 009 页 +2° 时 177 根)，
        # conf 低说明底部区没有文字内容可印证，宁不纠偏。
        if conf < 30 or abs(ang_b - ang_h) > 0.8:
            return pil_img, 0.0
    elif conf >= 15:
        # 小角度分支：底部区有相当数量文字线可印证。
        # ① 高置信近水平线否决：大量文字线近水平(|角|<=0.3°)而投影法称倾斜——
        #    投影方差被红章弧线/页脚线等图形元素带偏的伪峰(实测 0054 页 27 根水平线、
        #    投影 -0.78°/1.24 把含红章的下半页旋歪，印章内容被改变)。真倾斜页文字行同步倾斜，不会近水平。
        # ② 两法不一致(>0.5°)且置信充足：小角度投影的 1.15 门槛区分度不足，宁可不动。
        if (abs(ang_h) <= 0.3 and abs(ang_b) >= 0.5) or (conf >= 20 and abs(ang_b - ang_h) > 0.5):
            return pil_img, 0.0
    # 2. 切分线：页面上部最靠近正文的整行白底带(顶部内容保留最多)
    gray = np.array(gray_l) if gray_l is not None else np.array(pil_img.convert('L'))
    rows_white = (gray >= 210).mean(axis=1) >= 0.985
    y_lo, y_hi = int(H * 0.15), int(H * 0.50)
    best = None
    y = y_lo
    while y < y_hi:
        if rows_white[y]:
            s = y
            while y < H and rows_white[y]:
                y += 1
            if y - s >= 8 and (best is None or s > best[0]):
                best = (s, y)
        else:
            y += 1
    if best is None:
        return pil_img, 0.0
    y_cut = (best[0] + best[1]) // 2
    # 3. 顶部原样保留，底部绕自身中心旋转，拼回原尺寸画布(旋出三角用填充色)
    top = pil_img.crop((0, 0, W, y_cut))
    bot = pil_img.crop((0, y_cut, W, H)).rotate(
        ang_b, resample=Image.BICUBIC, expand=False, fillcolor=fillcolor)
    out = Image.new(pil_img.mode, (W, H), fillcolor)
    out.paste(top, (0, 0))
    out.paste(bot, (0, y_cut))
    return out, round(float(ang_b), 2)


def _deskew_split_lines(pil_img, fillcolor=(255, 255, 255), gray_l=None):
    """
    分区纠偏路径二(稀疏布局逐行共识)。
    场景：内容集中在页面上部(红头+文号+少量正文行)，下方是印章/日期/页码加大片空白。
    此时路径一的底部区(40%~100%)几乎全是空白，投影信号被稀释(实测 ang≈0/ratio≈1)，
    而正文行本身确有可见倾斜(如右倾约1.5°)。对策：按整行白底带切分内容带，对每
    个文字行高度的内容带单独测投影角，至少两行同向且角度接近(共识)才认定倾斜；
    旋转范围从最上倾斜行上方的白底带到最下倾斜行下方的白底带(下方无白底带则延
    伸到页底)，接缝落在白底带上。防误触发闸门：候选行须有足够墨量(排除印章圆弧/
    手写批注等碎片)、单行置信比>=1.05、行间隔角度差<=1.2°、条带级投影 |角|>=0.5°
    且置信比>=1.02、Hough 交叉印证(同路径一)。
    """
    W, H = pil_img.size
    gray = np.array(gray_l) if gray_l is not None else np.array(pil_img.convert('L'))
    rows_white = (gray >= 210).mean(axis=1) >= 0.985
    ink = gray < 210
    min_ink = int(0.0002 * W * H)  # 文字行墨量下限(随分辨率缩放)：印章圆弧碎片/手写批注达不到

    # 1. 内容带与白底带切分(均为极大连续段)
    runs, wbands = [], []
    y = 0
    while y < H:
        if rows_white[y]:
            s = y
            while y < H and rows_white[y]:
                y += 1
            if y - s >= 8:
                wbands.append((s, y))
        else:
            s = y
            while y < H and not rows_white[y]:
                y += 1
            if y - s >= 12:  # 低于12行的细线/噪点不构成文字行
                runs.append((s, y))

    # 2. 逐行测量：单个文字行(高<=200行，排除印章/图片大块)投影角可信度低，
    #    只作“倾斜行”筛选(墨量达标+置信比>=1.05且|角|>=0.8°)，不直接采信其角度。
    tilted = []
    for (s, e) in runs:
        if e - s > 200 or int(ink[s:e].sum()) < min_ink:
            continue
        a, r = _projection_skew(pil_img.crop((0, max(0, s - 4), W, min(H, e + 4))), 5.0,
                                gray_l=(gray_l.crop((0, max(0, s - 4), W, min(H, e + 4)))
                                        if gray_l is not None else None))
        if r >= 1.05 and abs(a) >= 0.8:
            tilted.append((s, e, a))
    if len(tilted) < 2:
        return pil_img, 0.0
    angs = [t[2] for t in tilted]
    if max(angs) - min(angs) > 1.2:
        return pil_img, 0.0  # 各行角度互不认同：可能是版式伪倾斜，不动
    # 所有倾斜行须同为正文主体：最上与最下倾斜行间距不超过半页(防止页眉页脚偶发噪声对拼)
    if tilted[-1][0] - tilted[0][1] > H * 0.5:
        return pil_img, 0.0

    # 3. 旋转条带：上接缝=最上倾斜行上方最近的白底带中点(限0.3页高内，否则放弃)，
    #    下接缝=最下倾斜行下方最近的白底带中点(无则延伸到页底，同路径一)。
    top_s = tilted[0][0]
    bot_e = tilted[-1][1]
    up = [b for b in wbands if b[1] <= top_s + 2 and top_s - b[1] <= H * 0.3]
    if not up:
        return pil_img, 0.0
    dn = [b for b in wbands if b[0] >= bot_e - 2]
    y_cut_top = (up[-1][0] + up[-1][1]) // 2
    y_cut_bot = ((dn[0][0] + dn[0][1]) // 2) if dn else H

    # 4. 条带级角度裁决(多条平行文字行互相增强，比单行可信；降采样图投影与 Hough 共享)
    strip = pil_img.crop((0, y_cut_top, W, y_cut_bot))
    strip_small = (_small_gray(gray_l.crop((0, y_cut_top, W, y_cut_bot)))
                   if gray_l is not None else None)
    ang_s, r_s = _projection_skew(strip, 5.0, small=strip_small)
    if abs(ang_s) < 0.5 or abs(ang_s) > 4.0 or r_s < 1.02:
        return pil_img, 0.0
    ang_h, conf = _hough_skew(strip, small=strip_small)
    if conf >= 30 and abs(ang_s - ang_h) > 0.8:
        return pil_img, 0.0  # 与 Hough 矛盾：不动

    # 5. 旋转条带并拼回(条带上下接缝都在白底带上，位移不可见)
    strip_r = strip.rotate(ang_s, resample=Image.BICUBIC, expand=False, fillcolor=fillcolor)
    out = pil_img.copy()
    out.paste(strip_r, (0, y_cut_top))
    return out, round(float(ang_s), 2)


def _deskew_image(pil_img, fillcolor=(255, 255, 255), min_angle=0.1, min_ratio=1.2):
    """
    对图像做纯旋转纠偏(自动检测)。返回 (结果Image, 应用的角度；未纠偏时为 0.0)。
    仅当 |偏斜角|>=min_angle(0.1°) 且 置信比>=min_ratio(1.2) 时才纠偏。
    真实偏斜经预处理后置信比通常>=1.3，平整页≈1.0；1.2 兼顾灵敏与抗误报。
    纯旋转(无缩放/剪切)→ 内容不变形；expand=False 保持原尺寸，
    旋出的边角用 fillcolor 填充(默认白)。
    全局判平整但正文区明显倾斜时(红头页)，改走分区纠偏(_deskew_split)。
    横线基准(_ruled_table_angle，约1秒)只计算一次，供 _estimate_skew 与
    _deskew_split 复用，避免每页重复两次的昂贵剪切扫描。
    全页灰度只转一次，供横线基准/投影法/Hough/竖框线/分区各环节共享，
    消除各环节重复的全图 convert('L')。
    """
    gray_l = pil_img.convert('L')
    ruled = _ruled_table_angle(pil_img, gray_l=gray_l)
    ang, ratio = _estimate_skew(pil_img, ruled=ruled, gray_l=gray_l)
    if abs(ang) >= min_angle and ratio >= min_ratio:
        if abs(ang) >= 2.0:
            # 垂直框线裁决：页面有左右两条清晰竖框线(三/四面包围手写的方框)时，竖线是页面方向基准。
            # 框内手写行写歪会让投影法产生大角度伪峰(实测0040页框竖直、框内手写-2.58°把整页旋歪)，
            # 竖框接近竖直则页面已正，宁不纠偏。小角度(<2°)不查：真微倾页竖框同样微倾，投影法可信。
            v_ang = _vertical_frame_angle(pil_img, gray_l=gray_l)
            if v_ang is not None and abs(v_ang) <= 0.6:
                return pil_img, 0.0
        out = pil_img.rotate(ang, resample=Image.BICUBIC, expand=False, fillcolor=fillcolor)
        return out, ang
    return _deskew_split(pil_img, fillcolor, ruled=ruled, gray_l=gray_l)


class CircleDetectionWorker(QThread):
    """黑色圆圈检测后台工作线程（多线程处理）"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    result_signal = Signal(list)  # 发送处理结果列表
    finished_signal = Signal(bool, str)
    file_done_signal = Signal(str)  # 单个文件处理完成后发射其输出路径

    def __init__(self, input_dir, output_dir, max_diameter_mm=25, margin_mm=40, deskew=False, remove_border=True, thread_count=4, edge_cover=False, edge_margin_mm=2.0, dpi=300, auto_darken=True, remove_shadow=True, parent=None):
        super().__init__(parent)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.max_diameter_mm = max_diameter_mm
        self.margin_mm = margin_mm
        self.deskew = deskew
        self.remove_border = remove_border
        self.thread_count = thread_count
        self.edge_cover = edge_cover
        self.edge_margin_mm = edge_margin_mm
        self.auto_darken = auto_darken
        self.remove_shadow = remove_shadow
        self.is_stopped = False
        self.dpi_assumption = dpi
        self.max_diameter_pixels = int(self.max_diameter_mm * self.dpi_assumption / 25.4)
        self.margin_pixels = int(self.margin_mm * self.dpi_assumption / 25.4)
        self.edge_margin_pixels = int(self.edge_margin_mm * self.dpi_assumption / 25.4) if self.edge_cover else 0

    def run(self):
        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            import threading

            jpg_files = []
            for root, dirs, files in os.walk(self.input_dir):
                if self.is_stopped:
                    break
                for filename in files:
                    if filename.lower().endswith(('.jpg', '.jpeg')):
                        jpg_files.append(os.path.join(root, filename))

            def _natural_key(path):
                return [int(t) if t.isdigit() else t.lower()
                        for t in re.split(r'(\d+)', path)]
            jpg_files.sort(key=_natural_key)

            total = len(jpg_files)
            if total == 0:
                self.finished_signal.emit(False, "未找到任何JPG/JPEG文件")
                return

            self.log_signal.emit(f"找到 {total} 个JPG文件，{self.thread_count}线程并行处理...")

            results = []
            processed = [0]
            deskew_count = [0]
            darken_count = [0]
            holed_file_count = [0]
            hole_count_total = [0]
            shadow_file_count = [0]
            shadow_count_total = [0]
            lock = threading.Lock()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(self.output_dir, f"处理日志_{timestamp}.txt")
            os.makedirs(self.output_dir, exist_ok=True)
            logf = open(log_path, 'w', encoding='utf-8')
            log_lock = threading.Lock()

            def wlog(s):
                with log_lock:
                    logf.write(s + "\n")
                    logf.flush()

            wlog("黑色圆洞（装订孔）检测与裁剪 - 处理日志")
            wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog("OpenCV: " + ("可用" if HAS_CV2 else "不可用(降级为纯Python模式，速度较慢)"))
            wlog(f"输入目录: {self.input_dir}")
            wlog(f"输出目录: {self.output_dir}")
            wlog(f"圆圈最大直径: {self.max_diameter_mm}mm；纠偏: {'开启' if self.deskew else '关闭'}；去孔影: {'开启' if self.remove_shadow else '关闭'}；自动加深: {'开启' if self.auto_darken else '关闭'}；线程数: {self.thread_count}")
            wlog("=" * 70)

            # 预分配输出路径：输出保持输入目录结构(相对输入目录)，每个输入子目录在
            # 输出目录下生成对应子目录。仍检测大小写不敏感重名(两个相对路径仅大小写
            # 不同，如 A\009.jpg 与 a\009.jpg)，Windows 文件系统不区分大小写，
            # 后者会静默覆盖前者导致输出缺失且无任何报错。冲突时后者改名加 _重复N 后缀。
            out_paths = {}
            _name_seen = {}
            for jpg_path in jpg_files:
                rel_path = os.path.relpath(jpg_path, self.input_dir)
                key = rel_path.lower()
                n = _name_seen.get(key, 0)
                _name_seen[key] = n + 1
                if n > 0:
                    base, ext = os.path.splitext(rel_path)
                    rel_path = f"{base}_重复{n}{ext}"
                    wlog(f"警告: {jpg_path} 与此前文件相对路径仅大小写不同，Windows下会互相覆盖，"
                         f"本文件输出改名为 {rel_path}")
                out_paths[jpg_path] = os.path.join(self.output_dir, rel_path)

            def process_one(jpg_path, idx):
                if self.is_stopped:
                    return
                self.log_signal.emit(f"处理中: {os.path.basename(jpg_path)}")
                wlog(f"[{idx}/{total}] 正在处理: {jpg_path}")
                try:
                    result = self.process_image(jpg_path, output_path=out_paths[jpg_path])
                except Exception as e:
                    result = {'path': jpg_path, 'filename': os.path.basename(jpg_path),
                              'success': False, 'error_msg': str(e),
                              'circles_found': 0, 'shadows_removed': 0,
                              'deskew_angle': 0.0, 'darken_applied': False}
                with lock:
                    results.append(result)
                    holes = result.get('circles_found', 0)
                    hole_count_total[0] += holes
                    if holes > 0:
                        holed_file_count[0] += 1
                    shadows = result.get('shadows_removed', 0)
                    shadow_count_total[0] += shadows
                    if shadows > 0:
                        shadow_file_count[0] += 1
                    da = result.get('deskew_angle', 0.0) or 0.0
                    if da:
                        deskew_count[0] += 1
                    dk = result.get('darken_applied', False)
                    if dk:
                        darken_count[0] += 1
                    processed[0] += 1
                    if result['success']:
                        parts = [f"✓ {os.path.basename(jpg_path)}"]
                        if self.deskew:
                            parts.append(f"纠偏{da}°" if da else "无需纠偏")
                        parts.append(f"装订孔{holes}个" if holes else "无装订孔")
                        if self.remove_shadow and shadows:
                            parts.append(f"孔影残留{shadows}处")
                        if self.auto_darken:
                            parts.append("已加深" if dk else "无需加深")
                        self.log_signal.emit("  ".join(parts))
                    else:
                        self.log_signal.emit(f"✗ {os.path.basename(jpg_path)} - 失败 {result.get('error_msg', '')}")
                    wlog(f"  装订孔: {'检测并填充 %d 个' % holes if holes else '未检测到'}")
                    if self.remove_shadow:
                        wlog(f"  孔影残留: {'清除 %d 处' % shadows if shadows else '无'}")
                    if self.deskew:
                        wlog(f"  纠偏: {'已纠正 %.2f°' % da if da else '无明显偏斜，未纠偏'}")
                    if self.auto_darken:
                        wlog(f"  加深: {'文字偏浅，已加深' if dk else '文字已足够深，未加深'}")
                    wlog(f"  结果: {'成功' if result['success'] else '失败: ' + str(result.get('error_msg', ''))}")
                    wlog(f"  输出: {result.get('output_path', '')}")
                    if result['success'] and result.get('output_path'):
                        self.file_done_signal.emit(result['output_path'])
                    self.progress_signal.emit(processed[0], total)

            with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                futures = {}
                for idx, jpg_path in enumerate(jpg_files, 1):
                    if self.is_stopped:
                        break
                    future = executor.submit(process_one, jpg_path, idx)
                    futures[future] = jpg_path
                for future in as_completed(futures):
                    if self.is_stopped:
                        for f in futures:
                            f.cancel()
                        break
                    future.result()

            wlog("=" * 70)
            wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            success_count = sum(1 for r in results if r['success'])
            wlog(f"总计文件: {processed[0]}（成功 {success_count}，失败 {processed[0] - success_count}）")
            wlog(f"去装订孔: {holed_file_count[0]} 个文件，共 {hole_count_total[0]} 个孔")
            if self.remove_shadow:
                wlog(f"去孔影残留: {shadow_file_count[0]} 个文件，共 {shadow_count_total[0]} 处")
            wlog(f"纠偏: {deskew_count[0]} 个文件")
            wlog(f"加深: {darken_count[0]} 个文件")
            # 终结输出核对：每个已提交的输入都必须有非空输出落盘。任何环节(线程异常、
            # 写盘失败、杀软拦截、外部删除)导致的缺失都在此显式暴露，
            # 杜绝“处理完成但输出缺文件且无任何报错”的静默缺失。
            # 处理失败的文件兜底拷贝源文件到输出路径——保证输出目录永远不缺文件：
            # 处理不了(损坏图/解码异常等)也比丢文件好，用户至少拿到原始副本。
            # (仅在正常结束时核对：用户中途停止时未提交的文件属预期跳过，已有停止提示覆盖)
            missing_outputs = []
            fallback_copies = []
            if not self.is_stopped:
                res_by_path = {r.get('path'): r for r in results}
                for jpg_path in jpg_files:
                    op = out_paths.get(jpg_path)
                    if op is None:
                        continue
                    ok_file = os.path.exists(op) and os.path.getsize(op) > 0
                    r = res_by_path.get(jpg_path)
                    if not ok_file:
                        reason = (str(r.get('error_msg', ''))
                                  if (r and not r.get('success')) else '输出文件缺失或为空(原因未知)')
                        # 兜底拷贝源文件, 保证不丢文件(目录结构输出下子目录可能尚未创建)
                        try:
                            os.makedirs(os.path.dirname(op), exist_ok=True)
                            shutil.copy2(jpg_path, op)
                            fallback_copies.append(jpg_path)
                            wlog(f"⚠ 处理失败已拷贝源文件兜底: {os.path.basename(jpg_path)}"
                                 f"（{reason}）")
                            self.log_signal.emit(
                                f"⚠ {os.path.basename(jpg_path)} - 处理失败, 已拷贝源文件到输出")
                            # 兜底成功后计为成功(输出存在), 但错误原因仍在日志
                            if r:
                                r['success'] = True
                                r['fallback_copy'] = True
                            success_count += 1
                        except Exception as copy_err:
                            missing_outputs.append((jpg_path, f"{reason}; 兜底拷贝也失败: {copy_err}"))
                            wlog(f"✗ 输出缺失且兜底拷贝失败: {os.path.basename(jpg_path)}"
                                 f" -> {op}（{reason}; 拷贝错误: {copy_err}）")
                            self.log_signal.emit(
                                f"✗ {os.path.basename(jpg_path)} - 输出缺失且拷贝源文件失败！{reason}")
                    elif r and not r.get('success'):
                        # 罕见：报失败但文件在(如保存后校验前异常)——以实际落盘为准改记成功，避免误报
                        r['success'] = True
                        success_count += 1
                if missing_outputs:
                    wlog(f"警告: {len(missing_outputs)} 个输出文件仍缺失(兜底拷贝也失败)，请检查上方明细！")
                if fallback_copies:
                    wlog(f"兜底拷贝: {len(fallback_copies)} 个处理失败文件已用源文件副本补齐输出")
            if self.is_stopped:
                wlog("注意：处理被用户中途停止")
            logf.close()
            self.log_signal.emit(f"已生成处理日志: {os.path.basename(log_path)}")

            if not self.is_stopped:
                self.result_signal.emit(results)
                if missing_outputs:
                    names = "、".join(os.path.basename(j) for j, _ in missing_outputs[:10])
                    more = f"等{len(missing_outputs)}个" if len(missing_outputs) > 10 else ""
                    msg = (f"处理完成但有 {len(missing_outputs)} 个输出文件缺失：{names}{more}！"
                           f"请查看日志 {os.path.basename(log_path)} 并重新处理这些文件。")
                    self.finished_signal.emit(False, msg)
                else:
                    msg = (f"处理完成！共 {processed[0]} 个文件，成功 {success_count}；"
                           f"去孔 {holed_file_count[0]} 文件/{hole_count_total[0]} 个；"
                           + (f"去孔影 {shadow_count_total[0]} 处；" if self.remove_shadow else "") +
                           f"纠偏 {deskew_count[0]} 个文件；"
                           f"加深 {darken_count[0]} 个文件。日志: {os.path.basename(log_path)}")
                    self.finished_signal.emit(True, msg)
            else:
                self.finished_signal.emit(False, f"处理已停止。日志: {os.path.basename(log_path)}")

        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {str(e)}")

    def stop(self):
        self.is_stopped = True

    def darken_text(self, arr, gray, gamma=1.3):
        """
        自动加深文字：对较暗的文字像素(灰度<200)做幂律加深，背景(>200)不变。
        gamma>1 使中间调(浅灰文字)变暗，让文字更黑更清晰，接近高对比扫描件的效果。
        仅当文字偏浅时调用(由 process_image 根据文字平均灰度判断)。
        LUT 实现：映射 v→clip(200*(v/200)^gamma) 只依赖像素自身通道值(注意
        v>=200 时原幂律会把亮通道轻微提亮如240→253，LUT 完全保留此行为)，
        与原 float64 幂律逐位一致；免去全图 float64 中间数组(约 200MB)与逐像素幂运算。
        输入/输出为管线传引用的 numpy 数组：gray 在变像素上用同一整除公式重算，
        与全图 _gray_u8 结果逐位一致。返回 (加深后数组, 同步灰度数组)。
        """
        lut = 200.0 * (np.arange(256, dtype=np.float64) / 200.0) ** gamma
        table = np.clip(lut, 0, 255).astype(np.uint8)
        # 掩码 gray<200 用整除灰度与浮点均值判定逐位等价(sum//3<200 ⇔ sum/3<200)
        mask = gray < 200  # 文字/图形区域(非背景)
        if not mask.any():
            return arr, gray
        out = arr.copy()
        out[mask] = table[arr[mask]]
        g_out = gray.copy()
        if arr.ndim == 3:
            px = out[mask]
            g_out[mask] = ((px[:, 0].astype(np.uint16) + px[:, 1] + px[:, 2])
                           // 3).astype(np.uint8)
        else:
            g_out[mask] = out[mask]
        return out, g_out

    def process_image(self, image_path, output_path=None):
        """
        处理单个图像：检测打孔洞并用白色填充。返回处理结果字典。
        output_path 可由批处理预分配(含大小写冲突改名)；缺省按输入目录相对路径推导(保持目录结构)。
        """
        try:
            # 档案扫描图通常较大：解除 PIL 默认大图限制，容错截断图
            Image.MAX_IMAGE_PIXELS = None
            Image.LOAD_TRUNCATED_IMAGES = True
            img = Image.open(image_path)
            img.load()  # 立即解码，及时暴露损坏文件
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            # 记录原图 DPI，处理过程中 fromarray/rotate 会丢失 DPI 元数据，
            # 保存时需写回，确保输出保持原图分辨率(通常 300DPI)。
            orig_dpi = img.info.get('dpi')
            if not orig_dpi:
                orig_dpi = (float(self.dpi_assumption), float(self.dpi_assumption))
            # 可选：纠偏(去倾斜)——纯旋转，内容不变形；之后再做圆洞检测
            deskew_applied = 0.0
            if self.deskew:
                img, deskew_applied = _deskew_image(img)
            orig_w, orig_h = img.size

            # --- 先检测+填充装订孔（在去黑边之前！）---
            # 去黑边用更宽的灰度阈值(page_bg-60)，会把孔和附近的暗块连成大块一并填掉，
            # 导致后续检测不到孔。先在 <50 严格阈值上检测孔，填充后再去黑边。
            # 性能：管线入口一次性 numpy 化并只算一次灰度，之后各环节传引用复用；
            # 各环节写像素后用同一整除公式同步更新对应像素的灰度(与全图重算逐位一致)，
            # 消除原先每页 5+ 次重复灰度转换与逐环节 PIL↔numpy 往返转换。
            arr = np.array(img)
            gray_full = _gray_u8(arr)
            mask_full = gray_full < 50  # 装订孔检测阈值(灰度<50=足够暗)
            circles_info = self.detect_edge_holes(mask_full, orig_w, orig_h, gray_full)
            # 带底色扫描图判定：整页底色非白(中位灰<235)的图(彩色底/米黄底档案纸)，
            # 其"底色与内容对比弱"，去黑边/色蕴/散点/竖带等清理环节的暗块阈值
            # (bg-60等)会把底色上的正常文字/表格误判清除(实测0006底色213被
            # 误清117k像素)。此类图只做装订孔检测与填充，跳过其他清理。
            _arr_med = float(np.median(gray_full))
            is_tinted_page = _arr_med < 235
            del mask_full
            circles_info = self._dedup_circles(circles_info)

            if circles_info:
                img = self.crop_circles(img, circles_info, arr)

            if is_tinted_page:
                # 带底色图：仅装订孔处理，其余清理全部跳过(底色图上暗块阈值不可靠)
                dots_removed = 0
                shadows_removed = 0
                darken_applied = False
                rel_path = os.path.relpath(image_path, self.input_dir)
                output_path = output_path or os.path.join(self.output_dir, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, quality=95, dpi=orig_dpi)
                return {
                    'path': image_path,
                    'filename': os.path.basename(image_path),
                    'success': True,
                    'circles_found': len(circles_info),
                    'deskew_angle': deskew_applied,
                    'darken_applied': darken_applied,
                    'dots_removed': dots_removed,
                    'shadows_removed': shadows_removed,
                    'tinted_page': True,
                    'output_path': output_path,
                }

            # 非底色页继续清理：孔已填充，先刷新管线基准数组(后续环节看填充后的图)
            if circles_info:
                arr = np.array(img)
                gray_full = _gray_u8(arr)

            # --- 已知孔位残影定点清理：孔周浅灰环影(含与扫描灰带相连的情况) ---
            if self.remove_shadow and circles_info:
                arr, gray_full, _ = self.cleanup_known_hole_residue(
                    arr, gray_full, circles_info)

            # --- 去贴边竖向扫描暗带(装订侧盖板阴影)：孔已填充，按列剖面整带清理 ---
            _vb, _lstd15 = 0, None
            if self.remove_border:
                arr, gray_full, _vb, _lstd15 = self.remove_edge_vertical_band(arr, gray_full)

            # --- 再去黑边/阴影（孔已填充为底色，不会被误连）---
            # 竖带环节未改图(_vb==0)时，其 15×15 局部标准差直接复用(同一灰度，结果逐位一致)
            if self.remove_border:
                arr, gray_full, _br = self.remove_black_border(
                    arr, gray_full, local_std15=_lstd15 if _vb == 0 else None)

            # --- 印章保护区域前置缓存：孔影/散点两环节共用，避免重复全图连通域 ---
            seal_zones = None
            shadows_removed = 0
            if self.remove_shadow:
                seal_zones = self._detect_seal_protect_zones(arr, gray_full)
                # --- 去装订孔阴影残留：孔周浅灰环/弧影(冲头压痕/扫描泛光) ---
                arr, gray_full, shadows_removed = self.remove_hole_shadow_residue(
                    arr, gray_full, seal_zones)

            # --- 去边缘浅蓝色蕴(装订孔后): 扫描仪边缘偏色, 替换为本体色 ---
            arr, gray_full = self.remove_color_halo(arr, gray_full)

            # --- 去空白区订书机孔散点: 主体文字区外的孤立实心小暗点 ---
            arr, gray_full, dots_removed = self.remove_isolated_specks(
                arr, gray_full, seal_zones)

            # --- 边缘底色覆盖：将四周边缘区域用底色覆盖 ---
            if self.edge_cover and self.edge_margin_pixels > 0:
                arr, gray_full = self.cover_edge_with_bg(
                    arr, gray_full, self.edge_margin_pixels)

            # --- 自动加深文字 ---
            darken_applied = False
            if self.auto_darken:
                # 判断文字是否偏浅：统计文字像素(灰度 30~150)的平均灰度，
                # 偏浅(>110)才加深；已经很深的文字不处理，避免过度加深。
                # (直接用管线灰度，不再重复转换)
                text_px = gray_full[(gray_full > 30) & (gray_full < 150)]
                if text_px.size > 500 and float(text_px.mean()) > 110:
                    arr, gray_full = self.darken_text(arr, gray_full, gamma=1.3)
                    darken_applied = True

            img = Image.fromarray(arr)

            # 输出路径：保持输入目录结构(相对输入目录)，每个子目录对应生成输出子目录
            if output_path is None:
                rel_path = os.path.relpath(image_path, self.input_dir)
                output_path = os.path.join(self.output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if circles_info:
                img.save(output_path, quality=95, dpi=orig_dpi)
            else:
                # 未检测到圆洞：检查去黑边是否改了图
                img.save(output_path, quality=95, dpi=orig_dpi)
            # 保存后落盘校验：防磁盘写满/权限不足/杀软拦截等造成的静默缺失，
            # 确保“处理成功”必有对应非空输出文件(与批处理终结核对双重保险)。
            if not (os.path.exists(output_path) and os.path.getsize(output_path) > 0):
                raise IOError(f"输出文件未生成或为空: {output_path}")

            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'success': True,
                'circles_found': len(circles_info),
                'shadows_removed': shadows_removed,
                'deskew_angle': deskew_applied,
                'darken_applied': darken_applied,
                'output_path': output_path,
                'preview_before': image_path,
                'preview_after': output_path
            }

        except Exception as e:
            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'success': False,
                'error_msg': str(e),
                'circles_found': 0,
                'shadows_removed': 0,
                'deskew_angle': 0.0,
                'darken_applied': False
            }

    def detect_detection_boundaries(self, black_mask, img_width, img_height):
        """
        智能检测左右边界：
        1. 检测最左和最右的文字位置
        2. 检测长竖线位置
        3. 根据检测结果确定检测区域
        
        返回: (left_boundary, right_boundary)
        """
        # 计算每列的黑色像素数量（垂直投影）
        column_sums = np.sum(black_mask, axis=0)
        
        # 检测长竖线：连续多列都有较多黑色像素
        vertical_line_threshold = img_height * 0.3  # 竖线至少覆盖30%高度
        min_vertical_line_cols = 2  # 至少2列连续
        
        left_vertical_line_x = None
        right_vertical_line_x = None
        
        # 查找左侧最近的竖线
        consecutive_cols = 0
        for x in range(img_width):
            if column_sums[x] >= vertical_line_threshold:
                consecutive_cols += 1
                if consecutive_cols >= min_vertical_line_cols and left_vertical_line_x is None:
                    left_vertical_line_x = x
            else:
                consecutive_cols = 0
        
        # 查找右侧最近的竖线
        consecutive_cols = 0
        for x in range(img_width - 1, -1, -1):
            if column_sums[x] >= vertical_line_threshold:
                consecutive_cols += 1
                if consecutive_cols >= min_vertical_line_cols and right_vertical_line_x is None:
                    right_vertical_line_x = x
            else:
                consecutive_cols = 0
        
        # 检测文字边界：使用连通分量分析区分文字和圆圈
        # 优先用 cv2（C 实现，极快）；无 cv2 时回退到纯 Python 实现
        num_fg, stats = self._connected_components_with_stats(black_mask)

        # 找出所有连通区域的边界框，并分类
        text_leftmost = img_width
        text_rightmost = 0
        has_text_or_lines = False

        for min_row, min_col, max_row, max_col, pixel_count in self._iter_components(num_fg, stats):
            if pixel_count < 10:  # 忽略太小的区域（可能是噪点或小圆圈）
                continue

            height = max_row - min_row
            width = max_col - min_col
            area = height * width

            # 圆形候选（尺寸<=最大直径且接近方形）不当作“文字/线”。
            # 否则实心黑圆洞会因密度高被归为内容，把检测边界推到圆洞之外导致漏检。
            diameter = max(height, width)
            aspect = diameter / max(min(height, width), 1)
            if diameter <= self.max_diameter_pixels and aspect <= 3:
                continue

            # 判断是否为文字或竖线（而非圆圈）
            # 文字/竖线特征：
            # 1. 高度较大（超过图像高度5%）
            # 2. 或者宽高比异常（细长形状）
            # 3. 或者像素密度较高（实心区域）
            pixel_density = pixel_count / area if area > 0 else 0

            is_text_or_line = (
                (height > img_height * 0.05) or  # 高度超过5%
                (width > height * 2) or           # 宽远大于高（横线）
                (height > width * 2) or           # 高远大于宽（竖线）
                (pixel_density > 0.3 and pixel_count > 100)  # 高密度大区域
            )

            if is_text_or_line:
                has_text_or_lines = True
                text_leftmost = min(text_leftmost, min_col)
                text_rightmost = max(text_rightmost, max_col)
        
        # 情况3：没有文字和竖线，使用全图检测
        if not has_text_or_lines:
            return 0, img_width
        
        # 确定最终检测边界
        # 左侧：取竖线和文字中更靠外的
        if left_vertical_line_x is not None:
            left_boundary = min(left_vertical_line_x, text_leftmost)
        else:
            left_boundary = text_leftmost
        
        # 右侧：取竖线和文字中更靠外的
        if right_vertical_line_x is not None:
            right_boundary = max(right_vertical_line_x, text_rightmost)
        else:
            right_boundary = text_rightmost
        
        # 添加边距容差（15像素），确保能覆盖边缘的圆圈
        margin_tolerance = 15
        left_boundary = max(0, left_boundary - margin_tolerance)
        right_boundary = min(img_width, right_boundary + margin_tolerance)
        
        # 确保检测区域有效
        if left_boundary <= 0:
            left_boundary = 0
        if right_boundary >= img_width:
            right_boundary = img_width
        
        return left_boundary, right_boundary

    def find_black_circles_smart(self, black_mask, img_width, img_height, left_boundary, right_boundary):
        """
        在智能确定的检测区域内查找黑色圆圈
        返回圆圈信息列表：[(center_x, center_y, radius), ...]
        """
        circles = []
        searched = False

        # 提取左侧检测区域（从左边界到图像左边缘）
        if 0 < left_boundary < img_width:
            left_region = black_mask[:, :left_boundary]
            circles.extend(self.detect_circle_region(left_region, 0, img_height))
            searched = True

        # 提取右侧检测区域（从右边界到图像右边缘）
        if 0 < right_boundary < img_width:
            right_region = black_mask[:, right_boundary:]
            circles.extend(self.detect_circle_region(right_region, right_boundary, img_height))
            searched = True

        # 无边距区可搜（纯圆洞图、无文字内容，或内容占满全图）→ 全图检测，避免漏检
        if not searched:
            circles.extend(self.detect_circle_region(black_mask, 0, img_height))

        return circles

    def detect_edge_holes(self, mask, img_w, img_h, gray=None):
        """Edge band hole detection (single pass, default solidity)."""
        mp = self.margin_pixels
        candidates = []
        if 0 < mp < img_w // 2:
            for cx, cy, r in self.detect_circle_region(mask[:, :mp], 0, img_h):
                candidates.append((cx, cy, r, 'L'))
            for cx, cy, r in self.detect_circle_region(mask[:, img_w - mp:], img_w - mp, img_h):
                candidates.append((cx, cy, r, 'R'))
        if 0 < mp < img_h // 2:
            for cx, cy, r in self.detect_circle_region(mask[:mp, :], 0, mp):
                candidates.append((cx, cy, r, 'T'))
            for cx, cy, r in self.detect_circle_region(mask[img_h - mp:, :], 0, mp):
                candidates.append((cx, cy + (img_h - mp), r, 'B'))
        return self._filter_punch_holes(candidates, img_w, img_h, mask, gray)

    def _is_isolated_hole(self, mask, cx, cy, r, img_w, img_h):
        """
        判断一个候选是否为真装订孔(用于排除标题/印章粘连块)。
        真孔四周贴近区是白纸，邻域环带内没有其它黑色连通域；而标题/印章粘连块
        紧邻其它笔画，环带内会出现多个独立黑色连通域。
        在候选外围环带(1.3r~2.2r)统计独立黑色连通域数。
        环带半径取 2.2r(而非更大)：真孔即使附近有表格/文字行(2.2r 外)，贴近区
        仍是干净的；标题粘连块的相邻笔画就在 2.2r 内。阈值 sibs<3：
        真孔贴近区兄弟=0；标题块 2.2r 典型>=4。
        """
        r = int(r)
        inner = int(r * 1.3)   # 略大于候选本体，排除候选自身
        outer = int(r * 2.2)
        x0, x1 = max(0, cx - outer), min(img_w, cx + outer + 1)
        y0, y1 = max(0, cy - outer), min(img_h, cy + outer + 1)
        sub = mask[y0:y1, x0:x1]
        if sub.size == 0:
            return True
        Hs, Ws = sub.shape
        yy, xx = np.mgrid[0:Hs, 0:Ws]
        sx, sy = (cx - x0), (cy - y0)
        dist2 = (xx - sx) ** 2 + (yy - sy) ** 2
        ring = (dist2 >= inner * inner) & (dist2 <= outer * outer)
        if ring.sum() < 20:
            return True  # 环带太小，无法判断，保守放行
        # 环带内的独立黑色连通域数(候选自身在 inner 之内，不计入)。
        # 只统计面积>=8且宽高均>=4的有效笔画——真孔上方邻行常有扫描噪点碎屑(1-7px)，
        # 它们不是"文字密集区"，不应把真孔误判为粘连块(导致底部单孔漏检)。
        # 宽高>=4另拦细长虚线碎片：页码行"— 39 —"破折号碎段(高2px)紧贴底部孔时，
        # 4个碎段会把真孔环带误判为文字密集区；真文字笔画高度>20，不受影响。
        ring_fg = (ring & (sub > 0)).astype(np.uint8)
        try:
            import cv2
            n_cc, _, st_arr, _ = cv2.connectedComponentsWithStats(ring_fg, 8)
            sibs = sum(1 for i in range(1, n_cc)
                       if st_arr[i, cv2.CC_STAT_AREA] >= 8
                       and st_arr[i, cv2.CC_STAT_WIDTH] >= 4
                       and st_arr[i, cv2.CC_STAT_HEIGHT] >= 4)
        except Exception:
            # 无 cv2 回退：用黑色像素占比近似
            sibs = 99 if float(ring_fg.mean()) > 0.05 else 0
        # 真孔贴近区有效笔画=0；标题/印章区 2.2r 典型>=4
        return sibs < 3

    def _filter_punch_holes(self, candidates, img_w, img_h, mask=None, gray=None):
        """Filter punch holes from edge candidates."""
        if not candidates:
            return []
        # 距边筛选带宽: 覆盖整个检测边带。此前取 margin*0.5(20mm/236px)——
        # 实测多批档案的装订孔打在距边 24-40mm(280-470px)处, 大量孔落在
        # 带外侧被整组丢弃(漏检)。放宽到全带宽后, 远端误入的表格/文字碎块
        # 由后续「大候选计数 + 邻域隔离 + 径向对比度」三重终检拦截。
        band = self.margin_pixels
        tol = max(self.max_diameter_pixels / 4, 1)
        floor = self.max_diameter_pixels * 0.03

        from collections import defaultdict
        by_edge = defaultdict(list)
        for cx, cy, r, edge in candidates:
            # 距最近纸边的距离：左右边用全带宽(装订孔主区, 实测孔距边24-40mm)；
            # 顶/底边保持半带宽——顶部带横跨整页宽, 放宽会把页中部标题/图形
            # (y在带内但远离纸边)误入, 如标题行y≈300距顶边300>236被正确排除。
            if edge in ('L', 'R'):
                near = min(cx, img_w - 1 - cx) <= band
            else:
                near = min(cy, img_h - 1 - cy) <= (band * 0.5)
            if near:
                by_edge[edge].append((cx, cy, r))

        kept = []
        for edge, comps in by_edge.items():
            vertical = edge in ('L', 'R')
            key_idx = 0 if vertical else 1   # 竖向边按 x 聚列，横向边按 y 聚排
            cols = []
            for c in sorted(comps, key=lambda c: c[key_idx]):
                placed = False
                for col in cols:
                    if abs(col[0][key_idx] - c[key_idx]) <= tol:
                        col.append(c)
                        placed = True
                        break
                if not placed:
                    cols.append([c])
            min_iso = self.max_diameter_pixels * 0.045
            max_per_col = 6  # 超过6个的列/排是文字(如标题行)，不是装订孔
            # 文字行 vs 装订孔列 判别：统计“大候选”数量。
            # 大候选 = 半径 >= 0.5*列内最大半径 且 >= 绝对阈值(12px)。
            # 装订孔列：真孔通常 3-6 个一排，大候选 >= 3；
            # 标题/文字行：即使笔画粘连成大块，大候选也只有 1-2 个(<=2)。
            # 用“大候选计数”比“半径中位数”更稳健——真孔列混入再多表格碎块
            # 也不影响大候选计数，而碎块会拉低中位数导致误杀。
            # 下限取整(14.75→14)：半径是整像素量，1px 抖动(如 JPEG 重压缩)不应翻转分支。
            big_abs_r = int(max(self.max_diameter_pixels * 0.05, 12))
            for col in cols:
                radii = sorted([c[2] for c in col])
                max_r = radii[-1]
                n_big = sum(1 for rr in radii if rr >= 0.5 * max_r and rr >= big_abs_r)
                # 文字行：大候选 < 3 → 整组丢弃
                if n_big < 3:
                    # 仅当确无成排大孔时才视为文字；保留极少数(<3)大候选
                    # 交给后续 _is_isolated_hole 邻域终检做最后裁决。
                    big_candidates = [(cx, cy, r) for cx, cy, r in col
                                      if r >= 0.5 * max_r and r >= big_abs_r]
                    kept.extend(big_candidates)
                    continue
                # 计算相对尺寸阈值：排除单个异常大值(如角落扫描伪影)的干扰。
                if len(radii) >= 3 and radii[-1] > radii[-2] * 1.5:
                    ref_r = radii[-2]  # 最大值是异常值，用第二大
                else:
                    ref_r = radii[-1]
                thresh = max(floor, ref_r * 0.5)
                filtered = [(cx, cy, r) for cx, cy, r in col if r >= thresh]
                if len(filtered) > max_per_col:
                    continue  # 过滤后仍太密集=文字行，跳过
                if len(filtered) >= 2:
                    kept.extend(filtered)
                elif len(col) == 1:
                    cx, cy, r = col[0]
                    if r >= min_iso:
                        kept.append((cx, cy, r))
        # 终检1 邻域上下文：逐一验证候选四周是否有其它黑色连通域(相邻文字笔画)。
        # 真孔处于白纸区(无兄弟)；标题/印章粘连块四周密布其它笔画 → 排除。
        if mask is not None and kept:
            kept = [c for c in kept
                    if self._is_isolated_hole(mask, c[0], c[1], c[2], img_w, img_h)]
        # 终检2 径向对比度：真装订孔是中心暗、向外亮的实心圆盘(中心 vs 外环
        # 灰度差大)；而闭运算把表格线/印章/散点连成的伪圆，中心与外环亮度接近
        # (对比度小)。有灰度图时启用，用对比度阈值剔除这类伪圆。
        if gray is not None and kept:
            kept = [c for c in kept
                    if self._is_solid_dark_disk(gray, c[0], c[1], c[2], img_w, img_h, mask)]
        return kept

    @staticmethod
    def _is_solid_dark_disk(gray, cx, cy, r, img_w, img_h, mask=None):
        """
        验证候选是否为实心暗圆盘(真装订孔)。真孔光学上是穿透的黑洞，中心区域
        像素极暗(灰度很低)且四周明显亮于中心，据此判据：
        1. 中心绝对暗度 + 外环对比度：中心区(0~0.5r)灰度均值 < 50，且外环
           (1.2~1.45r)与中心的对比度足够大(>=100)。真孔中心典型 1-10，白底/灰带内
           真孔外环 206-255(对比度 200-246)；而深灰颗粒噪点团中心虽暗(≈39)，
           但外环同暗(≈93，对比度仅 54)，靠外环对比度拦截。
        2. 径向对比度兜底：中心不够极暗(如孔中心采样恰好落在碎块间隙)时，
           仅凭对比度 >=100 也可通过。白底真孔对比度大(>=140)；
           表格线/印章/笔画粘连伪圆对比度小(<=80)被拒。
        3. 彩色封面(红/蓝底)打孔：外环不是白纸，对比度到不了100(实测红底封皮外环≈83、
           对比度≈80)，但中心仍是光学穿透的纯黑(<20)且盘芯在严格阈值下实心(填充率≥0.8)，
           叠加对比度>=55判真孔；深灰噪点团中心≈39、填充稀疏，双重拦截。
        """
        import math
        r = max(int(r), 4)
        # 中心区域均值(判据1与盘芯填充率联合判据都需要)
        ri = max(2, r // 3)
        x0, x1 = max(0, cx - ri), min(img_w, cx + ri + 1)
        y0, y1 = max(0, cy - ri), min(img_h, cy + ri + 1)
        center_box = gray[y0:y1, x0:x1]
        if center_box.size == 0:
            return True
        center_mean = float(center_box.mean())
        # 前置判据：盘芯原始掩码填充率(闭运算前)。真孔是光学穿透黑洞，盘芯在严格阈值下
        # 几乎全部像素直接<50(实测三批案例均≈1.0，最暗孔边缘碎裂也≥0.9)；
        # 而闭运算/降级小核把文字笔画粘连成的伪圆(如“四”字笔画团)，盘芯只有
        # 稀疏笔画，原始填充率低(实测字符块 0.37~0.64，中心均值 78~121)。
        # 联合拦截：填充率<0.70 且 中心不够极暗(>=30) 才拒绝——浅边真孔
        # (孔缘灰度47-56被严格阈值切掉)中心依然极暗(<20)，不受影响；
        # 字符块中心 78+ 被拦截。必须先于中心暗度判据：笔画恰好穿过盘芯时
        # 中心均值也可能<50，只有联合判据能区分实心黑洞与笔画拼合块。
        if mask is not None:
            rd = max(2, int(r * 0.4))
            dx0, dx1 = max(0, cx - rd), min(img_w, cx + rd + 1)
            dy0, dy1 = max(0, cy - rd), min(img_h, cy + rd + 1)
            core = mask[dy0:dy1, dx0:dx1]
            if core.size and float(core.mean()) < 0.70 and center_mean >= 30:
                return False
        # 外环亮度采样(判据1/2共用)
        outer_vals = []
        for ang_deg in range(0, 360, 30):
            rad = math.radians(ang_deg)
            for mul in (1.2, 1.45):
                ox = cx + int(r * mul * math.cos(rad))
                oy = cy + int(r * mul * math.sin(rad))
                if 0 <= ox < img_w and 0 <= oy < img_h:
                    outer_vals.append(float(gray[oy, ox]))
        if not outer_vals:
            return True
        outer_mean = float(np.mean(outer_vals))
        contrast = outer_mean - center_mean
        # 判据1：中心绝对暗度 + 外环对比度(拦截暗背景上的噪点团)
        if center_mean < 50:
            if contrast >= 100:
                return True
            # 判据3：彩色封面(红/蓝底)真孔——外环是封面色(灰度60~140)而非白纸，
            # 对比度到不了100(实测0003红封面外环≈83、对比度≈80)被误拒。
            # 真孔中心仍是光学穿透的纯黑(<20)，盘芯在严格阈值下实心(填充率≥0.8)；
            # 深灰噪点团中心≈39(≥20)、填充稀疏，进不了此分支；全暗均匀块对比度≈0过不了55。
            if center_mean < 20 and contrast >= 55 and mask is not None:
                rd = max(2, int(r * 0.4))
                dx0, dx1 = max(0, cx - rd), min(img_w, cx + rd + 1)
                dy0, dy1 = max(0, cy - rd), min(img_h, cy + rd + 1)
                core = mask[dy0:dy1, dx0:dx1]
                if core.size and float(core.mean()) >= 0.8:
                    return True
            return False
        # 判据2：径向对比度兜底(中心采样落在碎块间隙时)
        return contrast >= 100

    @staticmethod
    def _dedup_circles(circles):
        """按中心距离去重(中心距 < 较小半径视为同一圆)。"""
        unique = []
        for cx, cy, r in circles:
            r = int(r)
            is_dup = False
            for ux, uy, ur in unique:
                if (cx - ux) ** 2 + (cy - uy) ** 2 < min(r, int(ur)) ** 2:
                    is_dup = True
                    break
            if not is_dup:
                unique.append((int(cx), int(cy), r))
        return unique

    def find_black_circles(self, black_mask, img_width, img_height):
        """
        在黑色掩码中查找圆形区域（仅在两侧边距范围内检测）
        返回圆圈信息列表：[(center_x, center_y, radius), ...]
        """
        circles = []
        
        # 计算左右两侧的边界（仅检测距离边缘margin_pixels范围内的区域）
        left_boundary = self.margin_pixels  # 左侧检测区域的右边界
        right_boundary = img_width - self.margin_pixels  # 右侧检测区域的左边界
        
        # 确保边界有效
        if left_boundary <= 0 or right_boundary >= img_width or left_boundary >= right_boundary:
            # 如果图像宽度太小，无法划分边距区域，则不检测
            return circles
        
        # 提取左侧边距区域（从左边到left_boundary）
        left_region = black_mask[:, :left_boundary]
        # 提取右侧边距区域（从right_boundary到右边）
        right_region = black_mask[:, right_boundary:]

        # 检测左侧圆圈（offset_x为0，因为是从x=0开始）
        left_circles = self.detect_circle_region(left_region, 0, img_height)
        circles.extend(left_circles)

        # 检测右侧圆圈（offset_x为right_boundary，因为是从right_boundary开始）
        right_circles = self.detect_circle_region(right_region, right_boundary, img_height)
        circles.extend(right_circles)

        return circles

    def detect_circle_region(self, region_mask, offset_x, img_height):
        """
        在指定区域检测黑色圆圈
        """
        circles = []
        height, width = region_mask.shape

        if not region_mask.any():  # 区域内无黑色像素(原 np.where 取索引未被使用)
            return circles

        # 简单的聚类方法：将接近的黑色像素归为一组
        min_distance = self.max_diameter_pixels // 2

        # 形态学闭运算：把因阈值边缘不饱满而被切碎的装订孔碎片重新合并成整圆。
        # 某些扫描件装订孔灰度均值仅 47-56，严格阈值(<50)会切掉孔的浅色边缘，
        # 导致一个整孔碎裂成多个细长小块，达不到实心度/宽高比要求而漏检。
        # 用接近预期孔半径的椭圆核做闭运算，能在不放宽灰度阈值(避免引入文字)
        # 的前提下让碎片重连。无 cv2 时跳过(降级为原行为)。
        raw_mask = region_mask  # 保留闭运算前的掩码，用于后续验证
        try:
            import cv2
            # 闭运算核半径：取预期装订孔半径的约一半(常见孔半径15-40px → 核半径10)
            k = max(7, int(self.max_diameter_pixels * 0.035))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k * 2 + 1, k * 2 + 1))
            closed = cv2.morphologyEx(region_mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
            region_mask = closed > 0
        except Exception:
            # 无 cv2 回退：移位并/或运算实现小半径闭运算(3x3十字核×3次≈半径3)，
            # 仍能把轻微碎裂的孔边缘重连，避免缺 cv2 时孔碎裂漏检。
            m = (region_mask > 0).astype(np.uint8)
            for _ in range(3):
                d = m.copy()
                d[1:, :] |= m[:-1, :]; d[:-1, :] |= m[1:, :]
                d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
                e = d.copy()
                e[1:, :] &= d[:-1, :]; e[:-1, :] &= d[1:, :]
                e[:, 1:] &= d[:, :-1]; e[:, :-1] &= d[:, 1:]
                m = e
            region_mask = m > 0

        def _emit_components(src_mask):
            """对给定掩码做连通域几何筛选，输出圆候选。"""
            out = []
            num_fg_l, stats_l = self._connected_components_with_stats(src_mask)
            for min_row, min_col, max_row, max_col, pixel_count in self._iter_components(num_fg_l, stats_l):
                # 降低最小像素数要求，以检测小圆圈（从10降到5）
                if pixel_count < 5:  # 忽略太小的噪点
                    continue

                # 计算直径
                diameter = max(max_row - min_row, max_col - min_col)

                # 检查是否符合圆圈尺寸要求
                if diameter > self.max_diameter_pixels:
                    continue
                # 实际装订孔半径通常 15-40px；超过 max_diameter*0.2(~59px=10mm半径) 的大块
                # 不是装订孔而是印章/图形/表格区
                if diameter > self.max_diameter_pixels * 0.4:
                    continue

                # 额外检查：确保是近似圆形的（不是细长的线）
                # 宽高比 = 长边 / 短边（短边至少为1，避免除零）。圆≈1.0，细线条会很大。
                aspect_ratio = max(max_row - min_row, max_col - min_col) / max(min(max_row - min_row, max_col - min_col), 1)
                if aspect_ratio > 3:  # 如果宽高比超过3，可能是线条而非圆圈
                    continue

                # 实心度(solidity)：真圆洞(实心圆盘)密度高(≈0.78)；手写笔画/线条密度低
                bw, bh = max_col - min_col, max_row - min_row
                solidity = pixel_count / (bh * bw) if bh * bw > 0 else 0
                min_big_diam = self.max_diameter_pixels * 0.09
                if not (solidity >= 0.5 or (solidity >= 0.45 and diameter >= min_big_diam)):
                    continue

                # 闭运算前验证已下放：detect_circle_region 只负责几何筛选，
                # 伪圆(表格线粘连)的剔除交给 _is_isolated_hole 的邻域上下文终检。
                center_y = (min_row + max_row) // 2
                center_x = (min_col + max_col) // 2 + offset_x
                out.append((center_x, center_y, diameter // 2))
            return out

        # 双通道检测：先在原始掩码上找形态完好的独立圆，再叠加闭运算掩码补检碎裂孔。
        # 闭运算大核(半径~10)会把贴近页码/表格线的孔与邻物粘成一大块——实心度被稀释、
        # 宽高比超标，反而漏检(实测横版报告底部孔紧贴页码行仅20px)。原始通道让独立
        # 完整的孔不受闭运算污染；闭运算通道只补充原始掩码中碎裂未成形的孔，按圆重叠去重。
        circles = _emit_components(raw_mask)
        num_fg, stats = self._connected_components_with_stats(region_mask)

        for min_row, min_col, max_row, max_col, pixel_count in self._iter_components(num_fg, stats):
            # 降低最小像素数要求，以检测小圆圈（从10降到5）
            if pixel_count < 5:  # 忽略太小的噪点
                continue

            # 计算直径
            diameter = max(max_row - min_row, max_col - min_col)

            # 检查是否符合圆圈尺寸要求
            if diameter > self.max_diameter_pixels:
                continue
            # 实际装订孔半径通常 15-40px；超过 max_diameter*0.2(~59px=10mm半径) 的大块
            # 不是装订孔而是印章/图形/表格区
            if diameter > self.max_diameter_pixels * 0.4:
                continue

            # 额外检查：确保是近似圆形的（不是细长的线）
            # 宽高比 = 长边 / 短边（短边至少为1，避免除零）。圆≈1.0，细线条会很大。
            aspect_ratio = max(max_row - min_row, max_col - min_col) / max(min(max_row - min_row, max_col - min_col), 1)
            if aspect_ratio > 3:  # 如果宽高比超过3，可能是线条而非圆圈
                continue

            # 实心度(solidity)：真圆洞(实心圆盘)密度高(≈0.78)；手写笔画/线条密度低
            bw, bh = max_col - min_col, max_row - min_row
            solidity = pixel_count / (bh * bw) if bh * bw > 0 else 0
            min_big_diam = self.max_diameter_pixels * 0.09
            if not (solidity >= 0.5 or (solidity >= 0.45 and diameter >= min_big_diam)):
                continue

            # 闭运算前验证已下放：detect_circle_region 只负责几何筛选，
            # 伪圆(表格线粘连)的剔除交给 _is_isolated_hole 的邻域上下文终检。

            # 计算中心点和半径
            center_y = (min_row + max_row) // 2
            center_x = (min_col + max_col) // 2 + offset_x
            radius = diameter // 2

            # 与原始通道已检出的圆重叠 → 同一孔的闭运算粘连变体，跳过避免重复变形坐标
            dup = False
            for ex, ey, er in circles:
                if (center_x - ex) ** 2 + (center_y - ey) ** 2 <= (radius + er) ** 2:
                    dup = True
                    break
            if dup:
                continue

            circles.append((center_x, center_y, radius))

        return circles

    def label_connected_components(self, binary_mask):
        """
        简单的连通分量标记算法（4连通）- 不使用scipy
        返回标记后的数组和特征数量
        """
        height, width = binary_mask.shape
        labeled = np.zeros((height, width), dtype=int)
        current_label = 0
        
        # 简化的洪水填充算法
        visited = np.zeros((height, width), dtype=bool)
        
        for y in range(height):
            for x in range(width):
                if binary_mask[y, x] and not visited[y, x]:
                    current_label += 1
                    # BFS洪水填充
                    queue = [(y, x)]
                    visited[y, x] = True
                    labeled[y, x] = current_label
                    
                    while queue:
                        cy, cx = queue.pop(0)
                        # 检查4个方向的邻居
                        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < height and 0 <= nx < width:
                                if binary_mask[ny, nx] and not visited[ny, nx]:
                                    visited[ny, nx] = True
                                    labeled[ny, nx] = current_label
                                    queue.append((ny, nx))
        
        return labeled, current_label

    def _connected_components_with_stats(self, binary_mask):
        """
        连通域分析，返回 (num_fg, stats)。
        - num_fg: 前景连通域数量
        - stats: (num_fg+1, 5) 数组，每行 [left, top, width, height, area]；
                 第 0 行为背景/占位，前景连通域为 1..num_fg。
        优先用 cv2（C 实现，比纯 Python 洪水填充快上百倍，且直接给出 bbox/面积，
        无需逐域 np.where 扫描）；cv2 不可用时回退到 label_connected_components +
        逐域统计（与原实现等价，仅较慢）。
        """
        mask_u8 = binary_mask.astype(np.uint8)
        try:
            import cv2
            # connectivity=4，与原 label_connected_components 的 4 连通保持一致
            # 注意：必须用关键字传参，位置参数 4 会被当作 ltype 而非 connectivity
            num, _labels, stats, _centroids = cv2.connectedComponentsWithStats(mask_u8, connectivity=4)
            # cv2 的 num 含背景(label 0)，前景数 = num-1；stats[0] 为背景
            return num - 1, stats
        except Exception:
            labels, num_fg = self.label_connected_components(binary_mask)
            stats = self._build_stats_from_labels(labels, num_fg)
            return num_fg, stats

    def _connected_components_full(self, binary_mask):
        """
        连通域分析(含标记图)，返回 (num_fg, labels, stats)。
        需要逐域像素掩码(labels==i)的场景使用。优先 cv2(8连通)；无 cv2 回退纯
        Python 洪水填充(4连通，降级环境下的近似)。
        """
        mask_u8 = binary_mask.astype(np.uint8)
        try:
            import cv2
            num, labels, stats, _centroids = cv2.connectedComponentsWithStats(mask_u8, connectivity=8)
            return num - 1, labels, stats
        except Exception:
            labels, num_fg = self.label_connected_components(binary_mask)
            stats = self._build_stats_from_labels(labels, num_fg)
            return num_fg, labels, stats

    @staticmethod
    def _build_stats_from_labels(labels, num_fg):
        """由标记图构建 stats 数组（cv2 不可用时的回退路径，语义对齐 cv2）。"""
        stats = np.zeros((num_fg + 1, 5), dtype=np.int64)
        for lab in range(1, num_fg + 1):
            ys, xs = np.where(labels == lab)
            if ys.size == 0:
                continue
            xmin, xmax = int(xs.min()), int(xs.max())
            ymin, ymax = int(ys.min()), int(ys.max())
            stats[lab, 0] = xmin                       # left
            stats[lab, 1] = ymin                       # top
            stats[lab, 2] = xmax - xmin + 1           # width
            stats[lab, 3] = ymax - ymin + 1           # height
            stats[lab, 4] = ys.size                    # area(pixel count)
        return stats

    @staticmethod
    def _iter_components(num_fg, stats):
        """
        生成每个前景连通域的 (min_row, min_col, max_row, max_col, pixel_count)。
        语义与原 np.where(labeled==label) 计算的边界框完全一致，供检测逻辑直接复用。
        """
        for i in range(1, num_fg + 1):
            left = int(stats[i, 0])
            top = int(stats[i, 1])
            w = int(stats[i, 2])
            h = int(stats[i, 3])
            area = int(stats[i, 4])
            yield top, left, top + h - 1, left + w - 1, area

    def crop_circles(self, img, circles_info, arr=None):
        """
        用与底色一致的颜色填充圆洞区域：在每个圆洞外围采样局部背景色再填充。
        白底图填白、彩底图填对应底色，避免彩色底图上出现刺眼白斑。
        arr：原图 numpy 数组(管线传引用，省一次重复的 np.array(img))，缺省内部转换。
        """
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        if arr is None:
            arr = np.array(img)  # 原始未绘制状态，用于采样背景色
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3

        for center_x, center_y, radius in circles_info:
            padding = max(5, radius // 10)
            adjusted_radius = radius + padding

            x1 = max(0, int(center_x - adjusted_radius))
            y1 = max(0, int(center_y - adjusted_radius))
            x2 = min(W, int(center_x + adjusted_radius))
            y2 = min(H, int(center_y + adjusted_radius))

            # 在填充框外围采样背景色：取亮度较高的像素(排除暗的圆洞/文字)，中位数作为底色
            s = max(4, adjusted_radius // 3)
            sx1, sy1 = max(0, x1 - s), max(0, y1 - s)
            sx2, sy2 = min(W, x2 + s), min(H, y2 + s)
            sample = arr[sy1:sy2, sx1:sx2]
            if rgb:
                bright = sample[sample.mean(axis=2) > 80]
                color = tuple(int(v) for v in np.median(bright, axis=0)) if len(bright) else (255, 255, 255)
            else:
                bright = sample[sample > 80]
                color = int(np.median(bright)) if bright.size else 255

            draw.ellipse([x1, y1, x2, y2], fill=color)

        return img_copy

    def cleanup_known_hole_residue(self, arr, gray, circles_info):
        """
        已知装订孔位的阴影定点清理：孔填充后，孔周常残留浅灰环影(冲头压痕/扫描泛光)；
        当孔紧贴灰色扫描竖带时，残影与竖带连成巨型连通域，通用孔影检测(按连通域直径)
        会被整体拒绝。此处以检测阶段已确认的孔位为先验，对孔周浅灰残影做定点填充。
        安全：只动浅灰像素(>=90)，深色墨迹像素不覆盖；填充圆内有墨迹连通域时整孔放弃。
        填充色取孔外环带浅灰中位数(灰带内取灰带色、白底取白)，使孔位融入周边背景。
        纯 numpy 实现，无 cv2 亦可用。
        输入/输出为管线传引用的 numpy 数组，写像素处用同一整除公式同步灰度。
        返回 (结果数组, 同步灰度数组, 填充孔数)。
        """
        if not circles_info:
            return arr, gray, 0
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3
        page_bg = float(np.percentile(gray, 75))
        if page_bg < 150:
            return arr, gray, 0  # 暗底扫描件不适用残影概念(与 remove_hole_shadow_residue 一致)
        out = arr.copy()
        g_out = None  # 惰性拷贝：多数页无残影，可省一次全图灰度拷贝
        filled = 0
        for cx, cy, r in circles_info:
            r = int(r)
            rf = r + max(10, int(r * 0.35))  # 覆盖残影环(实测孔影外延约0.3r)
            x0, x1 = max(0, cx - rf), min(W, cx + rf + 1)
            y0, y1 = max(0, cy - rf), min(H, cy + rf + 1)
            if x1 - x0 < 4 or y1 - y0 < 4:
                continue
            crop = gray[y0:y1, x0:x1]
            cw, ch = x1 - x0, y1 - y0
            # 墨迹保护：填充框内有墨迹连通域(面积>=80，或延伸出填充框的笔画)则放弃整孔，
            # 防止把贴孔文字/手写一并抹掉；框内居中小碎屑随残影一起填。
            n_cc, lab, st = self._connected_components_full(crop < 85)
            blocked = False
            yy, xx = np.mgrid[y0:y1, x0:x1]
            ell = ((xx - cx) ** 2 + (yy - cy) ** 2) <= rf * rf
            for j in range(1, n_cc + 1):
                l3 = int(st[j, 0]); t3 = int(st[j, 1])
                w3 = int(st[j, 2]); h3 = int(st[j, 3])
                a3 = int(st[j, 4])
                # 微碎屑(<30px)直接忽略：灰色暗带上常见 1-4px 压缩噪声触框，
                # 若按"延伸出填充框"拦截会误杀整孔(实测 018 两孔被 3-4px 碎屑阻塞)
                if a3 < 30:
                    continue
                if a3 < 80 and l3 > 0 and t3 > 0 and l3 + w3 < cw and t3 + h3 < ch:
                    continue
                cm3 = lab[t3:t3 + h3, l3:l3 + w3] == j
                if (cm3 & ell[t3:t3 + h3, l3:l3 + w3]).any():
                    blocked = True
                    break
            if blocked:
                continue
            sub_g = crop.astype(np.float32)
            ell_sub = ell
            # 残影像素：填充盘内非墨迹(>=90)像素全部重填——含浅灰环影、已被填白的孔内区、
            # 以及低对比过渡尾。孔内区一并重填为周边背景色，避免白底填色在灰带上留白圈。
            residue = ell_sub & (sub_g >= 90)
            if not residue.any():
                continue
            # 填充色：孔外环带(rf~1.8rf)内浅灰像素中位数，使孔位融入周边背景。
            ell_o = ((xx - cx) ** 2 + (yy - cy) ** 2) <= (rf * 1.8) ** 2
            ann = ell_o & ~ell_sub & (crop >= 90) & (crop <= page_bg + 5)
            if rgb:
                s_arr = arr[y0:y1, x0:x1]
                color = (tuple(int(v) for v in np.median(s_arr[ann].reshape(-1, 3), axis=0))
                         if int(ann.sum()) >= 30 else (255, 255, 255))
            else:
                color = int(np.median(crop[ann])) if int(ann.sum()) >= 30 else 255
            sub = out[y0:y1, x0:x1]
            sub[residue] = color
            out[y0:y1, x0:x1] = sub
            # 同步更新灰度(与 _gray_u8 同一整除公式，逐位一致)
            if g_out is None:
                g_out = gray.copy()
            if rgb:
                g_out[y0:y1, x0:x1][residue] = (color[0] + color[1] + color[2]) // 3
            else:
                g_out[y0:y1, x0:x1][residue] = color
            filled += 1
        if filled == 0:
            return arr, gray, 0
        return out, g_out, filled

    def remove_edge_vertical_band(self, arr, gray):
        """
        去除紧贴左/右纸边的竖向扫描暗带(装订侧盖板阴影/纸张翘起泛光)。
        此类暗带纵贯全页、从纸边向内平滑渐变，孔填充后仍残留一条灰/黑竖带。
        连通域式去黑边对它无效：暗带与正文墨迹经表格线相连时连通域巨大，
        被面积上限(12%)拒绝；浅灰渐变部分又够不着暗阈值。故改用「列剖面」检测：
        从纸边向内前景比率连续高(软阈值>0.35)即暗带，按比率剖面自适应定带宽。
        安全(缺一不可)：
          1. 暗带必须靠边(峰值列距图边<200；歪斜纸纠偏后纸边与图边间可能有白条，
             此时要求峰值与图边之间的背景条前景<20%)且纵向连续(覆盖率>=70%)；
          2. 内部区高纹理(文字)占比>10%时整侧放弃——通过后软阴影像素可填，
             但彩墨像素(色散>30，如红章/彩笔)永不覆盖；
          3. 过渡区(带外侧渐变尾)收窄到更暗阈值(底色-60)之外才填且受墨迹保护，
             保护贴边但越界的手写/印章笔画。
        纯 numpy 实现，无 cv2 亦可用。输入/输出为管线传引用的 numpy 数组。
        返回 (结果数组, 同步灰度数组, 被填充像素数, 15×15局部标准差)——
        未改图时局部标准差可供后续去黑边环节复用(同一灰度，逐位一致)，已改图时为 None。
        """
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3
        page_bg = float(np.percentile(gray, 75))
        if page_bg < 150:
            return arr, gray, 0, None  # 暗底扫描件不处理(与其他边缘清理一致)
        body = slice(100, H - 100) if H > 400 else slice(0, H)
        body_h = body.stop - body.start
        if body_h < 200:
            return arr, gray, 0, None

        # 填充底色：取接近纸面白的像素中位(75 分位会被暗带亮部拉低，改取 90 分位)
        bgmask = gray >= float(np.percentile(gray, 90))
        if rgb:
            bgpx = arr[bgmask]
            bg = (tuple(int(v) for v in np.median(bgpx.reshape(-1, 3), axis=0))
                  if len(bgpx) else (255, 255, 255))
        else:
            bg = int(np.median(arr[bgmask])) if bgmask.any() else 255

        gf = gray.astype(np.float32)
        gmean, gsq = self._blur_pair(gf, 15)
        local_std = np.sqrt(np.maximum(gsq - gmean * gmean, 0))

        max_scan = min(W // 3, max(self.margin_pixels, 200))
        soft_thr = page_bg - 8    # 软阴影像素(含浅灰渐变尾)
        hard_thr = page_bg - 60  # 过渡区收窄阈值(墨迹保护线)

        fill_in = np.zeros((H, W), dtype=bool)    # 带内部：已过纹理校验，全量软阴影可填
        fill_tail = np.zeros((H, W), dtype=bool)  # 过渡区：保守填充，受墨迹保护
        for side in ('L', 'R'):
            # 右侧条带翻转：保证 prof[0]=图边、向内递增(与左侧同构)
            if side == 'L':
                strip_g = gray[body, :max_scan]
                strip_s = local_std[body, :max_scan]
            else:
                strip_g = gray[body, W - max_scan:][:, ::-1]
                strip_s = local_std[body, W - max_scan:][:, ::-1]
            prof = (strip_g < soft_thr).mean(axis=0)
            if len(prof) < 8:
                continue
            pk = int(np.argmax(prof[:min(len(prof), 250)]))
            if pk >= 200 or prof[pk] < 0.35:
                continue  # 峰值远离图边或前景不足：不是边缘暗带
            # 向外(图边方向)扩展：渐变尾阈值放宽到0.10(009型带从纸边渐进变暗；
            # 018型歪纸纠偏后纸边与图边间有白条，扩展到谷底自然停)
            s = pk
            while s > 0 and prof[s - 1] >= 0.10:
                s -= 1
            bw = pk + 1
            thr_w = max(prof[pk] - 0.35, 0.25)
            for x in range(pk + 1, min(pk + 100, len(prof))):
                if prof[x] < thr_w:
                    break
                bw = x + 1
            bw = min(bw, pk + 90)
            if bw - s < 8:
                continue
            # 纵向连续：带内列前景比率>=0.30 的占比>=70%
            if (prof[s:bw] >= 0.30).mean() < 0.70:
                continue
            in_dark = strip_g[:, s:bw] < soft_thr  # strip 坐标系(两侧同构)
            if not in_dark.any():
                continue
            if float((strip_s[:, s:bw][in_dark] > 50).mean()) > 0.10:
                continue  # 暗带内有大量文字纹理，放弃该侧
            # 过渡区：软剖面>10% 再外延<=30 列，填充收窄到 hard_thr 之外
            tail = 0
            for x in range(bw, min(bw + 30, len(prof))):
                if prof[x] < 0.10:
                    break
                tail += 1
            if side == 'L':
                xs0, xs1 = s, bw
                xt0, xt1 = bw, bw + tail
            else:
                xs0, xs1 = W - bw, W - s
                xt0, xt1 = W - bw - tail, W - bw
            b_in = np.zeros((H, W), dtype=bool)
            b_in[body, xs0:xs1] = gray[body, xs0:xs1] < soft_thr
            b_tail = np.zeros((H, W), dtype=bool)
            b_tail[body, xt0:xt1] = ((gray[body, xt0:xt1] >= 90) &
                                     (gray[body, xt0:xt1] < hard_thr))
            if not b_in.any():
                continue
            fill_in |= b_in
            fill_tail |= b_tail

        if not fill_in.any():
            return arr, gray, 0, local_std  # 未改图：局部标准差可供去黑边环节复用
        ink_mask = gray < (page_bg - 80)  # 过渡区深墨迹不覆盖(内部区已过纹理校验不受限)
        fill_tail = fill_tail & ~ink_mask
        fill = fill_in | fill_tail
        # 彩墨保护：扫描暗带是装订盖板阴影，必为无彩灰色渐变；色散>30 的像素是
        # 彩色内容(红章/彩笔)，不是暗带。实测 0054 页右下蓝色阴影上的半圆红章被
        # 列剖面误判为右侧暗带，印章暗红像素(灰度≈90-110 落入软阴影阈值)被填白。
        if rgb:
            chroma = (arr.max(axis=2).astype(np.int16) - arr.min(axis=2).astype(np.int16))
            fill = fill & (chroma <= 30)
        if not fill.any():
            return arr, gray, 0, local_std  # 墨迹/彩墨过滤后无填充：图未变，标准差仍可复用
        out_arr = arr.copy()
        out_arr[fill] = bg
        # 同步更新灰度(与 _gray_u8 同一整除公式，逐位一致)
        g_out = gray.copy()
        g_out[fill] = (bg[0] + bg[1] + bg[2]) // 3 if rgb else bg
        return out_arr, g_out, int(fill.sum()), None

    # ==================== 空白区订书机孔散点清理 + 印章保护 ====================

    @staticmethod
    def _content_bbox(mask, pad_ratio=0.02):
        """主体内容bbox：暗像素的5~95分位外扩pad。无内容返回None。
        用5%分位(而非1%): 散点/订书钉等离群暗点会把1%分位拉到自身位置,
        使其落入内容bbox内而漏清(实测单点在x=70把x_lo拉到61)。
        5%分位下离群点占比<5%时不影响边界。"""
        ys, xs = np.where(mask)
        if len(ys) < 100:
            return None
        y_lo, y_hi = np.percentile(ys, [5, 95])
        x_lo, x_hi = np.percentile(xs, [5, 95])
        py = (y_hi - y_lo) * pad_ratio
        px = (x_hi - x_lo) * pad_ratio
        return (int(x_lo - px), int(y_lo - py), int(x_hi + px), int(y_hi + py))

    @staticmethod
    def _detect_seal_protect_zones(arr, gray, dark_mask=None):
        """
        检测印章保护区域(圆bbox列表)。印章是合法内容, 散点清理绝不触碰:
          1. 红色印章: R>G+40 且 R>B+40 且 R>90 的红色块(任何尺寸);
          2. 黑色规则印章: d>=60px + 近圆(长宽比<=1.6) + 圆度>=0.35;
          3. 残缺印章碎块: d 20~60px 且实心度<0.5(笔画/环状) — 整块保护;
          4. 粘连保护: 印章区域外扩60px内的散点也跳过(章边印泥点)。
        dark_mask：调用方已有的 (gray<80) uint8 掩码(散点环节同源复用，避免重复全图比较)。
        返回 [(cx, cy, protect_radius), ...]。
        """
        try:
            import cv2
        except ImportError:
            return []
        zones = []
        H, W = gray.shape
        rgb = arr.ndim == 3

        def add_zone(cx, cy, reach):
            zones.append((cx, cy, reach))

        # 1) 红色印章(最强特征, 优先)
        if rgb:
            R = arr[:, :, 0].astype(np.int16)
            G = arr[:, :, 1].astype(np.int16)
            B = arr[:, :, 2].astype(np.int16)
            red = ((R - G > 40) & (R - B > 40) & (R > 90)).astype(np.uint8)
            if red.sum() > 200:
                k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
                cl = cv2.morphologyEx(red, cv2.MORPH_CLOSE, k)
                n, _, st, _ = cv2.connectedComponentsWithStats(cl, 8)
                for i in range(1, n):
                    a = st[i, 4]
                    if a < 500:
                        continue
                    l, t, w2, h2 = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
                    cx, cy = l + w2 // 2, t + h2 // 2
                    add_zone(cx, cy, max(w2, h2) // 2 + 60)

        # 2)+3) 黑色印章块: 单阈值全图暗块分析(含残章)
        # 残章碎块保护限定在"内容区附近"(距内容bbox边<=200px):
        # 远离内容区的边缘碎块是订书钉/装订残物而非印章(印章盖在文字区上),
        # 不保护(否则顶部空白带的订书钉被整带保护导致散点清理失效)。
        # 内容bbox由调用方散点清理的主区bbox近似传入 → 此处自行重算。
        dark = dark_mask if dark_mask is not None else (gray < 80).astype(np.uint8)
        n2, _, st2, _ = cv2.connectedComponentsWithStats(dark, 8)
        near_content = None
        if dark.sum() > 5000:
            ys2, xs2 = np.where(dark)
            y2lo, y2hi = np.percentile(ys2, [2, 98])
            x2lo, x2hi = np.percentile(xs2, [2, 98])
            near_content = (x2lo - 120, y2lo - 120, x2hi + 120, y2hi + 120)
        for i in range(1, n2):
            a = st2[i, 4]
            if a < 300:
                continue
            l, t, w2, h2 = st2[i, 0], st2[i, 1], st2[i, 2], st2[i, 3]
            d = max(w2, h2)
            asp = d / max(min(w2, h2), 1)
            sol = a / (w2 * h2) if w2 * h2 else 0
            cx, cy = l + w2 // 2, t + h2 // 2
            if d >= 60 and asp <= 1.6:
                # 圆度: 面积/外接圆面积(印章环+文字典型>=0.35)
                circ = a / (np.pi * (d / 2.0) ** 2) if d > 0 else 0
                if circ >= 0.35:
                    add_zone(cx, cy, d // 2 + 60)
            elif 20 <= d <= 60 and sol < 0.5:
                # 残缺印章碎块(笔画/环状低实心): 仅在内容区附近保护;
                # 边缘远处的不保护(订书钉/装订残物)
                if near_content:
                    nx_lo, ny_lo, nx_hi, ny_hi = near_content
                    if nx_lo <= cx <= nx_hi and ny_lo <= cy <= ny_hi:
                        add_zone(cx, cy, d // 2 + 50)
        return zones

    @staticmethod
    def _text_line_bands(mask, min_x_extent=120, max_grow=45):
        """检出「文字行保护带」，返回 (row_band, (bx_lo, bx_hi))。

        row_band：长度 H 的 int32 数组，第 y 行属于第 k 条保护带则为 k，否则 -1；
        bx_lo/bx_hi：各保护带内墨迹的 x 起止(列表，下标与 k 对应)。
        判定「点(cx,cy)是否落在文字行上」即 row_band[cy]>=0 且
        bx_lo[k]<=cx<=bx_hi[k]，O(1) 查表，不随候选数退化。

        为什么需要：散点清理把内容bbox(暗像素5~95分位)之外当空白区，但页首标题行/
        页脚行/表头行这类「暗像素总量占比不足5%」的合法文字行会整体落在分位bbox之外，
        其笔画暗核(gray<50)随后被逐个当订书钉散点填白，只剩 50~80 灰度的抗锯齿
        轮廓 → 成品出现「中空只有黑边缘线的文字」(实测 007/019/056 首行、0160 页首
        标题行、0270 表头行均被掏空)；整行成员还会被行带逻辑误判为「订书钉排」而
        放宽尺寸(d<=60)与形状校验，加剧破坏。

        判据(6张样张实测的可分特征)：文字行整行笔画横贯，单行暗像素峰值>=146；
        订书钉/散点带每行只有几个小点，单行峰值<=82。故：
          ① 种子行 row_ink >= max(100, 4%W) —— 阈值落在 82 与 146 的间隙中；
          ② 向上下按 row_ink >= max(30, 1.2%W) 生长(至多 max_grow 行)补全字符高度，
             行间空白(ink≈0)自然截断生长，故各文字行不会被并成一条；
          ③ 带内墨迹 x 跨度 >= min_x_extent 才算文字行(排除印章/污渍等紧凑暗块
             自成的带，避免其把邻域散点一并庇护)。
        """
        H, W = mask.shape
        row_ink = mask.sum(axis=1)
        seed_thr = max(100, int(0.04 * W))
        grow_thr = max(30, int(0.012 * W))
        seeds = np.where(row_ink >= seed_thr)[0]
        row_band = np.full(H, -1, dtype=np.int32)
        if seeds.size == 0:
            return row_band, ([], [])
        band = np.zeros(H, dtype=bool)
        band[seeds] = True
        grow = row_ink >= grow_thr
        for _ in range(max_grow):
            nb = band.copy()
            nb[1:] |= band[:-1] & grow[1:]    # 向下生长
            nb[:-1] |= band[1:] & grow[:-1]   # 向上生长
            if np.array_equal(nb, band):
                break
            band = nb
        ys = np.where(band)[0]
        # 切分连续段(段内允许<=6行的抗锯齿/字间空隙)
        runs = []
        start = prev = int(ys[0])
        for y in ys[1:]:
            y = int(y)
            if y - prev > 6:
                runs.append((start, prev))
                start = y
            prev = y
        runs.append((start, prev))
        bx_lo, bx_hi = [], []
        for y0, y1 in runs:
            xs = np.where(mask[y0:y1 + 1].any(axis=0))[0]
            if xs.size == 0:
                continue
            if int(xs.max()) - int(xs.min()) + 1 < min_x_extent:
                continue
            bid = len(bx_lo)
            bx_lo.append(int(xs.min()))
            bx_hi.append(int(xs.max()))
            row_band[y0:y1 + 1] = bid
        return row_band, (bx_lo, bx_hi)

    def remove_isolated_specks(self, arr, gray, seal_zones=None,
                              max_diam_px=35, min_solidity=0.55, max_aspect=2.0):
        """
        清理主体文字区外的孤立订书机孔散点(实心小暗点), 用周边底色填充。
        只动"高实心+近圆+真暗"的小点(订书机孔物理特征):
          d<=35px + 实心度>=0.55 + 长宽比<=2.0 + 均值灰<80;
        印章保护: 红章/黑章整章/残章碎块及其60px邻域全部跳过。
        文字行保护: 页首标题行/页脚行/表头行等整行落在分位内容bbox外的合法文字,
        其笔画暗核不是散点, 一律跳过(_text_line_bands), 否则会被填白成中空黑边字。
        numpy数组+同步灰度进出(写像素后增量更新灰度)；
        seal_zones：上游前置缓存的印章保护区(缺省自行计算)。
        返回 (结果数组, 更新后灰度, 清理点数)。需要 cv2; 无 cv2 原样返回。
        """
        try:
            import cv2
        except ImportError:
            return arr, gray, 0
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3

        mask = (gray < 80).astype(np.uint8)
        # 无pad的内容bbox: pad会把贴近主区的散点也当内容保护起来
        # (实测S161主区y_lo=477, pad后427, 顶部订书钉y≈460被包进内容区漏清)
        bbox = self._content_bbox(mask, pad_ratio=0.0)
        if bbox is None:
            return arr, gray, 0
        x_lo, y_lo, x_hi, y_hi = bbox

        # 印章保护区域(优先用上游前置缓存；自算时复用本环节已有的(gray<80)掩码)
        zones = (seal_zones if seal_zones is not None
                 else self._detect_seal_protect_zones(arr, gray, dark_mask=mask))

        # 文字行保护带: 整行落在分位bbox外的页首标题行/页脚行/表头行(合法文字),
        # 其笔画暗核绝不能当散点填白(详见 _text_line_bands 注释)。
        row_band, _bx = self._text_line_bands(mask)
        bx_lo, bx_hi = _bx

        def in_text_line(cx, cy):
            bid = row_band[cy]
            return bid >= 0 and bx_lo[bid] <= cx <= bx_hi[bid]

        # 候选散点: 内容bbox外 + 严格暗(<80均值)小块
        strict = (gray < 50).astype(np.uint8)
        n, labels, st, _ = cv2.connectedComponentsWithStats(strict, 8)

        # 钉排残迹行带预判: bbox外的候选块按y聚成行带(±40px), 同带>=5块且带整体
        # 距内容区>=60px(远离正文, 排除页眉行) → 该带是订书钉成排残迹, 带内块
        # 放宽尺寸(d<=60)与形状限制(钉帽/翻折丝印低实心)。印章保护zone仍优先拦截。
        _pre = []
        for i in range(1, n):
            a = st[i, 4]
            if a < 3 or a > 1500:
                continue
            l, t, w2, h2 = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
            cx, cy = l + w2 // 2, t + h2 // 2
            if x_lo <= cx <= x_hi and y_lo <= cy <= y_hi:
                continue
            # 文字行成员不参与行带聚类: 否则整行文字会被当成"订书钉排"(同带>=5块
            # +距内容区>=60px)而放宽尺寸/形状校验, 把字符笔画核成排填白。
            if in_text_line(cx, cy):
                continue
            _pre.append((i, cx, cy, max(w2, h2), a))
        staple_rows = set()   # 行带内块的组件索引
        if _pre:
            _pre.sort(key=lambda c: c[2])
            row = [_pre[0]]
            rows = []
            for c in _pre[1:]:
                if c[2] - row[-1][2] <= 40:
                    row.append(c)
                else:
                    rows.append(row)
                    row = [c]
            rows.append(row)
            for r in rows:
                if len(r) < 5:
                    continue
                ys_r = [c[2] for c in r]
                # 带整体在内容区上方/下方且间隔>=60px
                if max(ys_r) < y_lo - 60 or min(ys_r) > y_hi + 60:
                    for c in r:
                        if c[3] <= 60:
                            staple_rows.add(c[0])
        out = None      # 惰性拷贝：真正写入像素时才复制 arr/gray
        g_out = None
        removed = 0
        for i in range(1, n):
            a = st[i, 4]
            if a < 3 or a > 1200:
                continue
            l, t, w2, h2 = st[i, 0], st[i, 1], st[i, 2], st[i, 3]
            cx, cy = l + w2 // 2, t + h2 // 2
            # 必须在内容bbox外(空白区)
            if x_lo <= cx <= x_hi and y_lo <= cy <= y_hi:
                continue
            # 文字行保护: 页首标题行/页脚行/表头行的笔画暗核不是订书钉散点,
            # 填白后只剩抗锯齿边缘 → 成品出现中空只有黑边缘线的文字(实测
            # 007/019/056 首行、0160 页首标题行、0270 表头行均被掏空)。
            if in_text_line(cx, cy):
                continue
            d = max(w2, h2)
            in_staple_row = (i in staple_rows)
            if d > (60 if in_staple_row else max_diam_px):
                continue
            asp = d / max(min(w2, h2), 1)
            # 实心度: 严格暗像素占bbox比(订书机孔穿透点实心度高)
            sol = a / (w2 * h2) if w2 * h2 else 0
            # 可清理形态:
            # ① 实心近圆点(sol>=0.55, asp<=2): 订书机冲孔点/大头针孔;
            # ② 细长低实心痕(sol>=0.15, asp<=6): 订书钉金属丝压痕;
            # ③ 钉排行带成员(d<=60): 成串伴同于散点的钉帽/翻折残迹(低实心近方),
            #    行带判据(同带>=5块+远离内容区)已排除页眉/印章, zone仍兜底保护。
            is_dot = (asp <= max_aspect and sol >= min_solidity)
            is_staple = (asp <= 6.0 and sol >= 0.15)
            if not (is_dot or is_staple or in_staple_row):
                continue
            # 块均值灰度(真暗)：只在外接框局部窗内做布尔比较(块像素都在框内，
            # 与全图 labels==i 逐位一致)，免去逐候选全图布尔运算——实测 0152 页 7446 个
            # 组件下全图版耗时约 3.1s(整个散点环节的一半)，是单张最大热点。
            comp = (labels[t:t + h2, l:l + w2] == i)
            if float(gray[t:t + h2, l:l + w2][comp].mean()) >= 80:
                continue
            # 印章保护: 落在任何保护zone内则跳过
            protected = False
            for zx, zy, zr in zones:
                if (cx - zx) ** 2 + (cy - zy) ** 2 <= zr ** 2:
                    protected = True
                    break
            if protected:
                continue
            # 手写笔画群保护: 候选点100x100邻域内若存在>=8个其他暗块(笔画碎片群),
            # 说明该处是手写数字/文字/印章笔画区(笔画由大量碎块构成), 不是孤立
            # 订书机孔点 — 跳过。实测章旁手写"150/145"区碎块密度高(章+笔画群),
            # 而订书机孔散点彼此孤立(100px窗内仅1-3块)。仅对非钉排行带成员检查
            # (钉排本身是成排散点, 密度高是正常的)。
            if not in_staple_row:
                nb = sum(1 for pj, px, py, pd, pa in _pre
                         if pj != i and abs(px - cx) <= 50 and abs(py - cy) <= 50)
                if nb >= 8:
                    continue
            # 用周边(外扩至bbox外1.5倍)的亮像素中位数填底色
            s = max(d, 8)
            sx1, sy1 = max(0, cx - s), max(0, cy - s)
            sx2, sy2 = min(W, cx + s + 1), min(H, cy + s + 1)
            region_src = out if out is not None else arr
            region = region_src[sy1:sy2, sx1:sx2]
            region_gray = (region.mean(axis=2) if region.ndim == 3 else region)
            bright = region[region_gray > 100]
            if len(bright):
                fill_color = tuple(int(v) for v in np.median(
                    bright.reshape(-1, bright.shape[-1]) if region.ndim == 3 else bright,
                    axis=0))
            else:
                fill_color = (255, 255, 255) if rgb else 255
            # 填充整个块(用连通域精确形状)——注意填充窗与组件外接框坐标不同，
            # 须在填充窗坐标下重新取局部布尔(与原全图 comp 切片逐位一致)
            sub = (labels[sy1:sy2, sx1:sx2] == i)
            if out is None:
                out = arr.copy()
                g_out = gray.copy()
            if rgb:
                tgt = out[sy1:sy2, sx1:sx2]
                tgt[sub] = fill_color
            else:
                out[sy1:sy2, sx1:sx2][sub] = fill_color
            # 灰度增量同步: 与 _gray_u8 同一整除公式(逐位一致)
            g_out[sy1:sy2, sx1:sx2][sub] = (
                (fill_color[0] + fill_color[1] + fill_color[2]) // 3 if rgb else fill_color)
            removed += 1
        if removed == 0:
            return arr, gray, 0
        return out, g_out, removed

    def remove_color_halo(self, arr, gray, edge_ratio=0.18):
        """
        去除页面边缘的浅蓝色蕴(扫描仪彩色边缘偏色)，替换为页面本体色。
        判定条件(全部满足)：
          1. 偏蓝：B-R > 12 且 B > 185（浅蓝色蕴典型 RGB≈234,246,252，B-R≈16-20）；
          2. 偏亮：灰度 > 215（排除深色内容）；
          3. 无文字：51px 邻域内暗像素(<120)密度 < 2%（表格行底纹虽也是浅蓝，
             但行内含黑字，密度高——借此排除，不误伤表格底纹）；
          4. 靠边：位于页面四周 edge_ratio(18%) 带内（色蕴是边缘现象，
             中部同色是内容底色不动）。
        本体色取页面中部非蓝像素中位数。需要 cv2；无 cv2 原样返回。
        numpy数组+同步灰度进出，返回 (结果数组, 更新后灰度)。
        """
        try:
            import cv2
        except ImportError:
            return arr, gray

        H, W = arr.shape[:2]
        rgb = arr.ndim == 3
        if not rgb:
            return arr, gray  # 灰度图无彩色色蕴

        r_c = arr[:, :, 0].astype(np.int16)
        b_c = arr[:, :, 2].astype(np.int16)

        # 全蓝底图保护：蓝色亮像素占比>50%说明整页就是蓝底(如蓝图/彩色底文件)，
        # 不是边缘色蕴——此时"中部非蓝像素"是黑色文字，取它做本体色会把整页填黑。
        # 直接原样返回，不做色蕴处理。
        _blue_all = ((b_c - r_c) > 10) & (b_c > 180) & (gray > 190)
        if float(_blue_all.mean()) > 0.50:
            return arr, gray

        # 页面本体色(中部非蓝像素中位 RGB)
        cx0, cx1 = max(0, W // 2 - 300), min(W, W // 2 + 300)
        cy0, cy1 = max(0, H // 2 - 300), min(H, H // 2 + 300)
        creg = arr[cy0:cy1, cx0:cx1]
        cblue = (creg[:, :, 2].astype(np.int16) - creg[:, :, 0].astype(np.int16)) > 12
        body_px = creg[~cblue]
        if len(body_px) < 100:
            return arr, gray
        body = tuple(int(v) for v in np.median(body_px.reshape(-1, 3), axis=0))

        # 色蕴候选：蓝+亮+靠边；先做廉价判定，无候选直接返回(省去 51px 邻域模糊与连通域分析)
        halo = ((b_c - r_c) > 10) & (b_c > 180) & (gray > 200)
        ex, ey = int(W * edge_ratio), int(H * edge_ratio)
        edge_band = np.zeros((H, W), dtype=bool)
        edge_band[:ey, :] = True
        edge_band[H - ey:, :] = True
        edge_band[:, :ex] = True
        edge_band[:, W - ex:] = True
        halo = halo & edge_band
        if not halo.any():
            return arr, gray
        # 无文字：邻域暗像素密度(色蕴区可能含浅表格线, 阈值放宽到0.06;
        # 表格行底纹的文字密度通常>>0.10, 仍被排除)
        dark = (gray < 120).astype(np.float32)
        kd = cv2.blur(dark, (51, 51))
        halo = halo & (kd < 0.06)
        if not halo.any():
            return arr, gray

        # 连通域过滤：只处理与纸边相连的大块色蕴(排除边缘孤立蓝色小图形)
        halo_u8 = halo.astype(np.uint8)
        n, labels, stats, _ = cv2.connectedComponentsWithStats(halo_u8, 8)
        final = np.zeros((H, W), dtype=bool)
        for i in range(1, n):
            l, t, w2, h2, a = (stats[i, 0], stats[i, 1], stats[i, 2],
                               stats[i, 3], stats[i, 4])
            if a < 2000:
                continue
            # 与纸边相接(任一边界触碰色蕴带)
            if l <= 2 or t <= 2 or (l + w2) >= W - 2 or (t + h2) >= H - 2:
                final |= (labels == i)
        if not final.any():
            return arr, gray

        out = arr.copy()
        out[final] = body
        g_out = gray.copy()
        # 灰度增量同步: 与 _gray_u8 同一整除公式(逐位一致；本环节仅处理RGB图)
        g_out[final] = (body[0] + body[1] + body[2]) // 3
        return out, g_out

    @staticmethod
    def _box_blur(gray_f, win):
        """盒式均值滤波，语义对齐 cv2.blur 的 BORDER_REFLECT(=REFLECT_101)。
        有 cv2 时直接用其 C 实现(实测比前缀和版快约 10 倍)；无 cv2 回退二维前缀和。
        输入输出均为 float32。"""
        win = max(1, int(win))
        try:
            import cv2
            return cv2.blur(gray_f, (win, win))
        except Exception:
            pass
        r = win // 2
        p = np.pad(gray_f, r, mode='reflect')
        c = p.cumsum(axis=0).cumsum(axis=1)
        h, w = gray_f.shape
        d = 2 * r + 1
        out = c[2 * r:, 2 * r:].copy()
        out[1:, :] -= c[:-d, 2 * r:]
        out[:, 1:] -= c[2 * r:, :-d]
        out[1:, 1:] += c[:-d, :-d]
        return (out / float(d * d))[:h, :w].astype(np.float32)

    @staticmethod
    def _blur_pair(g, win):
        """一次模糊同时取局部标准差所需的 (均值, 平方均值)：把两个数组堆成双通道
        单次 cv2.blur(逐通道独立，与分别调用两次逐位一致，已探针验证)，省一次全图滤波。
        无 cv2 回退两次 _box_blur(前缀和实现仅支持二维，不可堆叠)。"""
        try:
            import cv2
            bl = cv2.blur(np.stack((g, g * g), axis=2), (win, win))
            return bl[:, :, 0], bl[:, :, 1]
        except Exception:
            return (CircleDetectionWorker._box_blur(g, win),
                    CircleDetectionWorker._box_blur(g * g, win))

    def remove_black_border(self, arr, gray, local_std15=None):
        """
        去除扫描黑边/阴影：检测靠近纸边、明显比页面底色暗的大块连通域
        (深色长条、灰色阴影三角等)，用页面底色填充。
        只处理“靠近边缘且足够大”的暗块，不动正文与远处内容。
        local_std15：前一环节(竖带清理)未改图时传入的 15×15 局部标准差(同一灰度，
        逐位一致)，直接复用省去全图滤波；缺省自行计算(双通道单次模糊)。
        连通域/纹理均有无 cv2 回退路径，打包环境缺 cv2 时不失效。
        输入/输出为管线传引用的 numpy 数组。返回 (结果数组, 同步灰度数组, 被填充像素数)。
        """
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3

        # 页面底色亮度(取偏亮的 75 分位，避免被暗块/文字拉低)
        page_bg = float(np.percentile(gray, 75))
        thr = page_bg - 60           # 比底色暗 60 以上视为边/阴影
        darkish = (gray < thr).astype(np.uint8)

        # 填充用底色(取接近底色亮度的像素中位 RGB)
        bgmask = gray >= (page_bg - 20)
        if rgb:
            bgpx = arr[bgmask]
            bg = tuple(int(v) for v in np.median(bgpx.reshape(-1, 3), axis=0)) if len(bgpx) else (255, 255, 255)
        else:
            bg = int(np.median(arr[bgmask])) if bgmask.any() else 255

        n_fg, labels, stats = self._connected_components_full(darkish)

        # 局部纹理(15x15 窗标准差)：二维码/条码等高频内容纹理高，真实黑边/阴影平滑(低)
        if local_std15 is not None:
            local_std = local_std15  # 前环节未改图，直接复用(逐位一致)
        else:
            gf = gray.astype(np.float32)
            gmean, gsq = self._blur_pair(gf, 15)
            local_std = np.sqrt(np.maximum(gsq - gmean * gmean, 0))

        min_area = int(0.0015 * W * H)  # 只处理大块，避免误删靠边文字(文字纹理高会被上面跳过)
        fill = np.zeros((H, W), dtype=bool)
        for i, (min_row, min_col, max_row, max_col, a) in enumerate(
                self._iter_components(n_fg, stats), 1):
            if a < min_area:
                continue
            l, t = min_col, min_row
            w = max_col - min_col + 1
            h = max_row - min_row + 1
            r = l + w; b = t + h
            # 靠近某条纸边(各自按该方向尺寸的10%)
            if not ((l < 0.1 * W) or (r > 0.9 * W) or (t < 0.1 * H) or (b > 0.9 * H)):
                continue
            # 面积过大(>12%)的不是边框，是大面积内容/底色
            if a > 0.12 * W * H:
                continue
            # 深度检查：至少有一条边，组件向内延伸不超过该方向30%
            # (否则是大面积浅灰底/内容区，不是边框/阴影)
            depth_ok = ((l < 0.1 * W and r < 0.3 * W) or
                        (r > 0.9 * W and (W - l) < 0.3 * W) or
                        (t < 0.1 * H and b < 0.3 * H) or
                        (b > 0.9 * H and (H - t) < 0.3 * H))
            if not depth_ok:
                continue
            # 填充率检查：真实扫描黑边/阴影是实心暗块(bbox 内填充率高，>25%)；
            # 表格网格线/单元格边框是稀疏线条(bbox 内填充率低，<20%，中间白底)。
            # 稀疏线条不是黑边，跳过，避免误删表格。
            bbox_area = w * h
            if bbox_area > 0 and (a / bbox_area) < 0.20:
                continue
            comp = labels == i
            # 纹理检查：横贯全幅(>75%宽)的顶部/底部条，或纵贯全幅(>75%高)的左/右条，
            # 原本不论纹理都去除(假设是整幅扫描黑条)。但表格的横/竖线也会横贯全幅
            # 且靠近顶/底边，会被误当黑条。区别在于：真实扫描黑边是实心暗条(bbox 内
            # 填充率高，>30%)；表格线条稀疏(bbox 内填充率低，<20%，中间是白底)。
            # 故 spans_full 块再加填充率检查：稀疏线条(表格)跳过，实心黑条才去除。
            spans_full = (w > 0.75 * W and (t < 0.1 * H or b > 0.9 * H)) or \
                         (h > 0.75 * H and (l < 0.1 * W or r > 0.9 * W))
            if spans_full:
                bbox_area = w * h
                fill_rate = (a / bbox_area) if bbox_area > 0 else 1.0
                if fill_rate < 0.20:
                    continue  # 稀疏线条=表格网格，不是实心黑边，跳过
            else:
                # 其余局部暗块：实心黑(均值<60)直接去；灰色阴影若>10%含高纹理(文字)则跳过
                comp_mean_gray = float(gray[comp].mean())
                if comp_mean_gray >= 60 and (local_std[comp] > 50).mean() > 0.10:
                    continue
            fill |= comp

        # ---- 额外：边缘细长扫描线(细灰线) —— 仅当其周边无文字时填充 ----
        for i, (min_row, min_col, max_row, max_col, a) in enumerate(
                self._iter_components(n_fg, stats), 1):
            if a < 40:
                continue
            l, t = min_col, min_row
            w = max_col - min_col + 1
            h = max_row - min_row + 1
            r = l + w; b = t + h
            # 靠近某条纸边(6%内)
            if not ((l < 0.06 * W) or (r > 0.94 * W) or (t < 0.06 * H) or (b > 0.94 * H)):
                continue
            longe = max(w, h); short = min(w, h)
            if longe < 40 or short > 25 or longe / max(short, 1) < 4:
                continue  # 不是细长线
            # 检查"内侧"(朝图像中心一侧)邻域是否有文字：暗像素占比>10%视为有文字
            gap = 15
            vertical = h > w
            if vertical:
                y0, y1 = max(0, t - gap), min(H, b + gap)
                band = darkish[y0:y1, max(0, l - gap):l] if r > 0.94 * W else darkish[y0:y1, r:min(W, r + gap)]
            else:
                x0, x1 = max(0, l - gap), min(W, r + gap)
                band = darkish[max(0, t - gap):t, x0:x1] if b > 0.94 * H else darkish[b:min(H, b + gap), x0:x1]
            if band.size == 0 or band.mean() > 0.10:
                continue  # 内侧有文字，不处理
            fill |= (labels == i)

        if not fill.any():
            return arr, gray, 0
        out_arr = arr.copy()
        # 墨迹保护：不覆盖非常暗的像素(灰度<底色-80)，这些是手写/印章/文字笔画
        bg_gray_val = float(np.mean(bg)) if rgb else float(bg)
        ink_mask = gray < (bg_gray_val - 80)
        fill = fill & ~ink_mask
        if not fill.any():
            return arr, gray, 0
        out_arr[fill] = bg
        # 同步更新灰度(与 _gray_u8 同一整除公式，逐位一致；注意与墨迹保护用的
        # 浮点均值 bg_gray_val 不同，此处必须与实际写入像素的灰度一致)
        g_out = gray.copy()
        g_out[fill] = (bg[0] + bg[1] + bg[2]) // 3 if rgb else bg
        return out_arr, g_out, int(fill.sum())

    def cover_edge_with_bg(self, arr, gray, margin_px):
        """
        将图像四周边缘 margin_px 像素宽度的区域用底色覆盖。
        底色通过采样四角区域的中位数获得。
        边缘区域内含手写/文字(高纹理)的段落跳过，只覆盖纯色边框区域。
        输入/输出为管线传引用的 numpy 数组。返回 (结果数组, 同步灰度数组)。
        """
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3

        # 采样四角区域获取底色
        corner = max(10, margin_px // 2)
        corners = [
            arr[0:corner, 0:corner],
            arr[0:corner, W - corner:W],
            arr[H - corner:H, 0:corner],
            arr[H - corner:H, W - corner:W],
        ]
        samples = np.concatenate([c.reshape(-1, c.shape[-1]) if rgb else c.reshape(-1) for c in corners])
        if rgb:
            bright = samples[samples.mean(axis=1) > 80]
            bg_color = tuple(int(v) for v in np.median(bright, axis=0)) if len(bright) else (255, 255, 255)
        else:
            bright = samples[samples > 80]
            bg_color = int(np.median(bright)) if bright.size else 255

        out = None
        g_out = None
        # 写入像素的实际灰度(与 _gray_u8 同一整除公式；区别于 is_ink 用的浮点均值)
        bg_gray_fill = ((bg_color[0] + bg_color[1] + bg_color[2]) // 3) if rgb else bg_color

        # 局部纹理：边缘区域内有手写/文字的段落(高纹理)不覆盖(双通道单次模糊)
        win = max(5, margin_px // 3)
        gmean, gsq = self._blur_pair(gray, win)
        local_std = np.sqrt(np.maximum(gsq - gmean * gmean, 0))
        has_texture = local_std > 30  # 高纹理=有内容

        # 只覆盖低纹理(纯色边框)区域，跳过高纹理(手写/文字)和深色墨迹(手写笔画)
        bg_gray_val = float(np.mean(bg_color)) if rgb else float(bg_color)

        def safe_cover(y0, y1, x0, x1):
            nonlocal out, g_out
            if y0 >= y1 or x0 >= x1:
                return
            region_texture = has_texture[y0:y1, x0:x1]
            region_gray = gray[y0:y1, x0:x1]
            # 只覆盖：低纹理(非边框)且非深色墨迹的像素
            # 深色墨迹(gray < bg-60)是手写/印章，不覆盖
            is_ink = region_gray < (bg_gray_val - 60)
            cover_mask = ~region_texture & ~is_ink
            if not cover_mask.any():
                return
            if out is None:
                out = arr.copy()
            sub = out[y0:y1, x0:x1]
            sub[cover_mask] = bg_color
            out[y0:y1, x0:x1] = sub
            if g_out is None:
                g_out = gray.copy()
            g_out[y0:y1, x0:x1][cover_mask] = bg_gray_fill

        # 上边
        safe_cover(0, margin_px, 0, W)
        # 下边
        safe_cover(H - margin_px, H, 0, W)
        # 左边
        safe_cover(margin_px, H - margin_px, 0, margin_px)
        # 右边
        safe_cover(margin_px, H - margin_px, W - margin_px, W)

        return (out if out is not None else arr,
                g_out if g_out is not None else gray)

    def remove_hole_shadow_residue(self, arr, gray, seal_zones=None):
        """
        去除装订孔阴影残留：孔洞填充后，孔位周围常残留浅灰色环状/弧状阴影
        (冲头压痕/扫描泛光)，灰度仅比页面底色暗 20~100(典型 130~220)，远达
        不到孔检测阈值(<50)，会漏过前面所有环节，在成品图上留下近似圆形/半圆
        形的痕迹。本方法在四条边距带(与装订孔检测同区域)内找「浅灰 + 近圆形 +
        四周无文字 + 同列成组」的连通块，用局部底色填充。返回 (结果Image, 清除数)。
        安全约束(缺一不可)：
          1. 仅限边距带内，且中心距纸边<=160px(装订孔物理上贴边打，实测76-107px)，
             排除边距带深处的文字/表格痕迹；
          2. 几何：直径 10~0.5*最大直径，宽高比<=2.5(排除笔画/线条)；
          3. 浅淡：连通块均值灰度>=110，过暗视为墨迹/污渍不动；彩色成分高(色散>60)
             视为红章/彩笔痕迹不动(孔影为无彩灰色)；
          4. 孤立：环带内墨迹样连通域(面积>=80且均值<85)<3 个——孔自身阴影
             (均值>=85)与扫描碎屑(<80)不计，避免真孔被旁边碎屑误杀；
          5. 成组：同边带内 2-8 个孔样成员(直径>=24)同列/同排对齐，且列向松散度/
             纵向跨度符合装订孔几何(拦截横排手写数字与聚团斑点)；且去除任一成员后
             跨度仍须达标(拦截靠单个远端碎块撑跨度的假组，如顶部手写+底部页脚碎块)；
          6. 填充前复查填充圆内无墨迹样连通域(面积>=80或延伸出填充框)；
          7. 暗核拦截：连通块外接框外扩8px窗内暗像素(灰度<90)总量>=25即放弃——手写笔画的
             外围浅灰晕圈围住/贴着暗色笔画核, 真孔影为纯渐变灰无暗核(实测拦截0152章旁手写)；
          8. 印章邻域保护：落在印章保护区域(红章/黑章/残章, 含邻域外延)内的候选整体跳过。
        numpy数组+同步灰度进出；seal_zones 由上游前置缓存传入(缺省自行计算)。
        返回 (结果数组, 更新后灰度, 清除数)。
        """
        try:
            import cv2
        except ImportError:
            return arr, gray, 0
        H, W = arr.shape[:2]
        rgb = arr.ndim == 3
        page_bg = float(np.percentile(gray, 75))
        if page_bg < 150:
            return arr, gray, 0  # 整页暗底扫描件不适用阴影残留概念，不处理

        thr = page_bg - 15
        # 浅灰阴影掩码(排除<90的深色墨迹)；硬掩码含墨迹，用于孤立性检查
        soft = ((gray < thr) & (gray >= 90)).astype(np.uint8)
        hard = (gray < thr).astype(np.uint8)

        mp = self.margin_pixels
        bands = []
        if 0 < mp < W // 2:
            bands.append((hard[:, :mp], soft[:, :mp], 0, 0, 'v', 'L'))
            bands.append((hard[:, W - mp:], soft[:, W - mp:], W - mp, 0, 'v', 'R'))
        if 0 < mp < H // 2:
            bands.append((hard[:mp, :], soft[:mp, :], 0, 0, 'h', 'T'))
            bands.append((hard[H - mp:, :], soft[H - mp:, :], 0, H - mp, 'h', 'B'))

        max_diam = self.max_diameter_pixels * 0.5
        tol = max(self.max_diameter_pixels // 4, 1)
        # 印章保护区域：手写数字/批注常伴随印章出现(实测0152/0219误清案例均在章旁)，
        # 落在红章/黑章/残章保护区域内的候选整体跳过，与散点清理同策略。
        if seal_zones is None:
            seal_zones = self._detect_seal_protect_zones(arr, gray)

        def edge_dist(cx, cy, edge):
            if edge == 'L':
                return cx
            if edge == 'R':
                return W - 1 - cx
            if edge == 'T':
                return cy
            return H - 1 - cy

        def ink_isolated(cx, cy, r):
            # 环带(1.3r~2.2r)内墨迹样连通域计数：面积>=80 且均值<85 才算笔画/印章。
            # 碎屑(<80)与孔自身阴影(浅灰均值>=85)不计，避免真孔被旁边污点误杀。
            r = max(int(r), 4)
            inner = int(r * 1.3)
            outer = int(r * 2.2)
            x0, x1 = max(0, cx - outer), min(W, cx + outer + 1)
            y0, y1 = max(0, cy - outer), min(H, cy + outer + 1)
            sub = hard[y0:y1, x0:x1]
            if sub.size == 0:
                return True
            hs, ws = sub.shape
            yy2, xx2 = np.mgrid[0:hs, 0:ws]
            dist2 = (xx2 - (cx - x0)) ** 2 + (yy2 - (cy - y0)) ** 2
            ring = (dist2 >= inner * inner) & (dist2 <= outer * outer)
            ring_fg = (ring & (sub > 0)).astype(np.uint8)
            n_cc2, lab2, st2, _ = cv2.connectedComponentsWithStats(ring_fg, 8)
            sibs = 0
            for j in range(1, n_cc2):
                if int(st2[j, cv2.CC_STAT_AREA]) < 80:
                    continue
                l2, t2 = int(st2[j, 0]), int(st2[j, 1])
                w2, h2 = int(st2[j, 2]), int(st2[j, 3])
                cm2 = lab2[t2:t2 + h2, l2:l2 + w2] == j
                mg2 = float(gray[y0 + t2:y0 + t2 + h2, x0 + l2:x0 + l2 + w2][cm2].mean())
                if mg2 < 85:
                    sibs += 1
                    if sibs >= 3:
                        return False
            return True

        candidates = []  # (cx, cy, 填充半径)
        for hard_b, soft_b, off_x, off_y, axis, edge in bands:
            if soft_b.size == 0:
                continue
            n_cc, labels, stats, _ = cv2.connectedComponentsWithStats(soft_b, 8)
            band_cands = []
            for i in range(1, n_cc):
                l, t, w, h, a = (int(stats[i, 0]), int(stats[i, 1]), int(stats[i, 2]),
                                 int(stats[i, 3]), int(stats[i, 4]))
                diam = max(w, h)
                short = min(w, h)
                if a < 30 or diam < 10 or diam > max_diam:
                    continue
                if diam / float(max(short, 1)) > 2.5:  # 细长=笔画/线条，不是环影
                    continue
                comp_mask = labels[t:t + h, l:l + w] == i
                # 用全图灰度取连通块像素(掩码本身只有0/1)
                comp_gray = gray[t + off_y:t + off_y + h,
                                l + off_x:l + off_x + w][comp_mask]
                if comp_gray.size == 0 or float(comp_gray.mean()) < 110:
                    continue  # 偏暗=疑似墨迹/污渍，不动
                # 色散检查：红章/彩笔像素在灰度上与浅灰痕迹重叠(130-150)，但
                # RGB通道差明显(红章实测109-137)，孔影/灰字痕迹<=30；色散>60丢弃。
                if rgb:
                    comp_rgb = arr[t + off_y:t + off_y + h,
                                   l + off_x:l + off_x + w][comp_mask]
                    chroma = (comp_rgb.max(axis=1).astype(np.int32)
                              - comp_rgb.min(axis=1).astype(np.int32)).mean()
                    if chroma > 60:
                        continue  # 彩色=印章/彩笔痕迹，不是孔影
                cx = l + w // 2 + off_x
                cy = t + h // 2 + off_y
                if not ink_isolated(cx, cy, diam // 2):
                    continue
                # 暗核拦截：手写笔画晕圈(灰度90~page_bg-15的浅灰外围)围住/贴着暗色笔画核，
                # 检查窗(连通块外接框外扩8px)内暗像素(<90)总量>=25即手写/污渍而非孔影。
                # 实测0152章旁手写150/带横线145的晕圈块尺寸/均值灰度/色散/成组全过关；
                # 笔画核有时不与晕圈连通(在框外相邻)故窗需外扩；用总量而非单块面积，
                # 拦截相邻的细笔画核。真孔已填白、孔影纯渐变无暗核；边带零散压缩噪声总量低不拦。
                bx0 = max(0, l + off_x - 8)
                by0 = max(0, t + off_y - 8)
                bx1 = min(W, l + off_x + w + 8)
                by1 = min(H, t + off_y + h + 8)
                if int((gray[by0:by1, bx0:bx1] < 90).sum()) >= 25:
                    continue
                # 印章邻域保护：候选中心落入印章保护区域则跳过(章旁手写/批注兜底)。
                # 半径额外外延120：章旁手写数字常距章心超出60px(实测0152/0219距章可达~150)。
                _prot = False
                for zx, zy, zr in seal_zones:
                    if (cx - zx) ** 2 + (cy - zy) ** 2 <= (zr + 120) ** 2:
                        _prot = True
                        break
                if _prot:
                    continue
                band_cands.append((cx, cy, w, h))
            # 贴边筛选：装订孔物理上贴着纸边打(实测孔心距边 76-107px)，只保留距纸边
            # <=160px 的候选——边距带深处的文字列表/表格/页眉痕迹(距边>=290px)全部排除。
            band_cands = [c for c in band_cands if edge_dist(c[0], c[1], edge) <= 160]
            # 同列/同排成组：装订孔必为2-6个一组；孤立候选(可能是铅笔点/碎屑)丢弃。
            # 同组尺寸不要求一致——同一页的孔影可能部分已被上轮处理削小。
            cols = []
            for c in sorted(band_cands, key=lambda c: c[0] if axis == 'v' else c[1]):
                key = c[0] if axis == 'v' else c[1]
                for col in cols:
                    k0 = col[0][0] if axis == 'v' else col[0][1]
                    if abs(k0 - key) <= tol:
                        col.append(c)
                        break
                else:
                    cols.append([c])
            for col in cols:
                # 组内至少2个孔样成员(直径>=24)才算装订孔组，排除纯碎屑凑组。
                big = [c for c in col if max(c[2], c[3]) >= 24]
                if len(big) < 2:
                    continue
                # 装订孔列的三重校验，拦截手写数字/批注(浅灰笔迹均值130-160能闯过
                # 前面所有单项检查，只能靠组级几何特征识别)：
                # ① 成员数≤8：文字行/批注行碎块多，真孔一列 2-6 个；
                # ② 列向松散度：同列孔心横坐标接近，但扫描偏斜会让孔位随列长
                #    线性漂移(实测≤3.4°)，容差随跨度放宽；而横排手写数字(如"102")
                #    横坐标差≈68 远超孔列容差，被拦截；
                # ③ 纵向跨度：装订孔跨大半个页面(实测跨度≥900)，孔距远大于孔径；
                #    手写数字/斑点聚团(跨度<250)被拦截。
                if len(col) > 8:
                    continue
                med = int(np.median([max(c[2], c[3]) for c in big]))
                keys = [c[0] if axis == 'v' else c[1] for c in big]
                spans = [c[1] if axis == 'v' else c[0] for c in big]
                span = max(spans) - min(spans)
                if max(keys) - min(keys) > max(48, int(med * 0.9)) + span * 0.08:
                    continue
                if span < max(250, med * 4):
                    continue
                # ④ 孤点撑跨度检测：去掉组内任一成员后剩余跨度仍须达标。手写碎块+
                #    远端单个页脚碎块可凑出大跨度假组，但去掉孤点后跨度立即崩塌；
                #    真孔列分布均匀，去任一成员跨度仅缩一个孔距，不会崩塌。
                if len(big) < 3:
                    continue
                lone = False
                for k in range(len(big)):
                    rest = [big[j][1] if axis == 'v' else big[j][0]
                            for j in range(len(big)) if j != k]
                    if max(rest) - min(rest) < max(250, med * 4):
                        lone = True
                        break
                if lone:
                    continue
                # 填充半径取组内(孔样成员)直径中位数——同页孔由同一冲头打出，
                # 尺寸一致，中位数可挽救只检出残弧(外接框偏小)的成员。
                rf = med // 2 + max(10, med // 5)
                candidates.extend((c[0], c[1], rf) for c in col)

        if not candidates:
            return arr, gray, 0

        # 去重(角落区域可能同时落在横竖两条边带内)
        targets = []
        for cx, cy, rf in candidates:
            dup = False
            for tx, ty, tr in targets:
                if (cx - tx) ** 2 + (cy - ty) ** 2 <= max(rf, tr) ** 2:
                    dup = True
                    break
            if not dup:
                targets.append((cx, cy, rf))

        out = None      # 惰性拷贝：真正写入像素时才复制 arr/gray
        g_out = None
        filled = 0
        for cx, cy, rf in targets:
            # 圆形填充区：以组内中位直径为基准外扩一圈，把渐变尾巴一并抹净
            x0, x1 = max(0, cx - rf), min(W, cx + rf + 1)
            y0, y1 = max(0, cy - rf), min(H, cy + rf + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            yy, xx = np.mgrid[y0:y1, x0:x1]
            ell = ((xx - cx) ** 2 + (yy - cy) ** 2) <= rf * rf
            # 墨迹保护：填充框内存在与填充圆相交的墨迹样连通域(面积>=80，或延伸出
            # 填充框=疑似框外笔画的一部分)则放弃(防误擦文字/手写)；框内居中小碎屑随影填充。
            crop = gray[y0:y1, x0:x1]
            cw, ch = x1 - x0, y1 - y0
            n_cc3, lab3, st3, _ = cv2.connectedComponentsWithStats(
                (crop < 85).astype(np.uint8), 8)
            blocked = False
            for j in range(1, n_cc3):
                l3, t3 = int(st3[j, 0]), int(st3[j, 1])
                w3, h3 = int(st3[j, 2]), int(st3[j, 3])
                a3 = int(st3[j, cv2.CC_STAT_AREA])
                if a3 < 80 and l3 > 0 and t3 > 0 and l3 + w3 < cw and t3 + h3 < ch:
                    continue  # 完全位于框内的小碎屑，不算墨迹，随阴影一起填掉
                cm3 = lab3[t3:t3 + h3, l3:l3 + w3] == j
                if (cm3 & ell[t3:t3 + h3, l3:l3 + w3]).any():
                    blocked = True
                    break
            if blocked:
                continue
            # 局部底色：填充圆外圈亮像素(>=thr)中位数，白底填白、彩底填对应底色
            pad = max(6, rf // 2)
            sx0, sx1 = max(0, x0 - pad), min(W, x1 + pad)
            sy0, sy1 = max(0, y0 - pad), min(H, y1 + pad)
            s_gray = gray[sy0:sy1, sx0:sx1]
            bright = s_gray >= thr
            if rgb:
                s_arr = arr[sy0:sy1, sx0:sx1]
                color = (tuple(int(v) for v in np.median(s_arr[bright].reshape(-1, 3), axis=0))
                         if bright.any() else (255, 255, 255))
            else:
                color = int(np.median(s_gray[bright])) if bright.any() else 255
            if out is None:
                out = arr.copy()
                g_out = gray.copy()
            sub = out[y0:y1, x0:x1]
            sub[ell] = color
            out[y0:y1, x0:x1] = sub
            # 灰度增量同步: 与 _gray_u8 同一整除公式(逐位一致)
            g_out[y0:y1, x0:x1][ell] = (
                (color[0] + color[1] + color[2]) // 3 if rgb else color)
            filled += 1
        if filled == 0:
            return arr, gray, 0
        return out, g_out, filled


class ZoomableImageView(QGraphicsView):
    """支持缩放和边距红框叠加的图像预览视图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._pixmap_item = None
        self._margin_rect_item = None
        self._scale_factor = 1.0
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setStyleSheet("background-color: #1a1a2e; border: 1px solid #30363D; border-radius: 3px;")
        self._img_width = 0
        self._img_height = 0

    def set_image(self, pil_image, margin_mm=0, dpi=300):
        """设置显示的PIL图像，可选绘制边距红框"""
        if pil_image is None:
            return
        rgb = pil_image.convert('RGB')
        data = rgb.tobytes('raw', 'RGB')
        qimg = QImage(data, rgb.width, rgb.height, rgb.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self._img_width = rgb.width
        self._img_height = rgb.height

        self._scene.clear()
        self._scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self._pixmap_item = self._scene.addPixmap(pixmap)

        if margin_mm > 0:
            px = int(margin_mm * dpi / 25.4)
            pen = QPen(QColor(255, 0, 0), max(2, int(max(rgb.width, rgb.height) / 500)))
            self._margin_rect_item = self._scene.addRect(
                QRectF(px, px, max(0, rgb.width - 2 * px), max(0, rgb.height - 2 * px)), pen)
        else:
            self._margin_rect_item = None

        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        self._scale_factor = 1.0

    def clear_image(self):
        self._scene.clear()
        self._pixmap_item = None
        self._margin_rect_item = None
        self._img_width = 0
        self._img_height = 0

    def zoom_in(self):
        self._scale_factor *= 1.25
        self.scale(1.25, 1.25)

    def zoom_out(self):
        self._scale_factor /= 1.25
        self.scale(1 / 1.25, 1 / 1.25)

    def fit_to_view(self):
        if self._pixmap_item:
            self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
            self._scale_factor = 1.0

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()


class PreviewPanel(QWidget):
    """单个预览面板：包含导航、缩放、图像视图和路径显示"""
    nav_changed = Signal()  # 当用户切换页面时发出

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # 标题栏
        self.header = QLabel(title)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 14px; font-weight: bold; padding: 2px;")
        layout.addWidget(self.header)

        # 导航栏
        nav = QHBoxLayout()
        self.prev_btn = QPushButton("◀ 上一页")
        self.prev_btn.setObjectName("BrowseBtn")
        self.prev_btn.setFixedWidth(90)
        self.next_btn = QPushButton("下一页 ▶")
        self.next_btn.setObjectName("BrowseBtn")
        self.next_btn.setFixedWidth(90)
        self.page_label = QLabel("0 / 0")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("color: #E0E0E0; font-size: 12px;")
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.page_label, 1)
        nav.addWidget(self.next_btn)
        layout.addLayout(nav)

        # 图像视图
        self.image_view = ZoomableImageView()
        self.image_view.setMinimumHeight(300)
        layout.addWidget(self.image_view, 1)

        # 缩放按钮栏
        zoom_bar = QHBoxLayout()
        self.zoom_in_btn = QPushButton("放大 +")
        self.zoom_in_btn.setObjectName("BrowseBtn")
        self.zoom_in_btn.setFixedWidth(70)
        self.zoom_out_btn = QPushButton("缩小 −")
        self.zoom_out_btn.setObjectName("BrowseBtn")
        self.zoom_out_btn.setFixedWidth(70)
        self.fit_btn = QPushButton("适应窗口")
        self.fit_btn.setObjectName("BrowseBtn")
        self.fit_btn.setFixedWidth(80)
        zoom_bar.addWidget(self.zoom_in_btn)
        zoom_bar.addWidget(self.zoom_out_btn)
        zoom_bar.addWidget(self.fit_btn)
        zoom_bar.addStretch()
        layout.addLayout(zoom_bar)

        # 文件路径
        self.path_label = QLabel("")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("color: #8B949E; font-size: 14px; padding: 3px;")
        layout.addWidget(self.path_label)

        # 连接缩放按钮
        self.zoom_in_btn.clicked.connect(self.image_view.zoom_in)
        self.zoom_out_btn.clicked.connect(self.image_view.zoom_out)
        self.fit_btn.clicked.connect(self.image_view.fit_to_view)

        self._files = []
        self._current_index = -1

    def set_files(self, files):
        self._files = list(files)
        self._current_index = 0 if files else -1
        self._update_nav_state()

    def get_current_index(self):
        return self._current_index

    def set_current_index(self, idx):
        if 0 <= idx < len(self._files):
            self._current_index = idx
            self._update_nav_state()
            self.nav_changed.emit()

    def current_file(self):
        if 0 <= self._current_index < len(self._files):
            return self._files[self._current_index]
        return None

    def file_count(self):
        return len(self._files)

    def _update_nav_state(self):
        total = len(self._files)
        self.prev_btn.setEnabled(self._current_index > 0)
        self.next_btn.setEnabled(self._current_index < total - 1)
        if total > 0:
            self.page_label.setText(f"{self._current_index + 1} / {total}")
        else:
            self.page_label.setText("0 / 0")

    def show_pil_image(self, pil_image, margin_mm=0, dpi=300):
        self.image_view.set_image(pil_image, margin_mm, dpi)
        f = self.current_file()
        self.path_label.setText(f if f else "")

    def clear(self):
        self.image_view.clear_image()
        self.path_label.setText("")
        self.page_label.setText("0 / 0")
        self._files = []
        self._current_index = -1


class BlackCircleRemoverPage(QWidget):
    """黑色圆圈移除主页面"""

    DARK_QSS = """
    QWidget { background-color: #0B0F19; color: #E0E0E0; font-family: 'Microsoft YaHei', Arial; }
    QGroupBox {
        border: 1px solid #30363D; border-radius: 5px; margin-top: 15px; padding: 15px;
        font-weight: bold; color: #00F0FF;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
    QLineEdit, QSpinBox, QComboBox {
        background-color: #0D1117; border: 1px solid #30363D; border-radius: 3px;
        padding: 5px; color: #E0E0E0;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #00F0FF; }
    QSpinBox::up-button, QSpinBox::down-button { background-color: #21262D; border: none; width: 18px; }
    QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; border-left: 1px solid #30363D; }
    QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right; border-left: 1px solid #30363D; border-top: 1px solid #30363D; }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #30363D; }
    QSpinBox::up-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #E0E0E0; width: 0px; height: 0px; }
    QSpinBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #E0E0E0; width: 0px; height: 0px; }
    QPushButton#ActionBtn { background-color: #238636; color: white; border: none; padding: 8px 16px; border-radius: 3px; font-weight: bold; }
    QPushButton#ActionBtn:hover { background-color: #2EA043; }
    QPushButton#ActionBtn:disabled { background-color: #1a3a25; color: #5a7a65; }
    QPushButton#BrowseBtn { background-color: #30363D; color: white; border: none; padding: 5px 10px; border-radius: 3px; }
    QPushButton#BrowseBtn:hover { background-color: #3C434D; }
    QTextEdit { background-color: #0D1117; border: 1px solid #30363D; border-radius: 3px; color: #FFFFFF; font-size: 13px; }
    QProgressBar { background-color: #0D1117; border: 1px solid #30363D; border-radius: 3px; text-align: center; color: #FFFFFF; font-weight: bold; }
    QProgressBar::chunk { background-color: #2EA043; border-radius: 2px; }
    QCheckBox { color: #E0E0E0; }
    QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #30363D; border-radius: 3px; background-color: #0D1117; }
    QCheckBox::indicator:checked { background-color: #00F0FF; border: 1px solid #00F0FF; }
    """

    LIGHT_QSS = """
    QWidget { background-color: #ecf0f1; color: #2c3e50; font-family: 'Microsoft YaHei', Arial; font-size: 14px; }
    QGroupBox {
        border: 2px solid #aed6f1; border-radius: 8px; margin-top: 15px; padding: 15px;
        font-weight: bold; color: #1a5276; background-color: #ffffff;
    }
    QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
    QLineEdit, QSpinBox, QComboBox {
        background-color: white; border: 1px solid #bdc3c7; border-radius: 4px;
        padding: 5px; color: #2c3e50;
    }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #3498db; }
    QSpinBox::up-button, QSpinBox::down-button { background-color: #d6eaf8; border: none; width: 18px; }
    QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; border-left: 1px solid #bdc3c7; }
    QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right; border-left: 1px solid #bdc3c7; border-top: 1px solid #bdc3c7; }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #aed6f1; }
    QSpinBox::up-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #2c3e50; width: 0px; height: 0px; }
    QSpinBox::down-arrow { image: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #2c3e50; width: 0px; height: 0px; }
    QPushButton#ActionBtn { background-color: #27ae60; color: white; border: none; padding: 8px 16px; border-radius: 5px; font-weight: bold; }
    QPushButton#ActionBtn:hover { background-color: #2ecc71; }
    QPushButton#ActionBtn:disabled { background-color: #bdc3c7; }
    QPushButton#BrowseBtn { background-color: #2980b9; color: white; border: none; padding: 5px 10px; border-radius: 4px; }
    QPushButton#BrowseBtn:hover { background-color: #3498db; }
    QTextEdit { background-color: white; border: 1px solid #bdc3c7; border-radius: 4px; color: #2c3e50; font-size: 13px; }
    QProgressBar { background-color: white; border: 1px solid #bdc3c7; border-radius: 4px; text-align: center; color: #2c3e50; font-weight: bold; }
    QProgressBar::chunk { background-color: #27ae60; border-radius: 3px; }
    QCheckBox { color: #2c3e50; }
    QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #bdc3c7; border-radius: 3px; background-color: white; }
    QCheckBox::indicator:checked { background-color: #3498db; border: 1px solid #3498db; }
    """

    _DARK_COLORS = {
        'accent': '#00F0FF', 'text': '#E0E0E0', 'secondary': '#8B949E',
        'bg_dark': '#0D1117', 'border': '#30363D', 'view_bg': '#1a1a2e',
    }
    _LIGHT_COLORS = {
        'accent': '#1565C0', 'text': '#1c2833', 'secondary': '#5d6d7e',
        'bg_dark': '#ffffff', 'border': '#bdc3c7', 'view_bg': '#d5dbdb',
    }

    def __init__(self):
        super().__init__()
        self._current_theme = 'light'
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 10, 15, 12)
        self.layout.setSpacing(8)

        # === 左侧面板：设置区 ===
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # 标题
        self.lbl_title = QLabel("图像质检工具")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet(
            "font-size: 26px; font-weight: bold;"
            "font-family: 'SimHei','黑体','Microsoft YaHei'; padding: 2px 0 6px 0;")
        left_layout.addWidget(self.lbl_title)

        # 设置组
        group = QGroupBox("处理设置")
        form = QFormLayout()

        # 输入目录选择
        self.input_dir = QLineEdit()
        btn_browse_input = QPushButton("选择文件夹")
        btn_browse_input.setObjectName("BrowseBtn")
        btn_browse_input.clicked.connect(self.browse_input_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.input_dir)
        h1.addWidget(btn_browse_input)
        form.addRow("输入目录:", h1)

        # 输出目录选择
        self.output_dir = QLineEdit()
        btn_browse_output = QPushButton("选择文件夹")
        btn_browse_output.setObjectName("BrowseBtn")
        btn_browse_output.clicked.connect(self.browse_output_dir)
        h2 = QHBoxLayout()
        h2.addWidget(self.output_dir)
        h2.addWidget(btn_browse_output)
        form.addRow("输出目录:", h2)

        # 自动设置输出目录选项
        self.auto_output_dir = QCheckBox("自动在源目录下创建'图像处理结果'目录")
        self.auto_output_dir.setChecked(True)
        self.auto_output_dir.stateChanged.connect(self.on_auto_output_changed)
        form.addRow("", self.auto_output_dir)

        # 最大直径设置（毫米）
        self.max_diameter_spin = QSpinBox()
        self.max_diameter_spin.setRange(5, 50)
        self.max_diameter_spin.setValue(25)  # 2.5cm = 25mm
        self.max_diameter_spin.setSuffix(" mm")
        form.addRow("圆圈最大直径:", self.max_diameter_spin)

        # 纠偏(去倾斜)选项
        self.deskew_check = QCheckBox("纠偏（将内容旋转到水平，纯旋转不变形）")
        self.deskew_check.setChecked(True)
        form.addRow("纠偏:", self.deskew_check)

        # 去黑边选项(默认选中)
        self.border_check = QCheckBox("去黑边（去除扫描产生的边缘黑条/阴影，保留正文）")
        self.border_check.setChecked(True)
        form.addRow("去黑边:", self.border_check)

        # 去孔影残留选项(默认选中)
        self.shadow_check = QCheckBox("去孔影（清除装订孔周围残留的浅灰色圆形/半圆形阴影痕迹）")
        self.shadow_check.setChecked(True)
        self.shadow_check.setToolTip("装订孔去除后，孔位周围常残留浅灰色环状/弧状阴影(冲头压痕/扫描泛光)；"
                                     "启用后会在边距区内识别并用底色抹除这类痕迹，不影响正文。")
        form.addRow("去孔影:", self.shadow_check)

        # DPI 设置
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 1200)
        self.dpi_spin.setValue(300)
        self.dpi_spin.setSuffix(" DPI")
        self.dpi_spin.setToolTip("用于将毫米转换为像素的DPI假设值")
        form.addRow("图像DPI:", self.dpi_spin)

        # 边缘覆盖边距设置
        self.edge_margin_spin = QDoubleSpinBox()
        self.edge_margin_spin.setRange(0.0, 50.0)
        self.edge_margin_spin.setValue(2.0)
        self.edge_margin_spin.setSingleStep(0.5)
        self.edge_margin_spin.setSuffix(" mm")
        self.edge_margin_spin.setToolTip("距离文件边缘的边距宽度，该区域内的内容将被底色覆盖")
        form.addRow("边缘覆盖边距:", self.edge_margin_spin)

        # 边缘覆盖选项
        self.edge_cover_check = QCheckBox("边缘底色覆盖（将四周边缘区域用底色覆盖）")
        self.edge_cover_check.setChecked(False)
        self.edge_cover_check.setToolTip("启用后，处理时会将文件四周边缘设定边距宽度的区域用底色覆盖")
        # 勾选/改值时实时刷新预览红框
        self.edge_cover_check.stateChanged.connect(self._refresh_edge_preview)
        self.edge_margin_spin.valueChanged.connect(self._refresh_edge_preview)
        form.addRow("边缘覆盖:", self.edge_cover_check)

        # 自动加深文字选项(默认选中)
        self.darken_check = QCheckBox("自动加深（检测偏浅文字并加深，提升清晰度）")
        self.darken_check.setChecked(True)
        self.darken_check.setToolTip("启用后，处理完成时检查文字颜色深度；若文字偏浅则自动加深到合适黑度，背景不变。已经足够深的文字不处理。")
        form.addRow("自动加深:", self.darken_check)

        # 主题选择
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("浅色界面")
        self.theme_combo.addItem("褐色界面")
        self.theme_combo.currentIndexChanged.connect(self._switch_theme)
        form.addRow("界面风格:", self.theme_combo)

        # 线程数设置
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 8)
        self.thread_spin.setValue(4)
        self.thread_spin.setSuffix(" 线程")
        form.addRow("并行线程数:", self.thread_spin)

        group.setLayout(form)
        left_layout.addWidget(group)

        # 说明文本
        self.info_label = QLabel(
            "功能说明：\n"
            "• 递归扫描指定目录及子目录下的所有JPG文件\n"
            "• 智能检测文字和竖线边界，自动确定检测区域\n"
            "• 仅在文字/竖线外侧区域检测黑色圆圈\n"
            "• 圆圈最大直径可配置（默认25mm/2.5cm）\n"
            "• 用与底色一致的颜色填充检测到的圆洞\n"
            "• 边缘覆盖：将文件四周边缘用底色覆盖\n"
            "• 右侧预览区可预览原图和处理后的效果\n"
            "• 支持鼠标滚轮缩放、拖拽查看"
        )
        self.info_label.setStyleSheet("font-size: 14px;")
        left_layout.addWidget(self.info_label)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.process_btn = QPushButton("开始处理")
        self.process_btn.setObjectName("ActionBtn")
        self.process_btn.clicked.connect(self.start_processing)
        btn_layout.addWidget(self.process_btn)

        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633; color: white;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)

        left_layout.addLayout(btn_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("待开始")
        left_layout.addWidget(self.progress_bar)

        # 日志框
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(180)
        left_layout.addWidget(self.log_box, 1)

        # === 右侧：预览区（原图和处理后并排显示） ===
        self.preview_splitter = QSplitter(Qt.Vertical)

        self.before_panel = PreviewPanel("原图预览")
        self.after_panel = PreviewPanel("处理后预览")
        self.preview_splitter.addWidget(self.before_panel)
        self.preview_splitter.addWidget(self.after_panel)
        self.preview_splitter.setStretchFactor(0, 1)
        self.preview_splitter.setStretchFactor(1, 1)

        # === 中间：文件树浏览器 ===
        tree_container = QWidget()
        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setContentsMargins(2, 2, 2, 2)
        self.tree_label = QLabel("文件浏览器")
        self.tree_label.setStyleSheet("font-weight: bold; padding: 2px;")
        tree_layout.addWidget(self.tree_label)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setStyleSheet("""
            QTreeWidget { background-color: #0D1117; border: 1px solid #30363D; border-radius: 3px; font-size: 13px; color: #E0E0E0; }
            QTreeWidget::item { padding: 3px; }
            QTreeWidget::item:selected { background-color: #1F6FEB; color: white; }
        """)
        self.file_tree.itemClicked.connect(self.on_tree_item_clicked)
        self.file_tree.currentItemChanged.connect(self.on_tree_current_changed)
        tree_layout.addWidget(self.file_tree)

        # 分割器（三栏：设置 | 文件树 | 预览）
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(left_panel)
        self.main_splitter.addWidget(tree_container)
        self.main_splitter.addWidget(self.preview_splitter)
        self.main_splitter.setStretchFactor(0, 2)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setStretchFactor(2, 3)
        self.main_splitter.setSizes([300, 200, 500])
        self.layout.addWidget(self.main_splitter, 1)

        # 应用默认主题
        self.apply_theme()

        # 存储处理结果
        self.process_results = []
        self.worker = None
        self.source_files = []  # 源目录下的所有JPG文件列表

        # 连接预览导航按钮
        self.before_panel.prev_btn.clicked.connect(lambda: self._tree_navigate(-1))
        self.before_panel.next_btn.clicked.connect(lambda: self._tree_navigate(1))
        # 处理结果预览取消上一页/下一页，只随动原图预览
        self.after_panel.prev_btn.hide()
        self.after_panel.next_btn.hide()

    def apply_theme(self):
        """根据当前主题应用对应的界面样式"""
        colors = self._DARK_COLORS if self._current_theme == 'dark' else self._LIGHT_COLORS
        qss = self.DARK_QSS if self._current_theme == 'dark' else self.LIGHT_QSS
        self.setStyleSheet(qss)
        # 更新标题颜色
        self.lbl_title.setStyleSheet(
            f"color: {colors['accent']}; font-size: 26px; font-weight: bold;"
            f"font-family: 'SimHei','黑体','Microsoft YaHei'; padding: 2px 0 6px 0;")
        # 更新说明文本颜色
        self.info_label.setStyleSheet(f"color: {colors['secondary']}; font-size: 14px;")
        # 更新文件浏览器标题颜色
        self.tree_label.setStyleSheet(f"color: {colors['accent']}; font-weight: bold; padding: 2px;")
        # 更新文件树样式(文件名文字: 浅色主题用深黑加大字号)
        _tree_fs = 15 if self._current_theme == 'light' else 13
        self.file_tree.setStyleSheet(
            f"QTreeWidget {{ background-color: {colors['bg_dark']}; border: 1px solid {colors['border']};"
            f" border-radius: 3px; font-size: {_tree_fs}px; color: {colors['text']}; }}"
            f"QTreeWidget::item {{ padding: 3px; }}"
            f"QTreeWidget::item:selected {{ background-color: #1F6FEB; color: white; }}")
        # 更新树节点颜色: 目录行(顶层项)加深+加粗, 与文件名区分
        _dir_color = '#0e2f44' if self._current_theme == 'light' else colors['accent']
        root = self.file_tree.invisibleRootItem()
        for i in range(root.childCount()):
            dir_item = root.child(i)
            _f = dir_item.font(0)
            _f.setBold(True)
            dir_item.setFont(0, _f)
            dir_item.setForeground(0, QColor(_dir_color))
        # 更新预览面板样式
        for panel in [self.before_panel, self.after_panel]:
            panel.header.setStyleSheet(
                f"color: {colors['accent']}; font-size: 14px; font-weight: bold; padding: 2px;")
            panel.page_label.setStyleSheet(f"color: {colors['text']}; font-size: 12px;")
            panel.path_label.setStyleSheet(f"color: {colors['secondary']}; font-size: 14px; padding: 3px;")
        # 更新图像视图背景
        for panel in [self.before_panel, self.after_panel]:
            panel.image_view.setStyleSheet(
                f"background-color: {colors['view_bg']}; border: 1px solid {colors['border']}; border-radius: 3px;")

    def _switch_theme(self, index):
        """切换界面主题：0=浅色界面，1=褐色界面"""
        self._current_theme = 'light' if index == 0 else 'dark'
        self.apply_theme()
        # 重新预览当前文件以更新图像视图背景
        files = getattr(self, '_tree_files', [])
        idx = getattr(self, '_tree_current_idx', -1)
        if 0 <= idx < len(files):
            self.preview_file_by_path(files[idx])

    def browse_input_dir(self):
        """选择输入目录"""
        d = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if d:
            self.input_dir.setText(d)
            if self.auto_output_dir.isChecked():
                output_path = os.path.join(d, "图像处理结果")
                self.output_dir.setText(output_path)
            self._scan_source_files(d)
            self.build_file_tree(d)

    def browse_output_dir(self):
        """选择输出目录"""
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.output_dir.setText(d)
            # 取消自动输出目录选项
            self.auto_output_dir.setChecked(False)

    def on_auto_output_changed(self, state):
        """自动输出目录选项改变"""
        if state == Qt.Checked and self.input_dir.text():
            output_path = os.path.join(self.input_dir.text(), "图像处理结果")
            self.output_dir.setText(output_path)

    def build_file_tree(self, root_dir):
        """构建文件浏览器树：一级=子目录(默认折叠)+根目录下的JPG文件。"""
        self.file_tree.clear()
        self._tree_files = []
        self._tree_current_idx = -1
        if not root_dir or not os.path.isdir(root_dir):
            return
        self._tree_root_dir = root_dir
        try:
            entries = sorted(os.listdir(root_dir))
            for sub in entries:
                sub_path = os.path.join(root_dir, sub)
                if not os.path.isdir(sub_path):
                    continue
                count = 0
                sub_files = []
                for r, d, files in os.walk(sub_path):
                    for f in sorted(files):
                        if f.lower().endswith(('.jpg', '.jpeg')):
                            sub_files.append(os.path.join(r, f))
                            count += 1
                if count == 0:
                    continue
                dir_item = QTreeWidgetItem(self.file_tree)
                dir_item.setText(0, f"📁 {sub} ({count})")
                _dir_font = dir_item.font(0)
                _dir_font.setBold(True)
                dir_item.setFont(0, _dir_font)
                dir_item.setForeground(0, QColor('#00F0FF' if self._current_theme == 'dark' else '#0e2f44'))
                dir_item.setData(0, Qt.UserRole, ("dir", sub_path))
                for fp in sub_files:
                    file_item = QTreeWidgetItem(dir_item)
                    file_item.setText(0, os.path.basename(fp))
                    file_item.setData(0, Qt.UserRole, ("file", fp))
                    self._tree_files.append(fp)
            root_jpgs = []
            for f in entries:
                fp = os.path.join(root_dir, f)
                if os.path.isfile(fp) and f.lower().endswith(('.jpg', '.jpeg')):
                    root_jpgs.append(fp)
            if root_jpgs:
                root_item = QTreeWidgetItem(self.file_tree)
                root_item.setText(0, f"📁 根目录 ({len(root_jpgs)})")
                root_item.setForeground(0, QColor('#00F0FF' if self._current_theme == 'dark' else self._LIGHT_COLORS['accent']))
                root_item.setData(0, Qt.UserRole, ("dir", root_dir))
                for fp in root_jpgs:
                    file_item = QTreeWidgetItem(root_item)
                    file_item.setText(0, os.path.basename(fp))
                    file_item.setData(0, Qt.UserRole, ("file", fp))
                    self._tree_files.append(fp)
        except Exception as e:
            self.log(f"构建文件树出错: {e}")

    def on_tree_item_clicked(self, item, column):
        """点击文件树节点：文件则预览，目录则展开/折叠"""
        data = item.data(0, Qt.UserRole)
        if data and data[0] == "file":
            filepath = data[1]
            if filepath in self._tree_files:
                self._tree_current_idx = self._tree_files.index(filepath)
                self._update_nav_buttons()
            self.preview_file_by_path(filepath)

    def on_tree_current_changed(self, current, previous):
        """键盘上下键移动选中项时联动预览"""
        if current is None:
            return
        data = current.data(0, Qt.UserRole)
        if data and data[0] == "file":
            filepath = data[1]
            if filepath in self._tree_files:
                self._tree_current_idx = self._tree_files.index(filepath)
                self._update_nav_buttons()
            self.preview_file_by_path(filepath)

    def preview_file_by_path(self, filepath):
        """按文件路径预览：原图+处理后对比。
        处理后结果按输入目录相对路径匹配(输出保持输入目录结构)。"""
        if not filepath or not os.path.isfile(filepath):
            return
        # 原图（如果勾选了边缘覆盖，传入margin参数以显示红框）
        edge_mm = self.edge_margin_spin.value() if self.edge_cover_check.isChecked() else 0
        dpi_val = 300
        try:
            img = Image.open(filepath)
            img.load()
            self.before_panel.show_pil_image(img, margin_mm=edge_mm, dpi=dpi_val)
            self.before_panel._filepath = filepath
            self.before_panel.path_label.setText(filepath)
        except Exception:
            pass
        # 处理后结果：按相对输入目录的路径匹配(输出保持输入目录结构)
        self.after_panel.clear()
        self.after_panel.path_label.setText("")
        output_dir = self.output_dir.text().strip()
        root_dir = getattr(self, '_tree_root_dir', '') or self.input_dir.text().strip()
        if output_dir and os.path.isdir(output_dir) and root_dir:
            rel = os.path.relpath(filepath, root_dir)
            after_path = os.path.join(output_dir, rel)
            if os.path.isfile(after_path):
                try:
                    img2 = Image.open(after_path)
                    img2.load()
                    self.after_panel.show_pil_image(img2)
                    self.after_panel._filepath = after_path
                    self.after_panel.path_label.setText(after_path)
                except Exception:
                    pass

    def _tree_navigate(self, direction):
        """通过文件树列表导航：-1上一页，+1下一页，原图和处理后联动"""
        files = getattr(self, '_tree_files', [])
        idx = getattr(self, '_tree_current_idx', -1)
        new_idx = idx + direction
        if 0 <= new_idx < len(files):
            self._tree_current_idx = new_idx
            self._update_nav_buttons()
            self.preview_file_by_path(files[new_idx])

    def _update_nav_buttons(self):
        """更新原图面板的上一页/下一页按钮状态和页码"""
        files = getattr(self, '_tree_files', [])
        idx = getattr(self, '_tree_current_idx', -1)
        total = len(files)
        self.before_panel.prev_btn.setEnabled(idx > 0)
        self.before_panel.next_btn.setEnabled(idx < total - 1)
        if 0 <= idx < total:
            self.before_panel.page_label.setText(f"{idx + 1} / {total}")

    def _refresh_edge_preview(self):
        """边缘覆盖勾选/改值时，实时刷新原图预览的红框"""
        files = getattr(self, '_tree_files', [])
        idx = getattr(self, '_tree_current_idx', -1)
        if 0 <= idx < len(files):
            self.preview_file_by_path(files[idx])

    def start_processing(self):
        """开始处理"""
        input_dir = self.input_dir.text().strip()
        if not input_dir:
            QMessageBox.warning(self, "提示", "请先选择输入目录")
            return

        if not os.path.exists(input_dir):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return

        # 确定输出目录
        output_dir = self.output_dir.text().strip()
        if not output_dir:
            QMessageBox.warning(self, "提示", "请指定输出目录")
            return

        # 如果启用了自动创建输出目录
        if self.auto_output_dir.isChecked():
            output_dir = os.path.join(input_dir, "图像处理结果")
            os.makedirs(output_dir, exist_ok=True)
            self.output_dir.setText(output_dir)
            self.log(f"✓ 已创建输出目录: {output_dir}")

        # 清空之前的结果
        self.process_results = []
        self.log_box.clear()

        max_diameter = self.max_diameter_spin.value()
        deskew = self.deskew_check.isChecked()
        remove_border = self.border_check.isChecked()
        remove_shadow = self.shadow_check.isChecked()
        dpi = self.dpi_spin.value()
        edge_cover = self.edge_cover_check.isChecked()
        edge_margin = self.edge_margin_spin.value()
        auto_darken = self.darken_check.isChecked()

        self.log("=" * 60)
        self.log(f"开始处理目录: {input_dir}")
        self.log(f"输出目录: {output_dir}")
        self.log(f"圆圈最大直径: {max_diameter}mm")
        self.log(f"纠偏: {'开启（自动检测，纯旋转不变形）' if deskew else '关闭'}")
        self.log(f"去黑边: {'开启' if remove_border else '关闭'}")
        self.log(f"去孔影: {'开启' if remove_shadow else '关闭'}")
        self.log(f"边缘覆盖: {'开启' if edge_cover else '关闭'}")
        if edge_cover:
            self.log(f"边缘覆盖边距: {edge_margin}mm")
        self.log(f"自动加深: {'开启' if auto_darken else '关闭'}")
        self.log(f"DPI: {dpi}")
        thread_count = self.thread_spin.value()
        self.log(f"并行线程: {thread_count}")
        self.log("=" * 60)

        # 创建工作线程
        self.worker = CircleDetectionWorker(input_dir, output_dir, max_diameter,
                                            deskew=deskew, remove_border=remove_border,
                                            thread_count=thread_count,
                                            edge_cover=edge_cover, edge_margin_mm=edge_margin,
                                            dpi=dpi, auto_darken=auto_darken,
                                            remove_shadow=remove_shadow)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.result_signal.connect(self.display_results)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.file_done_signal.connect(self._on_file_done)

        # 清空处理后预览
        self.after_panel.clear()

        self.worker.start()

        # 更新按钮状态
        self.process_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)

    def update_progress(self, current, total):
        """更新进度"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress_bar.setValue(int(percentage))
        self.progress_bar.setFormat(f"{current} / {total} ({percentage:.1f}%)")

    def display_results(self, results):
        """显示处理结果"""
        self.process_results = results

        if not results:
            self.log("\n✓ 未处理任何文件")
            return

        success_count = sum(1 for r in results if r['success'])
        circles_total = sum(r['circles_found'] for r in results)

        self.log(f"\n处理统计：")
        self.log(f"  总文件数: {len(results)}")
        self.log(f"  成功处理: {success_count}")
        self.log(f"  失败: {len(results) - success_count}")
        self.log(f"  检测到的圆圈总数: {circles_total}")

        # 处理完成后：不整批接管预览列表，仅刷新当前预览原件的对应结果
        # (处理后预览始终只展示与当前选中原件对应的输出)
        cur = self.before_panel._filepath if hasattr(self.before_panel, '_filepath') else None
        if cur and os.path.isfile(cur):
            self.preview_file_by_path(cur)

    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress_bar.setFormat("已完成" if success else "已停止")

        # 恢复按钮状态
        self.process_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.warning(self, "结束", message)

    def log(self, msg):
        """添加日志"""
        self.log_box.append(f">> {msg}")

    # === 预览相关方法 ===

    def _on_file_done(self, output_path):
        """单个文件处理完成。
        不再自动追加/切换处理后预览——处理中间的结果不打扰当前预览；
        若当前正预览的原件恰好就是刚完成的文件，则刷新其对应结果。"""
        cur = self.before_panel._filepath if hasattr(self.before_panel, '_filepath') else None
        if not cur or not os.path.exists(output_path):
            return
        # 仅当刚完成的输出正是当前预览原件的对应结果时刷新(相对目录结构匹配)
        output_dir = self.output_dir.text().strip()
        input_root = self.input_dir.text().strip()
        if output_dir and input_root:
            try:
                rel = os.path.relpath(cur, input_root)
                if os.path.normcase(os.path.join(output_dir, rel)) == os.path.normcase(output_path):
                    self.preview_file_by_path(cur)
            except Exception:
                pass

    def _scan_source_files(self, source_dir):
        """扫描源目录下的所有JPG文件，更新预览"""
        jpg_files = []
        for root, dirs, files in os.walk(source_dir):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    jpg_files.append(os.path.join(root, filename))

        def _natural_key(path):
            return [int(t) if t.isdigit() else t.lower()
                    for t in re.split(r'(\d+)', path)]
        jpg_files.sort(key=_natural_key)

        self.source_files = jpg_files
        if jpg_files:
            self.before_panel.set_files(jpg_files)
            self.before_panel.set_current_index(0)
            self._show_before_preview(0)
        else:
            self.before_panel.clear()

    def _show_before_preview(self, index):
        """显示原图预览"""
        if 0 <= index < len(self.source_files):
            try:
                img = Image.open(self.source_files[index])
                img.load()
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                dpi = self.dpi_spin.value()
                margin_mm = self.edge_margin_spin.value() if self.edge_cover_check.isChecked() else 0
                self.before_panel.show_pil_image(img, margin_mm, dpi)
            except Exception as e:
                self.before_panel.image_view.clear_image()
                self.before_panel.path_label.setText(f"加载失败: {e}")

    def _show_after_preview(self, index):
        """显示处理后预览"""
        files = self.after_panel._files
        if 0 <= index < len(files):
            try:
                img = Image.open(files[index])
                img.load()
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                self.after_panel.show_pil_image(img, 0, 0)
            except Exception as e:
                self.after_panel.image_view.clear_image()
                self.after_panel.path_label.setText(f"加载失败: {e}")

    def _navigate_preview(self, panel, direction):
        """导航预览：direction=-1上一页，+1下一页"""
        current = panel.get_current_index()
        new_idx = current + direction
        if 0 <= new_idx < panel.file_count():
            panel.set_current_index(new_idx)
            if panel is self.before_panel:
                self._show_before_preview(new_idx)
                if new_idx < self.after_panel.file_count():
                    self.after_panel.set_current_index(new_idx)
                    self._show_after_preview(new_idx)
            elif panel is self.after_panel:
                self._show_after_preview(new_idx)
                if new_idx < self.before_panel.file_count():
                    self.before_panel.set_current_index(new_idx)
                    self._show_before_preview(new_idx)


# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置Windows 7兼容性
    try:
        # 启用高DPI支持
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except:
        pass
    
    window = BlackCircleRemoverPage()
    window.setWindowTitle("同美图像质检工具 v" + VERSION)
    window.setGeometry(100, 100, 1400, 900)
    window.show()
    window.raise_()  # 确保窗口显示在最前面
    window.activateWindow()  # 激活窗口
    
    sys.exit(app.exec_())
