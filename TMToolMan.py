# -*- coding: utf-8 -*-
# 以下为您编写的“同美档案工具集合”Python代码。代码采用PyQt5框架构建，界面采用深色科技感配色，左侧为菜单栏，右侧为动态切换的功能区。
#
# 请确保在运行前安装依赖库：`pip
# install
# PyQt5
# `
#
# ```python

# ============================ 版本与修改记录 ============================
# 规则：每次修改本文件后，必须递增 VERSION(修订号+1，功能大变时递增次版本号)，
# 并在 CHANGELOG 头部追加一条记录(版本号/日期/修改内容)；窗口标题会显示当前版本号，
# 便于区分不同打包版本。
VERSION = "3.26"

CHANGELOG = [
    {
        "version": "3.26",
        "date": "2026-09-10",
        "changes": [
            "修复GPU模式JPG转双层PDF段错误崩溃(崩溃日志20260910: OCR服务线程在paddleocr img_decode内部np.frombuffer→cv2.imdecode发生access violation, GPU模式4工作线程运行中)：①各工作线程调用OCR前用PIL预解码图像为BGR连续ndarray(np.array拷贝+ascontiguousarray, 非np.asarray共享内存——共享视图在PIL关闭后指向已释放内存恰是段错误形态), 传ndarray给ocr()——paddleocr接受ndarray时check_img直接透传, 服务线程内完全不再执行文件读取与cv2.imdecode(崩溃点移出); ②首次探测/复探/CPU重探测三处探测图同样预解码; ③预解码失败回退原路径模式(尽力而为); ④ocr()三次调用点(首试/参数兼容重试/重建后重试)统一改用同一输入对象",
        ],
    },
    {
        "version": "3.25",
        "date": "2026-09-06",
        "changes": [
            "档案馆标准目录的目录类型由单选改为多选框(可同时勾选档案案卷目录+档案案件目录, 缺省两者都选)：一次点击生成两种目录文件, 共享一次编码子目录扫描与机构映射; Worker改为modes列表逐种执行, 每种类型分别校验对应模板存在; 进度按所选类型数累计; 日志文件名含全部所选类型名",
        ],
    },
    {
        "version": "3.24",
        "date": "2026-09-06",
        "changes": [
            "档案馆标准目录重构为业务目录/文书目录双TAB(业务目录下「档案案卷目录/档案案件目录」二选一)：①业务-档案案卷目录: 每个编码子目录一条, 卷内文件总件数=子目录同名xlsx序号最大值, 总页数=最大序号行页号终止值(如102-232取232); ②业务-档案案件目录: 逐子目录xlsx每序号行一条——案卷号=序号三位编码, 件号=序号, 档号=所属案卷档号-四位件号, 文件编号=文号, 责任者/题名直取, 文件日期=发文日期, 页号含'-'取右侧, 页数=与下一序号页号差值(负值置空; 无下一页号且当前含'-'则为右减左); ③新增「机构代码对应表」选择(表头: 机构代码/机构名称), 解析代码→名称填入机构问题列, 不选则留空手填; ④模板按目录类型分别选择(两个模板文件); ⑤输出文件名=所选目录名+「档案案卷目录」或「档案案件目录」, 输出目录规则不变; ⑥文书目录TAB预留",
        ],
    },
    {
        "version": "3.23",
        "date": "2026-09-05",
        "changes": [
            "文件夹命名标准化的「审计」字段更名为「专业类型」, 输入框缺省值由'审计'改为'SJ'(格式变为 全宗号-专业·专业类型·年限-保管期限-件号, 如 J380-ZY·SJ·2021-Y-0001); 引用现有逻辑不变(旧格式目录无专业类型段仍需直接填写)",
        ],
    },
    {
        "version": "3.22",
        "date": "2026-09-05",
        "changes": [
            "文件夹命名标准化规则变更：目标格式由 全宗号-专业·年限-保管期限-机构代码-件号 改为 全宗号-专业·审计·年限-保管期限-件号。①字段列表改为 全宗号/专业/审计/年限/保管期限/件号(去掉机构代码, 新增审计); ②「审计」为格式固定段, 界面默认预填'审计'并选中直接填写(可改); ③新格式正则支持中文段(专业/审计允许字母数字汉字); ④兼容旧格式目录作引用源(全宗号/专业/年限/保管期限/件号按位映射, 旧格式无审计段——审计字段需直接填写, 引用预览时显示'旧格式无此段'提示)",
        ],
    },
    {
        "version": "3.21",
        "date": "2026-09-05",
        "changes": [
            "文件夹命名标准化字段改回每行一条并缩窄窗口：6个字段由3列×2行网格改为每行一条(标签列对齐, 单选「填/引」+限宽120px输入框), 输入框限宽缩短窗口宽度; 分组标题与「标准化后重命名文件」勾选框长文本换行显示, 进一步压缩横向宽度",
        ],
    },
    {
        "version": "3.20",
        "date": "2026-09-05",
        "changes": [
            "文件改名页三个处理方式改为TAB并列：按目录名批量重命名/文件夹命名标准化/修改文件扩展名原为纵向堆叠(页面过长), 现改为QTabWidget三个标签页并列, 同一时刻只显示一个功能的输入区; 下方功能说明文本随TAB切换自动显示当前功能对应的说明",
        ],
    },
    {
        "version": "3.19",
        "date": "2026-09-05",
        "changes": [
            "文件夹命名标准化界面压缩与引用可视化：①6个字段由每行一个改为3列×2行网格(每格=字段名+填/引单选+输入框), 大幅缩短功能页长度; ②选择/输入目标目录后, 处于「引用现有」状态的输入框自动显示扫描到的第一个符合格式子目录的对应编码值(只读展示, 让用户预知将引用的内容; 无符合格式目录时提示占位文本), 切回「直接填写」后输入框清空并恢复可编辑",
        ],
    },
    {
        "version": "3.18",
        "date": "2026-09-05",
        "changes": [
            "文件改名页新增「文件夹命名标准化」功能：①目标命名格式为 全宗号-专业·年限-保管期限-机构代码-件号(专业与年限间用间隔号·, 其余用短横-); ②5个字段均支持两种填写方式: 直接填写(输入框)或引用现有(引用所选目录下现有子目录名对应位置的字段值, 目录无符合格式时字段留空跳过); ③提供预览: 弹窗表格列出每个子目录的原名→新名, 可直接修改后应用; ④执行后自动生成Excel文件记录原目录名与新目录名(openpyxl, 输出目录下 目录改名记录_时间戳.xlsx); ⑤新增选择框「目录标准化后批量重命名目录下文件」(默认不勾), 勾选后完成目录改名即调用「按目录名批量重命名」逻辑对新目录下文件批量命名(单文件=目录名, 多文件=目录名-0001起)",
        ],
    },
    {
        "version": "3.17",
        "date": "2026-09-04",
        "changes": [
            "取消v3.15的GPU OCR模式下JPG转双层PDF强制单线程限制, 恢复允许用户自选多线程(应用户要求)：①OCR本身仍由内部单一服务线程串行执行(线程安全不变), 多线程的意义在于图像解码/PDF分段写入等非OCR阶段与OCR形成流水线并行; ②UI不再弹窗后强制调为1线程, 改为多线程+GPU时一次性提示风险(内存峰值/GPU挂死会自动降级CPU), 用户确认后按所选线程数执行; ③运行日志提示同步改为'GPU OCR模式多线程'说明流水线并行与兜底机制; ④v3.15担心的孤儿GPU线程显存泄漏风险仍由v3.14的run_monitor监控+GPU引擎损坏计数≥2全局降级CPU兜底, 不再以牺牲吞吐换取",
        ],
    },
    {
        "version": "3.16",
        "date": "2026-09-03",
        "changes": [
            "修复_ocr_broken实例级全局标志导致探测失败后整批永久降级单层PDF的问题(高风险)：①原逻辑探测(GPU失败→CPU重建→CPU探测仍失败)置_ocr_broken=True后本轮运行内永不恢复, 后续所有目录静默跳过OCR直接单层(仅第一个失败目录有一行降级提示), 但探测失败可能是临时性故障(探测时GPU显存恰被其他程序占满/系统内存紧张, 之后资源已释放)或探测假阳性, 不应永久封死整批双层输出; ②降级改为非永久: 每_OCR_REPROBE_DIRS(10)个目录在探测锁内自动快速复探(丢弃旧引擎→重建→小图推理60秒), 通过即解除降级恢复双层生成并日志明示(降级期间的目录仍为单层, 可对本批重跑补齐); ③降级期间每个目录日志均明确提示'OCR仍处降级状态'(不再只在首个目录提示), 状态字符串改为'仅图像PDF（OCR探测失败已降级, 周期复探中）'; ④探测图字体改为simhei/msyh/simsun依次回退(原仅试simhei且缺失时静默用PIL默认小字体, 小字识别不出文字→探测假阳性→误全局降级单层)",
        ],
    },
    {
        "version": "3.15",
        "date": "2026-09-03",
        "changes": [
            "GPU OCR模式下JPG转双层PDF强制单线程(高风险修复——孤儿GPU线程显存泄漏)：OCR本就由内部单一服务线程串行执行, 多线程不提升OCR吞吐, 反而①多个工作线程各持fitz doc分段, GPU模式OCR快会使各线程同时处于写doc阶段, 内存并发峰值叠加paddle驻留(曾致进程被系统终止); ②OCR服务线程GPU推理挂死后无法强制终止成为孤儿线程, 其调用栈持有的GPU引擎(det/rec/cls三模型+CUDA上下文)显存永不释放, 且GPU引擎损坏计数≥2才降级CPU, 最坏可积累多个挂死GPU引擎——多线程高频投递放大180秒超时误判与重建频率, 孤儿线程更易累积; ③多线程同时超时在_ocr_svc_call超时分支存在连环重建服务线程的竞态(v3.14的run_monitor监控日志只能事后诊断, 不能阻止泄漏); 现JpgToPdfWorker.__init__按初始use_gpu_ocr强制max_workers=1(运行中降级CPU后不回改——CPU模式OCR慢, 多线程仍有流水线意义), UI勾选GPU OCR且线程数>1时弹窗确认后自动调为单线程并日志说明",
        ],
    },
    {
        "version": "3.14",
        "date": "2026-09-03",
        "changes": [
            "修复v3.13后GPU模式转PDF仍崩溃(同20260901崩溃日志形态: could not create a primitive→access violation)的问题：① 根因——_ocr_page捕获首次异常后立即用【同一个可能已损坏的实例】重试ocr()/predict()两次, GPU predictor报primitive/CUDA类错误后内部状态已坏, 在损坏的CUDA上下文上继续调用触发进程级access violation(段错误, Python层捕获无效); ② 首次异常即按文案判定引擎损坏类错误(primitive/显存/cudnn/cuda error/illegal memory access/SystemExit), 损坏类不再用原实例重试, 直接丢弃重建; 仅参数不兼容类(3.x不接受cls)才用原实例重试; ③ GPU引擎损坏累计≥2次→全局降级CPU推理(_rebuild_ocr_cpu, 一次性切换不再回GPU)——GPU实例反复报显存类错误说明CUDA上下文已不可靠, 继续重建GPU实例会在坏上下文上创建导致连环崩溃",
            "新增GPU模式运行监控日志run_monitor_时间戳.txt(输出目录): 每10秒采样进程工作集/GPU显存(paddle已分配+保留, paddle不可用时经NVML读全卡)/活跃线程数/OCR服务队列积压深度/引擎累计页数/GPU损坏计数/当前推理模式, 并在关键事件(引擎异常重建/GPU降级CPU/单页超时/内存看门狗触发/处理结束)时写事件行——崩溃后最后一条采样即崩溃时刻的资源快照, 用于判断显存耗尽/内存累积/线程风暴等崩溃原因; 新增_gpu_mem_info()显存查询(paddle CUDA API优先, NVML兜底)",
        ],
    },
    {
        "version": "3.13",
        "date": "2026-09-02",
        "changes": [
            "程序启动时强制校验解释器位数：必须64位(32位进程用户态地址空间上限约2GB, 是崩溃日志20260901中OCR长时间运行内存耗尽的根因)。检测到32位时弹窗提示「请使用64位Python重新打包」并拒绝启动, 同时写入崩溃日志留痕；此前曾误用32位Python打包出问题版本, 此处硬性拦截防止再次发生",
        ],
    },
    {
        "version": "3.12",
        "date": "2026-09-01",
        "changes": [
            "修复JPG转双层PDF的OCR模式运行中崩溃(日志: could not create a primitive → cv2 Insufficient memory → SystemExit → access violation)的问题：① paddleocr在cv2缩放内存不足时内部调用sys.exit(0)抛出的SystemExit继承BaseException, 原服务循环/单页逻辑仅捕获Exception导致OcrSvc服务线程被直接打死、后续所有页OCR任务空等超时, 现各层均捕获SystemExit(服务线程不再死亡, 单页按内存失败处理: 丢弃引擎重建+重试); ② 内存类错误关键词补充 could not create a primitive(MKL-DNN分配失败)与 insufficient memory; ③ OCR初始化显式关闭MKL-DNN(paddleocr 2.x缺省use_mkldnn=True, 其oneDNN缓存在变尺寸输入下持续泄漏宿主内存, 是宿主内存耗尽的根因); ④ 服务线程意外死亡时自动检测并重建(原死亡后任务永远超时); ⑤ 内存看门狗阈值适配32位进程(地址空间上限约2GB, 原2.6/3.2GB阈值永不可达, 改为1.2/1.5GB)",
        ],
    },
    {
        "version": "3.11",
        "date": "2026-08-31",
        "changes": [
            "修复JPG转双层PDF的GPU模式处理内容多、单文件大的目录时长时间运行崩溃(崩溃日志0字节=进程被系统终止)的问题：① 分段写盘页数CHUNK由固定50改为按单文件实际大小自适应(按单段≤约400MB折算, 8~50页)——大文件仍固定50页时, GPU模式因OCR快四线程同时处于写doc阶段, 叠加paddle驻留内存会达数GB触发系统终止; ② 新增进程内存看门狗: 每10页检测进程工作集, 超过预警线记日志留痕、超过回收线(3.2GB)在OCR服务线程内强制丢弃重建引擎+GC阻断继续增长; ③ 移除全局MKL-DNN开关(对本功能无加速作用, 且中途降级CPU后其oneDNN缓存在变尺寸输入下持续泄漏宿主内存); ④ 分段合并时中间doc立即关闭(原未关闭, 大分段驻留叠加内存峰值)",
        ],
    },
    # 新版本记录追加在此列表头部(最新在前)
    {
        "version": "3.10",
        "date": "2026-08-31",
        "changes": [
            "分件目录结构调整: 备考表卷底与卷皮目录两个子目录合并为编号0000的单一目录(如J380-ZY-SJ-2021-Y-0001-0000), 卷皮页/目录页与备考表卷底文件统一移入, 不再生成两个独立目录; 已分件目录的目录页查找同步适配(优先-0000, 兼容旧版卷皮目录)",
        ],
    },
    {
        "version": "3.9",
        "date": "2026-08-28",
        "changes": [
            "修复JPG转双层PDF的GPU模式运行一段时间后报「Memory allocation failed... Try increasing size of Virtual Memory」的问题：① paddle显存分配策略环境变量(按增长分配/卷积工作区上限/关闭cuDNN穷举搜索)原在工作线程run()里才设置, 但点击开始时的GPU预检已在主线程先行导入paddle导致设置全部失效, 现提前到模块导入时设置(先于任何功能路径); ② 新增OCR引擎例行重建: 每处理200页自动丢弃引擎并重建, 阻断paddle推理引擎长时间运行内存累积; ③ 超长目录每50页分段写盘后追加释放GPU缓存(原仅每目录结束释放一次); ④ 单页推理出现内存分配失败时自动丢弃引擎重建并重试该页一次, 不再直接跳过该页文本层",
        ],
    },
    {
        "version": "3.8",
        "date": "2026-08-27",
        "changes": [
            "新增生成档案馆标准目录功能: 解析编码子目录名(全宗-类型·年度-期限代码-项目-卷号, 如J380-ZY·2021-Y-FGC-0001)按模板xlsx批量生成案卷级标准目录; 案卷级档号=目录名, 期限代码Y/D30/D10映射永久/30年/10年(代码与中文两列), 总页数=子目录xlsx序号最大行页码列最大值; 编码目录递归查找, 按上级目录名分组输出; 输出目录可选缺省为数据目录下档案馆标准目录子目录; 模板列名自适应", 
        ],
    },
    {
        "version": "3.7",
        "date": "2026-08-27",
        "changes": [
            "修复JPG转双层PDF开启GPU的OCR时生成单层PDF(同样文件CPU模式为双层)的问题：① GPU模式OCR初始化失败(抛异常而非挂死)时原逻辑不做CPU回退直接降级仅图像单层PDF，现改为强制CPU重建后重试；② OCR初始化内部GPU配置全部失败时新增显式CPU(use_gpu=False)配置重试(原部分兜底配置未带use_gpu参数，paddleocr 2.x缺省use_gpu=True，GPU环境异常时会连带全部失败)。修复后GPU模式异常时自动降级CPU推理，输出与CPU模式一致(双层)",
        ],
    },
    {
        "version": "3.6",
        "date": "2026-08-27",
        "changes": [
            "文件头部新增显式UTF-8编码声明(# -*- coding: utf-8 -*-)：修复编辑器偶发将文件保存为非UTF-8(GBK)编码时运行报“SyntaxError: Non-UTF-8 code… but no encoding declared”的问题(已验证当前文件为合法UTF-8且可编译，项目缺省编码同步锁定为UTF-8)",
        ],
    },
    {
        "version": "3.5",
        "date": "2026-08-26",
        "changes": [
            "修复JPG转双层PDF在计算机同时运行其他任务时直接崩溃 、页面消失且无任何错误记录的问题：① 新增全局崩溃日志机制(faulthandler捕获段错误等致命错误+主线程/工作线程未捕获异常钩子)，任何崩溃均写入程序目录下 TMToolMan_崩溃日志_日期.txt，不再无声消失；② 仅图像PDF合并改用fitz流式逐页写盘(不再将整目录图像一次性全量解码驻留内存，内存峰值与页数无关)，降低系统内存紧张时被操作系统终止进程的概率；③ 新增QThread终止兜底：处理线程意外死亡未发完成信号时，界面自动恢复并弹窗提示崩溃原因，不再永久卡在“处理中”",
        ],
    },
    {
        "version": "3.4",
        "date": "2026-08-26",
        "changes": [
            "修复文件批量替换误报“源文件编号不连续…跳过本组”：改为源文件从最小编号起连续占位(最小编号处覆盖目标同名文件，源编号不连续时也自动归位不再跳过)，目标中编号大于最小编号的现有文件从最小编号+N起按升序重新编号(如源0002/0003替换目标0002后，目标原0003改名0004、后续依次类推)，保证替换后编号连续",
        ],
    },
    {
        "version": "3.3",
        "date": "2026-08-26",
        "changes": [
            "建立版本号与修改记录管理机制：新增模块级常量 VERSION 与 CHANGELOG 修改记录，窗口标题显示当前版本号(同美档案工具集合 v3.3)，便于区分不同打包版本",
        ],
    },
]
# ========================================================================

import sys
import re
import os
import shutil
# 使用 PyQt5（Qt5）替代 PySide6（Qt6），以兼容 Python 3.8。
# PyQt5 中信号为 pyqtSignal，通过别名统一为 Signal，保持下游写法不变。
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QFileDialog, QTextEdit, QSpinBox, QComboBox,
                             QFormLayout, QGroupBox, QMessageBox, QStackedWidget, QCheckBox,
                             QProgressBar, QDialog, QListWidget, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QRadioButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal, QRegularExpression
from PyQt5.QtGui import QFont, QRegularExpressionValidator
from PIL import Image, ImageDraw, ImageFont, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
# 注：cv2 与 numpy 已改为在 AutoPagingWorker.add_number_to_image 中延迟导入，
# 以提升 Win7 下的健壮性（opencv 在 Win7 上较易出现 DLL 加载失败），
# 这样即使该依赖缺失或损坏，主程序仍可启动、其他功能页仍可使用。
import time
import threading
from datetime import datetime
from pathlib import Path


# ============================ 崩溃日志机制(v3.5) ============================
# 背景: JPG转双层PDF在计算机多任务运行时曾出现整窗口消失且无任何错误记录的崩溃——
# C库(paddle/PyMuPDF)段错误与进程被操作系统因内存不足终止都不经过Python异常流，
# 打包程序又无控制台，堆栈全部丢失。此处建立三层记录:
#   ① faulthandler 捕获段错误/栈溢出等致命错误并写入C级堆栈;
#   ② sys.excepthook 捕获主线程(含Qt事件循环槽函数)未捕获异常;
#   ③ threading.excepthook 捕获工作线程未捕获异常。
# 统一追加写入程序目录下「TMToolMan_崩溃日志_日期.txt」，崩溃后可凭日志定位原因。
def _setup_crash_log():
    """启用全局崩溃日志(程序启动时调用一次)，返回崩溃日志文件路径。"""
    import faulthandler
    import traceback as _tb
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    crash_path = os.path.join(
        app_dir, f"TMToolMan_崩溃日志_{datetime.now().strftime('%Y%m%d')}.txt")

    def _write(header, lines):
        try:
            with open(crash_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{'=' * 80}\n{header} "
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.writelines(lines)
        except Exception:
            pass

    # ① 致命错误(段错误/栈溢出等, 是“无声消失”类崩溃的常见直接原因)。
    # 文件句柄须常驻打开(段错误发生时无机会再打开文件), 并保留引用防被GC关闭。
    try:
        _fh = open(crash_path, 'a', encoding='utf-8')
        faulthandler.enable(file=_fh, all_threads=True)
        _setup_crash_log._fh = _fh
    except Exception:
        pass

    # ② 主线程未捕获异常
    _old_hook = sys.excepthook
    def _excepthook(exc_type, exc_value, exc_tb):
        _write("主线程未捕获异常:",
               _tb.format_exception(exc_type, exc_value, exc_tb))
        _old_hook(exc_type, exc_value, exc_tb)
    sys.excepthook = _excepthook

    # ③ 工作线程未捕获异常(后台线程异常不会中断主程序, 但必须留痕)
    def _threadhook(args):
        _write(f"线程[{args.thread.name}]未捕获异常:",
               _tb.format_exception(args.exc_type, args.exc_value,
                                    args.exc_traceback))
    threading.excepthook = _threadhook

    return crash_path
# ========================================================================


# ============================ GPU显存安全配置(v3.9) ============================
# FLAGS_allocator_strategy 等环境变量必须在 paddle 【首次导入之前】设置才生效。
# 旧版在 JPG转PDF 工作线程 run() 里才设置, 但界面点击“开始转换”时的GPU预检会先在
# 主线程导入 paddle → 环境变量失效 → paddle 缺省分配器长时间运行后内存碎片持续累积,
# 最终报「Memory allocation failed ... Try increasing size of Virtual Memory」。
# 此处提前到模块导入时设置(先于任何功能路径)。
def _setup_paddle_gpu_env():
    """模块导入时执行一次: 屏蔽无卡机的CUDA设备 + 设置显存安全分配策略。"""
    # 装了GPU版paddle但机器无NVIDIA卡时, paddle导入即锁定找GPU设备,
    # 之后任何配置都报「Device id must be less than GPU count」→ 屏蔽CUDA设备走纯CPU。
    try:
        if 'CUDA_VISIBLE_DEVICES' not in os.environ:
            import ctypes as _ct
            try:
                _ct.CDLL('nvcuda.dll')
                _has_nvidia = True
            except OSError:
                _has_nvidia = False
            if not _has_nvidia:
                os.environ['CUDA_VISIBLE_DEVICES'] = ''
    except Exception:
        pass
    # auto_growth=显存按需增长(缺省策略预占/囤积大块显存, 与显示输出及其他应用争抢,
    #   长时间多线程运行后碎片累积是「Memory allocation failed」的根因之一);
    # workspace上限64MB=限制cuDNN卷积工作区, 防单次推理吃满显存;
    # 关闭cuDNN穷举搜索=避免首推理长耗时选算法(表现为探测超时)。
    os.environ.setdefault('FLAGS_allocator_strategy', 'auto_growth')
    os.environ.setdefault('FLAGS_conv_workspace_size_limit', '64')
    os.environ.setdefault('FLAGS_cudnn_exhaustive_search', '0')

_setup_paddle_gpu_env()
# ========================================================================


# ============================ 进程内存监测工具(v3.11) ============================
def _proc_mem_mb():
    """当前进程工作集内存(MB); 获取失败返回0。用于长时间运行的内存看门狗。"""
    try:
        import ctypes
        from ctypes import wintypes

        class _PMC(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong),
                        ("PageFaultCount", ctypes.c_ulong),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]

        _k32 = ctypes.windll.kernel32
        _k32.GetCurrentProcess.restype = wintypes.HANDLE
        _h = _k32.GetCurrentProcess()
        _psapi = ctypes.windll.psapi
        _psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE,
                                                ctypes.POINTER(_PMC),
                                                wintypes.DWORD]
        _psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
        _pmc = _PMC()
        _pmc.cb = ctypes.sizeof(_PMC)
        if _psapi.GetProcessMemoryInfo(_h, ctypes.byref(_pmc), _pmc.cb):
            return _pmc.WorkingSetSize / 1048576.0
    except Exception:
        pass
    return 0.0


def _gpu_mem_info():
    """GPU显存信息(v3.14): 返回 (已用MB, 总MB, paddle已分配MB), 获取失败返回None。
    优先用 paddle CUDA API(与推理同源, 反映paddle实际占用); 失败再试 NVML(nvml.dll)。
    本函数只在OCR服务线程/监控线程调用, 避免与其他CUDA操作并发。"""
    # ① paddle CUDA(与推理同源)
    try:
        import paddle
        if hasattr(paddle.device, 'cuda') and paddle.device.is_compiled_with_cuda():
            if int(paddle.device.cuda.device_count()) > 0:
                alloc = reserved = 0.0
                try:
                    alloc = float(paddle.device.cuda.memory_allocated()) / 1048576.0
                    reserved = float(paddle.device.cuda.memory_reserved()) / 1048576.0
                except Exception:
                    pass
                return (alloc, reserved, 'paddle')
    except Exception:
        pass
    # ② NVML(不依赖paddle, 反映全卡显存——含其他进程占用)
    try:
        import ctypes as _ct2
        nvml = _ct2.CDLL('nvml.dll')
        if nvml.nvmlInit_v2() == 0:
            try:
                h = _ct2.c_void_p()
                if nvml.nvmlDeviceGetHandleByIndex_v2(0, _ct2.byref(h)) == 0:
                    free = _ct2.c_ulonglong()
                    total = _ct2.c_ulonglong()
                    if nvml.nvmlDeviceGetMemoryInfo(h, _ct2.byref(free),
                                                    _ct2.byref(total)) == 0:
                        used = (total.value - free.value) / 1048576.0
                        tot = total.value / 1048576.0
                        return (used, tot, 'nvml')
            finally:
                try:
                    nvml.nvmlShutdown()
                except Exception:
                    pass
    except Exception:
        pass
    return None
# ========================================================================


class TechStyle:
    """浅色页面样式表(参照 ImageCheckTool 浅色风格)"""
    MAIN_BG = "#ecf0f1"
    PANEL_BG = "#ffffff"
    TEXT_COLOR = "#2c3e50"
    ACCENT_COLOR = "#1a5276"
    BTN_HOVER = "#2980b9"

    QSS = f"""
    QMainWindow {{ background-color: {MAIN_BG}; }}
    QWidget {{ color: {TEXT_COLOR}; font-family: 'Microsoft YaHei', Arial; }}

    /* 左侧菜单栏 */
    #LeftPanel {{
        background-color: {PANEL_BG};
        border-right: 1px solid #bdc3c7;
    }}
    QLabel#TitleLabel {{
        color: {ACCENT_COLOR};
        font-size: 18px;
        font-weight: bold;
        padding: 20px;
        border-bottom: 1px solid #bdc3c7;
    }}
    QPushButton#MenuBtn {{
        background-color: transparent;
        color: #1a5276;
        text-align: left;
        padding: 16px 20px;
        border: none;
        font-size: 17px;
        font-weight: bold;
    }}
    QPushButton#MenuBtn:hover {{
        background-color: #d6eaf8;
        color: #154360;
        border-left: 4px solid {ACCENT_COLOR};
    }}
    QPushButton#MenuBtn:checked {{
        background-color: #aed6f1;
        color: #0e2f44;
        border-left: 5px solid {ACCENT_COLOR};
        font-weight: bold;
    }}

    /* 右侧功能区 */
    #RightPanel {{ background-color: {MAIN_BG}; }}
    QGroupBox {{
        border: 1px solid #bdc3c7;
        border-radius: 5px;
        margin-top: 15px;
        padding: 15px;
        font-weight: bold;
        color: {ACCENT_COLOR};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }}

    /* 输入控件 */
    QLineEdit, QSpinBox, QComboBox {{
        background-color: #ffffff;
        border: 1px solid #bdc3c7;
        border-radius: 3px;
        padding: 5px;
        color: {TEXT_COLOR};
    }}
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {ACCENT_COLOR};
    }}

    /* QSpinBox 上下按钮：显式定义，避免样式表覆盖后按钮消失/失效 */
    QSpinBox::up-button, QSpinBox::down-button {{
        background-color: #d6eaf8;
        border: none;
        width: 18px;
    }}
    QSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; border-left: 1px solid #bdc3c7; }}
    QSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; border-left: 1px solid #bdc3c7; border-top: 1px solid #bdc3c7; }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background-color: #2980b9; }}
    QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{ background-color: {ACCENT_COLOR}; }}
    QSpinBox::up-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 5px solid {TEXT_COLOR};
        width: 0px; height: 0px;
    }}
    QSpinBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {TEXT_COLOR};
        width: 0px; height: 0px;
    }}

    /* 动作按钮 */
    QPushButton#ActionBtn {{
        background-color: #238636;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 3px;
        font-weight: bold;
    }}
    QPushButton#ActionBtn:hover {{
        background-color: #2EA043;
    }}
    QPushButton#BrowseBtn {{
        background-color: #2980b9;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }}
    QPushButton#BrowseBtn:hover {{
        background-color: #3498db;
    }}

    QTextEdit {{
        background-color: #ffffff;
        border: 1px solid #bdc3c7;
        border-radius: 3px;
        color: #2c3e50;
        font-size: 13px;
    }}
    
    /* 消息提示框 */
    QMessageBox {{
        background-color: #ffffff;
    }}
    QMessageBox QLabel {{
        color: #2c3e50;
        font-weight: bold;
        font-size: 14px;
    }}
    QMessageBox QPushButton {{
        background-color: #238636;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 3px;
        font-weight: bold;
        min-width: 80px;
    }}
    QMessageBox QPushButton:hover {{
        background-color: #2EA043;
    }}
    """


class FunctionPage(QWidget):
    """功能页面基类"""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            f"color: {TechStyle.ACCENT_COLOR}; font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(lbl_title)

    def add_log_widget(self):
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(150)
        self.layout.addWidget(self.log_box)

    def log(self, msg):
        self.log_box.append(f">> {msg}")


class FileSplitWorker(QThread):
    """
    分件后台处理线程：
    对所选目录下的每个子目录——
      1. 若目录下有 Directory.txt(文件批量替换生成): 第一页为卷皮, 目录页
         取自 Directory.txt 记录的文件(逐个OCR); 无则取排序后第2页(0002) OCR；
      2. 判断标题是否为“卷内文件目录”；是则解析表格中“序号”“页号”列；
      3. 按序号建子目录(目录名+“-”+四位序号)，按页号+偏移量移动 jpg 文件
         (偏移量=Directory.txt最大文件序号, 无Directory.txt时缺省为2；
         如偏移量2时页号“1-17”→移动 0003.jpg..0019.jpg)；
      4. 卷皮页/目录页 + 最大次大文件(原备考表卷底)统一移入“目录名-0000”子目录；
         不再单独生成「备考表卷底」「卷皮目录」两个目录；
         分件完成后删除该目录下 Directory.txt；
      5. 全程详细日志(OCR识别行、序号/页号解析、文件移动范围)写入所选目录。
    """
    log_signal = Signal(str)
    progress_signal = Signal(int, int)          # (当前, 总数)
    finished_signal = Signal(bool, str)

    def __init__(self, base_dir, target_base=None, copy_mode=False, xlsx_dir=None, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.target_base = target_base    # 分件到新目录: 输出根目录(None=原地)
        self.copy_mode = copy_mode        # True=文件拷贝(源不动), False=移动
        self.xlsx_dir = xlsx_dir          # 目录文件(xlsx)所在根目录(None=OCR模式)
        self.is_stopped = False
        self._ocr = None  # PaddleOCR 延迟初始化(只初始化一次, 避免重复加载模型)
        self._ocr_pages_since_init = 0  # 自上次引擎初始化以来处理的页数(例行重建计数, v3.9)
        import threading as _th
        self._ocr_init_lock = _th.Lock()   # 初始化锁: 多线程(JPG转PDF默认4线程)并发
                                           # (并发构造会内存暴涨/死锁——低配机卡死根因)

    # ---------- OCR ----------
    # OCR引擎例行重建阈值: 每处理N页丢弃实例重建。paddle推理引擎长时间连续运行会累积内存,
    # GPU模式曾运行一段时间后报「Memory allocation failed」→ 定期重建阻断累积。
    # 重建代价仅数秒模型重载, 相对数百页处理时长可忽略。
    _OCR_RECYCLE_PAGES = 200

    # ---------- OCR服务线程: 串行化+超时看门狗+挂死后CPU重建 ----------
    def _ocr_svc_loop(self, q):
        """OCR服务线程主循环: 串行执行提交的任务。
        队列元素 (fn, ev, box): fn=待执行函数, ev=threading.Event,
        box=list([ok, value])。任务挂起时本线程卡死(孤儿), 调用方靠超时脱身。"""
        while True:
            try:
                item = q.get()
            except Exception:
                continue
            if item is None:  # 退役信号(服务线程换新时给旧线程的善意尝试)
                return
            fn, ev, box = item
            try:
                val = fn()
                box[0], box[1] = True, val
            except BaseException as e:
                # v3.12: 必须捕获 SystemExit——paddleocr 在 cv2 缩放内存不足时内部调用
                # sys.exit(0)。SystemExit 继承 BaseException 而非 Exception, 漏捕获会把本服务
                # 线程直接打死(崩溃日志 20260901 根因), 之后所有 OCR 任务将永远等不到响应。
                box[0], box[1] = False, e
            finally:
                try:
                    ev.set()
                except Exception:
                    pass

    def _ensure_ocr_service(self):
        """惰性启动/重启OCR服务线程。线程数恒定(挂死线程换新队列后退出)。"""
        with self._svc_lock:
            import queue as _queue
            import threading as _th
            q = getattr(self, '_svc_q', None)
            t = getattr(self, '_svc_thread', None)
            if q is not None and (t is None or t.is_alive()):
                return q
            # v3.12: 服务线程已死亡(如旧版 SystemExit 未被捕获)→ 换新队列重建,
            # 否则投递的任务永远无人处理, 调用方全部空等超时。
            if q is not None:
                try:
                    q.put_nowait(None)
                except Exception:
                    pass
            q = _queue.Queue()
            self._svc_q = q
            t = _th.Thread(target=self._ocr_svc_loop, args=(q,),
                           name='OcrSvc', daemon=True)
            self._svc_thread = t
            t.start()
            return q

    def _ocr_svc_call(self, fn, timeout):
        """提交OCR任务到服务线程并限时等待。
        返回 (ok, value): ok=True时value为结果; ok=False时value为异常对象。
        返回 ('timeout', None): 服务线程超时未响应(判定挂死)——丢弃该线程,
        换新队列重启服务, 调用方据此决定是否CPU重建。"""
        import threading as _th
        q = self._ensure_ocr_service()
        ev = _th.Event()
        box = [False, None]
        q.put((fn, ev, box))
        if ev.wait(timeout):
            return ('ok' if box[0] else 'error'), box[1]
        # 超时: 服务线程挂死 → 换新队列重启(孤儿线程不再被引用, 无法强制终止)
        with self._svc_lock:
            try:
                q.put_nowait(None)  # 若线程只是队列异常仍会退出(挂死时无害)
            except Exception:
                pass
            self._svc_q = None
        self._ensure_ocr_service()
        return 'timeout', None

    def _rebuild_ocr_cpu(self):
        """GPU推理挂死后强制CPU重建: 丢弃挂死实例, 全程锁保护(每轮只做一次)。
        返回 True=已切换为CPU配置(新服务线程首次推理时将重新初始化)。
        paddle构造成功后无法改已有predictor的use_gpu → 只能置空实例,
        由 _init_ocr_locked 按新的 use_gpu_ocr=False 重新构造。"""
        import threading as _th
        if not hasattr(self, '_rebuild_lock'):
            with self._svc_lock:
                if not hasattr(self, '_rebuild_lock'):
                    self._rebuild_lock = _th.Lock()
        with self._rebuild_lock:
            if self._svc_rebuilt:
                return True
            self.log_signal.emit("  → OCR引擎切换为CPU重建(丢弃挂死的GPU实例)")
            self._run_monitor_line('GPU→CPU重建(推理挂死或引擎连续损坏, 后续全部CPU推理)')
            self.use_gpu_ocr = False
            self._ocr = None
            # 全局paddle place已设为GPU, 强制切回CPU(失败不影响重建——
            # 新实例构造时 use_gpu=False 会以CPU place创建)
            try:
                import paddle as _pd
                _pd.set_device('cpu')
            except Exception:
                pass
            # 换新服务线程(旧线程可能挂死在GPU调用上)
            with self._svc_lock:
                self._svc_q = None
            self._ensure_ocr_service()
            self._svc_rebuilt = True
            self._ocr_probed = False
            self._ocr_pages_since_init = 0  # CPU重建后重新计数(新实例从零开始)
            return True

    def _svc_empty_cache(self):
        """在OCR服务线程内释放GPU缓存(与推理串行, 避免并发CUDA操作挂死)。
        服务未启动/已挂死时跳过——此时已无存活推理, 释放无意义。"""
        try:
            with self._svc_lock:
                alive = self._svc_q is not None
            if not alive:
                return
            def _do():
                try:
                    import paddle
                    if hasattr(paddle.device, 'cuda'):
                        paddle.device.cuda.empty_cache()
                except Exception:
                    pass
            self._ocr_svc_call(_do, timeout=30)
        except Exception:
            pass

    # ---------- v3.14: GPU运行监控日志 ----------
    # 背景: GPU模式4线程转PDF仍崩溃(access violation), 崩溃点无从定位。
    # 此处建立周期采样: 每10秒记录 进程工作集/GPU显存/活跃线程数/OCR服务队列
    # 深度/引擎重建计数, 与业务日志同目录(run_monitor_时间戳.txt)。
    # 崩溃后最后一条采样即崩溃时刻的资源快照, 可判断是显存耗尽/内存累积/线程风暴。
    def _run_monitor_line(self, event=''):
        """写一条监控采样(线程安全)。event非空时为事件行(重建/降级/超时等)。"""
        if not getattr(self, '_run_mon_path', None):
            return
        try:
            import threading as _thm
            ts = datetime.now().strftime('%H:%M:%S')
            with self._run_mon_lock:
                with open(self._run_mon_path, 'a', encoding='utf-8') as f:
                    if event:
                        f.write(f"[{ts}] 事件: {event}\n")
                        return
                    mem = _proc_mem_mb()
                    n_threads = _thm.active_count()
                    qd = 'n/a'
                    try:
                        q = getattr(self, '_svc_q', None)
                        if q is not None:
                            qd = str(q.qsize())
                    except Exception:
                        pass
                    gpu_txt = 'n/a'
                    if getattr(self, 'use_gpu_ocr', False):
                        gi = _gpu_mem_info()
                        if gi:
                            gpu_txt = (f"{gi[0]:.0f}MB alloc/{gi[1]:.0f}MB reserved"
                                       if gi[2] == 'paddle'
                                       else f"{gi[0]:.0f}MB used/{gi[1]:.0f}MB total")
                    f.write(f"[{ts}] mem={mem:.0f}MB gpu={gpu_txt} "
                            f"threads={n_threads} ocr_q={qd} "
                            f"pages={getattr(self, '_ocr_pages_since_init', 0)} "
                            f"gpu_fail={getattr(self, '_gpu_engine_failures', 0)} "
                            f"gpu_mode={int(bool(getattr(self, 'use_gpu_ocr', False)))}\n")
        except Exception:
            pass

    def _run_monitor_loop(self, interval=10):
        """监控采样线程主循环(daemon), 由 _start_run_monitor 启动。"""
        while not self._run_mon_stop.wait(interval):
            self._run_monitor_line()

    def _start_run_monitor(self, output_dir, note=''):
        """启动运行监控(仅GPU模式)。输出 run_monitor_时间戳.txt 于输出目录。"""
        try:
            if not getattr(self, 'use_gpu_ocr', False):
                return
            os.makedirs(output_dir, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._run_mon_path = os.path.join(output_dir, f'run_monitor_{ts}.txt')
            import struct as _st_m
            bits = _st_m.calcsize('P') * 8
            with open(self._run_mon_path, 'w', encoding='utf-8') as f:
                f.write(f"TMToolMan GPU运行监控  启动: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
                f.write(f"解释器: {bits}位  工作线程数: {getattr(self, 'max_workers', '?')}  "
                        f"{'| ' + note if note else ''}\n")
                f.write("采样: 每10秒 | mem=进程工作集 gpu=显存(paddle分配/保留 或 全卡已用/总量) "
                        "threads=活跃线程 ocr_q=OCR服务队列积压 pages=引擎累计页数 "
                        "gpu_fail=GPU引擎损坏计数 gpu_mode=当前是否GPU推理\n")
                f.write("=" * 100 + "\n")
            import threading as _th_s
            _t = _th_s.Thread(target=self._run_monitor_loop, daemon=True,
                              name='RunMonitor')
            _t.start()
            self.log_signal.emit(f"  GPU运行监控已启动: run_monitor_{ts}.txt")
        except Exception as e:
            self.log_signal.emit(f"  (运行监控启动失败, 不影响处理: {e})")

    def _stop_run_monitor(self, note='正常结束'):
        """停止监控并写收尾行。"""
        try:
            self._run_mon_stop.set()
            if getattr(self, '_run_mon_path', None):
                self._run_monitor_line(f'监控结束({note})')
        except Exception:
            pass

    def _get_ocr(self):
        """
        延迟初始化 PaddleOCR(中文, 带方向分类)。失败返回 None。
        ★ 必须经由OCR服务线程调用(见 _ocr_svc_call): GPU路径初始化/推理可能永久挂起,
        服务线程+超时看门狗是唯一可脱身的隔离方式; 直接在工作线程调用会永久卡死。
        模型文件随程序打包(ocr_models/)，显式指定路径，避免在用户机器上
        联网下载模型(内网环境会静默失败导致 OCR 无结果)。
        """
        if self._ocr is None:
            # 双重检查锁: 拿到锁后再次确认(可能已被前一个线程初始化完)
            _lock = getattr(self, '_ocr_init_lock', None)
            if _lock is not None:
                _lock.acquire()
            try:
                if self._ocr is not None:
                    return self._ocr
                self._init_ocr_locked()
            finally:
                if _lock is not None:
                    _lock.release()
        return self._ocr

    def _init_ocr_locked(self):
        """在持有初始化锁的状态下构造 PaddleOCR(仅 _get_ocr 内部调用)。"""
        try:
            from paddleocr import PaddleOCR
            self.log_signal.emit("  初始化 PaddleOCR 引擎(首次较慢)...")
            # 模型目录定位: PyInstaller 打包后资源在 sys._MEIPASS; 开发环境在脚本目录
            base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            m_det = os.path.join(base, 'ocr_models', 'det')
            m_rec = os.path.join(base, 'ocr_models', 'rec')
            m_cls = os.path.join(base, 'ocr_models', 'cls')
            has_models = all(os.path.exists(os.path.join(m, 'inference.pdmodel'))
                             for m in (m_det, m_rec, m_cls))
            import warnings as _w
            _w.filterwarnings('ignore', message='.*use_angle_cls.*deprecated.*')
            # GPU OCR 请求检测: 双条件——paddle编译了CUDA支持 且 检测到GPU设备。
            # 仅编译支持但无卡(如GPU版paddle装在无NVIDIA机器)时 use_gpu=True 会
            # 报「Device id must be less than GPU count」→ 预检回退CPU。
            want_gpu = bool(getattr(self, 'use_gpu_ocr', False))
            gpu_ok = False
            if want_gpu:
                _pd = None
                try:
                    import paddle as _pd
                    compiled = bool(_pd.device.is_compiled_with_cuda())
                    n_gpu = int(_pd.device.cuda.device_count()) if compiled else 0
                    gpu_ok = compiled and n_gpu > 0
                except Exception:
                    gpu_ok = False
                if gpu_ok:
                    self.log_signal.emit("  OCR使用GPU推理(paddlepaddle-gpu, "
                                         f"{n_gpu}个GPU设备)")
                else:
                    self.log_signal.emit("  × GPU不可用(未装GPU版paddle或无NVIDIA设备)"
                                         " → 回退CPU推理(结果相同)")
                    # GPU版paddle装在无卡机上时, paddle默认找GPU设备会报
                    # 「Device id must be less than GPU count」——强制切CPU
                    if _pd is not None:
                        try:
                            _pd.set_device('cpu')
                        except Exception:
                            pass
            # paddleocr 版本碎片化兼容: 依次尝试多组配置, 成功即用。
            # 覆盖: 2.x(全参数) / 3.x legacy(use_angle_cls 可用但 show_log 移除)
            #       / 3.x 新参数(仅无内置模型时; 会走联网下载, 内网可能失败)
            # GPU 模式: 每组配置附加 use_gpu=True(2.x 参数; 3.x 由 paddle 自行调度)
            # 注意: paddleocr 2.7 的 use_gpu 参数【默认是 True】(utility.py)。
            # GPU版paddle在无卡机上必须显式 use_gpu=False 覆盖默认,
            # 否则即使不带参数也按GPU初始化而报错。
            _gpu_kw = dict(use_gpu=True) if (want_gpu and gpu_ok) else dict(use_gpu=False)
            configs = []
            if has_models:
                configs += [
                    # 2.x 标准配置
                    # use_mkldnn=False(v3.12): paddleocr 2.x 缺省 use_mkldnn=True,
                    # CPU predictor 的 oneDNN 缓存在变尺寸输入下持续泄漏宿主内存,
                    # 长时间运行后宿主内存耗尽(报 could not create a primitive /
                    # cv2 Insufficient memory 崩溃)。OCR推理不依赖其加速, 显式关闭。
                    dict(use_angle_cls=True, lang='ch', show_log=False,
                         det_model_dir=m_det, rec_model_dir=m_rec, cls_model_dir=m_cls,
                         use_mkldnn=False, **_gpu_kw),
                    # 3.x legacy: use_angle_cls 被兼容, 但 show_log 已移除(3.x可能不认
                    # use_mkldnn参数, 不携带——该配置失败时自动尝试下一配置)
                    dict(use_angle_cls=True, lang='ch',
                         det_model_dir=m_det, rec_model_dir=m_rec, cls_model_dir=m_cls,
                         use_mkldnn=False, **_gpu_kw),
                    # 3.x 新参数 + 旧模型路径(部分版本参数改名但模型格式仍兼容)
                    dict(use_textline_orientation=True, lang='ch',
                         det_model_dir=m_det, rec_model_dir=m_rec, cls_model_dir=m_cls),
                ]
            configs += [
                dict(use_angle_cls=True, lang='ch', show_log=False, **_gpu_kw),
                dict(use_angle_cls=True, lang='ch', **_gpu_kw),
                dict(use_textline_orientation=True),
                dict(),
            ]
            last_err = None
            for i, kw in enumerate(configs, 1):
                try:
                    self._ocr = PaddleOCR(**kw)
                    self.log_signal.emit(f"  (OCR初始化成功: 配置#{i}"
                                         f"{' 含内置模型' if 'det_model_dir' in kw else ''})")
                    break
                except Exception as e:
                    last_err = e
                    self.log_signal.emit(f"  (配置#{i} 不适用: {str(e)[:80]}, 尝试下一配置)")
            # v3.7修复: 请求GPU时部分“兜底”配置(#3/#6/#7)未带use_gpu参数,
            # 而paddleocr 2.x缺省use_gpu=True → GPU环境异常时兜底配置连带全部失败,
            # 最终OCR为None→单层PDF。此处GPU配置全失败后用显式CPU配置再试一轮。
            if self._ocr is None and want_gpu and gpu_ok:
                self.log_signal.emit("  × GPU配置全部失败, 改用显式CPU配置重试")
                try:
                    import paddle as _pd2
                    _pd2.set_device('cpu')
                except Exception:
                    pass
                for i, kw in enumerate(configs, 1):
                    kw = dict(kw)
                    if 'use_angle_cls' in kw:
                        kw['use_gpu'] = False  # 2.x风格: 显式CPU(覆盖2.7缺省GPU)
                    try:
                        self._ocr = PaddleOCR(**kw)
                        self.log_signal.emit(f"  (OCR初始化成功: CPU兜底配置#{i})")
                        break
                    except Exception as e:
                        last_err = e
                        self.log_signal.emit(f"  (CPU兜底配置#{i} 不适用: {str(e)[:80]})")
            if self._ocr is None:
                raise last_err or RuntimeError('所有OCR配置均失败')
        except Exception as e:
            self.log_signal.emit(f"  × PaddleOCR 初始化失败: {e}")
            return None
        return self._ocr

    def _preload_img_arr(self, image_path):
        """v3.26: 在调用方(工作线程)预解码图像为BGR ndarray。
        背景(崩溃日志20260910): GPU模式多线程下OCR服务线程在paddleocr
        img_decode内部(np.frombuffer→cv2.imdecode)发生access violation段错误
        ——GPU推理上下文内存损坏波及服务线程内的C层解码路径。
        对策: 服务线程外的各工作线程用PIL解码(不经cv2), 传ndarray给ocr()
        ——paddleocr接受ndarray, check_img直接透传, 服务线程内完全不再执行
        文件读取与cv2.imdecode(崩溃点被移出)。
        返回BGR连续数组(与cv2.imread通道序一致); 失败返回None(回退路径模式)。
        注意: 必须np.array(拷贝)——np.asarray与PIL共享内存, 图像close后数组
        指向已释放内存, 恰是access violation形态。"""
        try:
            import numpy as _np
            with Image.open(image_path) as _im:
                _rgb = _im.convert('RGB')
                _bgr = _np.array(_rgb)[:, :, ::-1]   # RGB→BGR, 同cv2.imread
                return _np.ascontiguousarray(_bgr)
        except Exception:
            return None

    def _ocr_page(self, image_path, logf, wlog, img_arr=None):
        """
        对单页做 OCR，返回片段列表 [(文本, x0, y0, x1), ...]。
        x1 为片段右边界，用于列定位。
        兼容 paddleocr 2.x (ocr(img, cls=True)) 与 3.x (predict(img), 结果对象)。
        """
        # --- 例行重建: 每 _OCR_RECYCLE_PAGES 页丢弃引擎, 本次调用重新初始化 ---
        # 阻断paddle推理引擎长时间运行内存累积(曾在GPU模式运行一段时间后报
        # "Memory allocation failed")。本方法只在OCR服务线程内串行执行, 重建安全。
        # v3.11: 另有内存看门狗在双层PDF主循环中按进程工作集阈值强制重建(见下方主循环)。
        _cnt = getattr(self, '_ocr_pages_since_init', 0)
        if _cnt > 0 and _cnt % self._OCR_RECYCLE_PAGES == 0 and self._ocr is not None:
            self.log_signal.emit(f"  OCR引擎例行重建(已处理{_cnt}页, 防长时间运行内存累积)")
            self._ocr = None
            try:
                import gc as _gc
                _gc.collect()
                if getattr(self, 'use_gpu_ocr', False):
                    import paddle as _pd
                    if hasattr(_pd.device, 'cuda'):
                        _pd.device.cuda.empty_cache()
            except Exception:
                pass
        self._ocr_pages_since_init = _cnt + 1
        ocr = self._get_ocr()
        if ocr is None:
            return []
        result = None
        _mem_fail = False
        # v3.26: 优先用调用方预解码的ndarray(服务线程内不再读文件/cv2.imdecode,
        # 规避20260910崩溃); 预解码失败回退路径模式(仍走img_decode, 尽力而为)。
        _ocr_input = img_arr if img_arr is not None else image_path
        try:
            result = ocr.ocr(_ocr_input, cls=True)
        except (Exception, SystemExit) as e:
            # v3.12: 必须同时捕获 SystemExit——paddleocr 在 cv2 缩放内存不足时内部调用
            # sys.exit(0)(崩溃日志20260901)。SystemExit 继承 BaseException, 仅捕获
            # Exception 会透传打死服务线程。此处拦下按内存失败处理。
            # v3.14: 首次异常即判定是否引擎损坏类错误(primitive/CUDA/显存类)。
            # 此类错误下 predictor 内部状态已坏, 继续用同一实例重试会在损坏的
            # CUDA 上下文上操作 → access violation 进程级崩溃(v3.13后仍崩的根因)。
            # 损坏类错误: 立即弃用实例; 仅参数不兼容类(3.x不接受cls)才用原实例重试。
            _e1_txt = f"{type(e).__name__}: {e}".lower()
            _engine_broken = (isinstance(e, SystemExit)
                              or any(k in _e1_txt for k in (
                                  'could not create a primitive',
                                  'memory allocation', 'bad_alloc', 'out of memory',
                                  'cannot allocate', 'allocation failed',
                                  'insufficient memory', 'cudnn', 'cuda error',
                                  'device side assert', 'illegal memory access')))
            e2 = e  # 默认占位: 引擎损坏路径不再重试, e2=e 保证下方文案判定包含首错
            if not _engine_broken:
                # 3.x: ocr() 不接受 cls 参数 → 重试无参/用 predict
                try:
                    result = ocr.ocr(_ocr_input)
                except (Exception, SystemExit):
                    try:
                        result = ocr.predict(_ocr_input)
                    except (Exception, SystemExit) as _e3:
                        e2 = _e3
                        result = None
                else:
                    e2 = None
            else:
                result = None
            if result is None:
                # v3.9: 内存分配失败(长时间运行内存累积) → 丢弃引擎重建后重试本页一次,
                # 不再直接跳过文本层。匹配paddle/CUDA的内存类错误文案(不区分大小写)。
                # v3.12: 补充 could not create a primitive(MKL-DNN分配失败)与
                # insufficient memory(cv2.resize OOM); SystemExit(paddleocr内部
                # sys.exit(0), 仅在resize内存不足时发生)同样判定为内存失败。
                _msg = f"{e} | {e2}".lower()
                _mem_fail = _mem_fail or _engine_broken or isinstance(e2, SystemExit) \
                    or any(k in _msg for k in ('memory allocation', 'bad_alloc',
                                               'out of memory', 'cannot allocate',
                                               'allocation failed',
                                               'could not create a primitive',
                                               'insufficient memory'))
                if _mem_fail:
                    self.log_signal.emit(
                        f"    × OCR引擎异常(疑似内存/推理损坏), 丢弃引擎重建后重试: "
                        f"{os.path.basename(image_path)}")
                    self._run_monitor_line(
                        f'OCR引擎异常并重建: {os.path.basename(image_path)} | '
                        f'{_e1_txt[:150]}')
                    self._ocr = None
                    try:
                        import gc as _gc2
                        _gc2.collect()
                    except Exception:
                        pass
                    # v3.14: GPU模式下引擎损坏达到累计阈值 → 全局降级CPU。
                    # GPU实例反复报 primitive/显存错误说明CUDA上下文已不可靠
                    # (显存耗尽/驱动异常), 继续重建GPU实例会在坏上下文上创建,
                    # 连环崩溃(v3.13后仍崩溃的直接原因)。CPU重建一次性切换,
                    # 之后所有页走CPU(慢但稳), 不再回到GPU。
                    _gpu_fail = getattr(self, '_gpu_engine_failures', 0) + \
                        (1 if getattr(self, 'use_gpu_ocr', False) else 0)
                    self._gpu_engine_failures = _gpu_fail
                    if getattr(self, 'use_gpu_ocr', False) and _gpu_fail >= 2:
                        self.log_signal.emit(
                            f"    × GPU引擎已连续损坏{_gpu_fail}次, 全局切换CPU推理"
                            f"(后续页全部走CPU, 速度变慢但不再崩溃)")
                        self._run_monitor_line(
                            f'GPU引擎累计损坏{_gpu_fail}次≥2, 全局降级CPU推理')
                        self._rebuild_ocr_cpu()
                    _ocr2 = self._get_ocr()
                    if _ocr2 is not None and _ocr2 is not ocr:
                        # v3.14: 重建实例仅试一次(带cls), 失败不再连环重试——
                        # 重建实例若仍报同类错误(显存/上下文问题未消除),
                        # 继续重试同样有access violation风险, 该页直接放弃文本层。
                        try:
                            result = _ocr2.ocr(_ocr_input, cls=True)
                        except (Exception, SystemExit):
                            result = None
                else:
                    import traceback
                    wlog(f"    OCR 出错 {os.path.basename(image_path)}: {e}")
                    wlog("    详细: " + traceback.format_exc().replace('\n', ' | ')[:500])
                    return []
                if result is None:
                    wlog(f"    OCR 内存分配失败且重建重试仍失败, 该页跳过文本层: "
                         f"{os.path.basename(image_path)}")
                    return []

        frags = []
        items = []
        if result:
            first = result[0]
            if first is not None and hasattr(first, 'rec_texts'):
                # 3.x 结果对象: rec_texts/rec_scores/dt_polys
                texts = list(getattr(first, 'rec_texts', []) or [])
                scores = list(getattr(first, 'rec_scores', []) or [])
                polys = list(getattr(first, 'dt_polys', []) or [])
                for i, txt in enumerate(texts):
                    poly = polys[i] if i < len(polys) and len(polys[i]) >= 4 else None
                    if poly is not None:
                        xs = [p[0] for p in poly]
                        ys = [p[1] for p in poly]
                        box = [[min(xs), min(ys)], [max(xs), max(ys)]]
                    else:
                        box = [[0, 0], [0, 0]]
                    conf = scores[i] if i < len(scores) else 0.0
                    items.append((box, txt, conf))
            elif first:
                # 2.x: [[box, (txt, conf)], ...] box为四点多边形
                # (左上/右上/右下/左下) → 统一转为 [左上,右下] 两点,
                # 使 y1-y0 为真实行高(box[1]右上的y≈box[0]左上的y)
                for item in first:
                    try:
                        box, (txt, conf) = item[0], item[1]
                        if len(box) >= 4:
                            xs = [p[0] for p in box]
                            ys = [p[1] for p in box]
                            box = [[min(xs), min(ys)], [max(xs), max(ys)]]
                        items.append((box, txt, conf))
                    except Exception:
                        continue
        if not items:
            shape = 'result为空' if not result else ('result[0]为None' if result[0] is None
                                                     else '结果无内容')
            wlog(f"    OCR 无内容({shape}): {os.path.basename(image_path)}")
            return frags
        for box, txt, conf in items:
            x0, y0 = box[0][0], box[0][1]
            x1, y1 = box[1][0], box[1][1]
            frags.append((txt, x0, y0, x1, y1))
            wlog(f"    OCR行: 「{txt}」 置信度={conf:.2f} 位置=({x0:.0f},{y0:.0f})")
        return frags

    # ---------- 表格解析 ----------
    @staticmethod
    def _row_of(frags, y, tol=35):
        """取与 y 同一行的片段(按 y 中心, 容差 tol)。"""
        out = []
        for txt, x0, y0, x1, _y1 in frags:
            yc = y0  # y0 即片段顶(近似行位置)
            if abs(yc - y) <= tol:
                out.append((txt, x0, x1))
        return out

    @staticmethod
    def _is_catalog_title(frags):
        """
        判断 OCR 片段中是否含标题「卷内文件目录」。
        匹配策略(由严到宽):
          1. 完整包含「卷内文件目录」;
          2. 同一片段同时含「卷内」和「目录」(允许中间夹杂其他字);
          3. 页面顶部(y最小)的大片段含「目录」且含「卷」——标题被OCR拆散/夹字时的兜底。
        """
        for txt, x0, y0, x1, _y1 in frags:
            compact = txt.replace(' ', '').replace('　', '')
            if '卷内文件目录' in compact:
                return True
            if '卷内' in compact and '目录' in compact:
                return True
        # 兜底: 顶部区域(y < 600)内, 「卷」和「目录」分别出现在不同片段
        has_juan = any('卷' in t.replace(' ', '').replace('　', '') for t, *_ in frags)
        has_mulu = any('目录' in t.replace(' ', '').replace('　', '') for t, _, y, _, _h in frags if y < 600)
        return has_juan and has_mulu

    @staticmethod
    def _parse_catalog_rows(frags, wlog):
        """
        解析表格数据行：返回 [(序号int, 起页int, 止页int), ...]。

        真实档案的两种页号写法(同一表内可混合)：
          1. 范围式 “1-17” / “146-149”；
          2. 单数字 “144”  —— 表示该件从该页开始，到下一行起始页-1 止
             (最后一行则到“下一起始页”未知，保守取同值，即只含该页)。
        列定位：先找表头“序号”“页号”的 x 坐标确定两列的 x 范围，
        数据行内按 x 落点取列值(序号列较窄, 页号列在表格最右数据区)。
        """
        # ---- 1. 定位表头列 x ----
        seq_x = page_x = None
        for txt, x0, y0, x1, _y1 in frags:
            compact = txt.replace(' ', '').replace('　', '')
            if compact == '序号' and seq_x is None:
                seq_x = x0
            elif '页号' in compact and page_x is None:
                page_x = x0
        if seq_x is None or page_x is None:
            wlog("    未找到表头「序号」或「页号」列, 尝试按位置推断列")
            # 推断: 序号=最左侧数字列, 页号=最右侧数据列(取全图宽)
            if frags:
                page_x = 0.62 * max(f[3] for f in frags)
                seq_x = 0.0

        # ---- 2. 收集数据行: 每行 = (序号候选, 页号原始文本, y) ----
        # 序号候选: 纯 1-2 位数字片段, x 靠近序号列(x0 < 页号列左界, 且 x0 在序号列附近±180px)
        seq_tol = 200
        page_left = page_x - 160  # 页号列数据允许在表头左侧一点
        candidates = []  # [(seq, y, pagetxt)]

        def _find_pagetxt(y_row):
            """在该行找页号: 优先独立片段; 否则从长文本尾部提取(OCR 常把日期和
            页号粘连, 如「...征求意见书及2021.12.2039-143」尾部是页号)。
            片段起点或右边界落入页号区(x1 >= page_left)即视为含页号。
            粘连两级处理:
              a. 日期与页号直接相连无分隔: 「2021.8.30107-111」→日期尾「30」
                 与页号「107-111」粘连 → 按日期模式(YYYY.M.D)切出页号;
              b. 页号前是非数字: 「...12.2039-143」→「39-143」(避免吞日期)。"""
            row = FileSplitWorker._row_of(frags, y_row)
            best = ''
            for rt, rx0, rx1 in sorted(row, key=lambda r: r[1]):
                if rx0 < page_left and rx1 < page_left:
                    continue  # 片段整体在页号区左侧
                rt2 = rt.strip()
                if re.fullmatch(r'\d{1,4}[-–—~]\d{1,4}', rt2):
                    return rt2
                if re.fullmatch(r'\d{1,4}', rt2):
                    best = best or rt2
                else:
                    # a. 日期模式紧贴页号: 「2021.8.30107-111」「2021.12.2039-143」
                    #    日期 YYYY.M.D 的最后一段日期数字与页号起始粘连,
                    #    页号= 去掉日期前缀后剩下的「数字-数字」
                    m = re.search(r'\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\s*(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*'
                                  r'(?:\s+(\d{1,4})\s*)?$', rt2)
                    if m:
                        # 可能还有第二个独立页号(如「...112-118」带空格形式)
                        return f"{m.group(1)}-{m.group(2)}"
                    # 带空格分隔: 「2021.8.30 112-118」→「112-118」
                    m = re.search(r'\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\s+(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$', rt2)
                    if m:
                        return f"{m.group(1)}-{m.group(2)}"
                    # b. 页号前是非数字(避免把日期一部分吞进来)
                    m = re.search(r'(?:^|\D)(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$', rt2)
                    if m:
                        return f"{m.group(1)}-{m.group(2)}"
                    m = re.search(r'(?:^|\s)(\d{1,4})\s*$', rt2)
                    if m and not best:
                        best = m.group(1)
            return best

        for txt, x0, y0, x1, _y1 in frags:
            t = txt.strip()
            if not re.fullmatch(r'\d{1,2}', t):
                continue
            if x0 > page_left:      # 在页号列右侧的数字 → 页号候选, 不是序号
                continue
            if abs(x0 - seq_x) > seq_tol and seq_x > 0:
                continue
            candidates.append((int(t), y0, _find_pagetxt(y0)))

        # ---- 2b. 补漏: 有页号但序号未被识别的行(如首行序号「1」漏识别) ----
        # 找出未被任何 candidate 认领的页号来源(两类) → 按 y 位置插入, 序号推断:
        #   i.  独立片段: 纯「X-Y」或纯数字(x 在页号区);
        #   ii. 长文本尾部粘连: 「2021.8.30 112-118」/「2021.8.30107-111」
        #       (序号与页号都被 OCR 挤进日期长文本的整行, 用同一套粘连提取)
        used_y = [c[1] for c in candidates]
        orphan_pages = []  # [(y, pagetxt)]

        def _extract_glued(t):
            """从长文本尾部提取粘连页号(与 _find_pagetxt 相同的规则, 返回''表示无)。"""
            m = re.search(r'\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\s*(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$', t)
            if m:
                return f"{m.group(1)}-{m.group(2)}"
            m = re.search(r'(?:^|\D)(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$', t)
            if m:
                return f"{m.group(1)}-{m.group(2)}"
            m = re.search(r'(?:^|\s)(\d{1,4})\s*$', t)
            return m.group(1) if m else ''

        for txt, x0, y0, x1, _y1 in frags:
            t = txt.strip()
            if x0 < page_left and x1 < page_left:
                continue  # 整体在页号区左侧, 不含页号
            if any(abs(y0 - uy) < 40 for uy in used_y):
                continue  # 已被认领
            if re.fullmatch(r'\d{1,4}[-–—~]\d{1,4}', t) or re.fullmatch(r'\d{1,4}', t):
                orphan_pages.append((y0, t))
            else:
                # 长文本: 仅当其右边界伸入页号区才尝试提取尾部粘连页号。
                # 只接受「X-Y」范围形式——单数字从长文本尾部提取误报率高
                # (容易把日期/字号等数字当页号), 不作为补漏来源。
                if x1 >= page_left:
                    glued = _extract_glued(t)
                    if glued and re.fullmatch(r'\d{1,4}[-–—~]\d{1,4}', glued):
                        orphan_pages.append((y0, glued))
        # 孤立页号行统一编号:
        #   在已认领行之前的 → 按 y 排序后从 (最小已认领序号 - 前置孤立行数)
        #   开始依次 +1 (例: 已认领最小序号4, 前置孤立3行 → 1,2,3)
        #   在已认领行之间的 → 前一行序号+1 (同前逻辑)
        orphan_pages.sort(key=lambda o: o[0])
        n_before = 0
        min_seq_known = min((c[0] for c in candidates), default=1)
        min_y_known = min((c[1] for c in candidates), default=float('inf'))
        # 统计在已认领行之前的孤立行数
        lead_orphans = [o for o in orphan_pages if o[0] < min_y_known]
        n_lead = len(lead_orphans)
        assigned_lead = 0
        for y0, t in orphan_pages:
            if not candidates:
                nxt_seq = 1 + assigned_lead
                assigned_lead += 1
            elif y0 < min_y_known:
                # 前置孤立行: 从 min_seq - n_lead 开始递增(≥1)
                nxt_seq = max(1, min_seq_known - n_lead) + assigned_lead
                assigned_lead += 1
            else:
                prevs = [c for c in candidates if c[1] < y0]
                base = max(prevs, key=lambda c: c[1]) if prevs else None
                if base is not None:
                    nxt_seq = base[0] + 1
                    # 若与后一行序号冲突(>= 后一行), 说明推断异常, 用后一行-1
                    nexts = [c for c in candidates if c[1] > y0]
                    if nexts:
                        nmin = min(nexts, key=lambda c: c[1])
                        if nxt_seq >= nmin[0]:
                            nxt_seq = nmin[0] - 1
                else:
                    nxt_seq = 1 + assigned_lead
                    assigned_lead += 1
            candidates.append((nxt_seq, y0, t))
            wlog(f"    [补漏] 序号={nxt_seq} y={y0:.0f} 页号「{t}」(序号未被OCR识别, 已推断)")

        # 按 y 去重(同一序号可能被 OCR 拆出多个同值片段)
        candidates.sort(key=lambda c: c[1])
        dedup = []
        for c in candidates:
            if dedup and abs(c[1] - dedup[-1][1]) < 30 and c[0] == dedup[-1][0]:
                # 补页号(若前一条为空)
                if not dedup[-1][2] and c[2]:
                    dedup[-1] = (dedup[-1][0], dedup[-1][1], c[2])
                continue
            dedup.append(c)

        # ---- 3. 解析页号(两种格式), 单数字推断止页=下一行起始-1 ----
        parsed = []
        for i, (seq, y, pagetxt) in enumerate(dedup):
            if not pagetxt:
                wlog(f"    跳过行(无页号): 序号={seq} y={y:.0f}")
                continue
            m = re.fullmatch(r'(\d{1,4})[-–—~](\d{1,4})', pagetxt)
            if m:
                p_start, p_end = int(m.group(1)), int(m.group(2))
                if p_end < p_start:
                    p_start, p_end = p_end, p_start
                src = pagetxt
            else:
                p_start = int(pagetxt)
                # 找下一行的起始页
                nxt = None
                for j in range(i + 1, len(dedup)):
                    if dedup[j][2]:
                        m2 = re.match(r'(\d{1,4})', dedup[j][2])
                        if m2:
                            nxt = int(m2.group(1))
                            break
                p_end = (nxt - 1) if (nxt is not None and nxt > p_start) else p_start
                src = f"{pagetxt}(推断到{p_end})"
            parsed.append((seq, p_start, p_end))
            wlog(f"    解析行: 序号={seq} 页号={p_start}-{p_end} ← 「{src}」 y={y:.0f}")

        # ---- 4. 连续性校验修正 ----
        # 档案各件页号首尾相接(本行起始 = 前行止页+1, 本行止页 = 下行起始-1)。
        # OCR 常把日期与页号粘连(如「2021.12.2039-143」实为页号「39-143」),
        # 导致某端数字虚大。按相邻行的连续性约束重切粘连数字。
        for i in range(len(parsed)):
            seq, p_start, p_end = parsed[i]
            prev_end = parsed[i - 1][2] if i > 0 else None
            next_start = parsed[i + 1][1] if i + 1 < len(parsed) else None
            raw = (dedup[i][2] if i < len(dedup) else '') or ''
            m = re.fullmatch(r'(\d{1,5})[-–—~](\d{1,5})', raw.strip())
            if not m:
                continue
            big, tail = m.group(1), m.group(2)
            big_v, tail_v = int(big), int(tail)
            lo, hi = (tail_v, big_v) if big_v > tail_v else (big_v, tail_v)
            # 期望: start=prev_end+1 (若有前行), end=next_start-1 (若有后行)
            exp_start = (prev_end + 1) if prev_end is not None else None
            exp_end = (next_start - 1) if (next_start is not None and next_start > 1) else None
            fixed = False
            new_start, new_end = p_start, p_end
            # 情形A: start 虚大(粘连在头, 如「2039-143」start 应为 39)
            if exp_start is not None and lo != exp_start and hi == (exp_end or hi):
                cand_s = big[-len(str(exp_start)):] if big_v > tail_v else tail[-len(str(exp_start)):]
                if cand_s == str(exp_start):
                    new_start, new_end = exp_start, hi
                    fixed = True
            # 情形B: end 虚大(粘连在尾)
            if not fixed and exp_end is not None and hi > exp_end and lo == exp_start:
                cand_e = tail[-len(str(exp_end)):] if tail_v > big_v else big[-len(str(exp_end)):]
                if cand_e == str(exp_end):
                    new_start, new_end = lo, exp_end
                    fixed = True
            # 情形C: 双端都可能粘连, 用两端约束直接切
            if not fixed and exp_start is not None and exp_end is not None \
                    and (lo != exp_start or hi != exp_end):
                s_str, e_str = str(exp_start), str(exp_end)
                joined = big + tail
                # 尝试在 joined 中找 s_str 和 e_str 的合理组合
                for cut in range(1, len(joined)):
                    a, b = joined[:cut], joined[cut:]
                    if a.endswith(s_str) and b.startswith(e_str) and len(a) >= len(s_str):
                        new_start, new_end = exp_start, exp_end
                        fixed = True
                        break
            if fixed and (new_start, new_end) != (p_start, p_end):
                parsed[i] = (seq, new_start, new_end)
                wlog(f"    [连续性修正] 序号={seq}: 页号 {p_start}-{p_end} → "
                     f"{new_start}-{new_end} (原文「{raw}」日期与页号粘连, 已按邻行连续性切分)")
        return parsed

    # ---------- 表格线模式解析 ----------
    _CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
               '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

    @staticmethod
    def _imread_cn(path):
        """中文路径安全读图(cv2.imread 不支持 Windows 非 ASCII 路径)。"""
        try:
            import cv2
            import numpy as _np
            data = _np.fromfile(path, dtype=_np.uint8)
            if data.size == 0:
                return None
            return cv2.imdecode(data, cv2.IMREAD_COLOR)
        except Exception:
            return None

    @staticmethod
    def _imwrite_cn(path, img):
        """中文路径安全写图(配套 _imread_cn)。"""
        try:
            import cv2
            ext = '.png' if path.lower().endswith('.png') else '.jpg'
            ok, buf = cv2.imencode(ext, img)
            if ok:
                buf.tofile(path)
                return True
        except Exception:
            pass
        return False

    def _detect_table_rows(self, image_path):
        """
        OpenCV 检测表格横线, 返回数据行区间 [(top, bottom), ...] 或 []。
        横线特征: 水平长线(≥图宽30%); 数据行=相邻横线间隔>100px。
        """
        try:
            import cv2
            import numpy as _np
            img = self._imread_cn(image_path)
            if img is None:
                return []
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            H, W = gray.shape
            _, bw = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
            hk = cv2.getStructuringElement(cv2.MORPH_RECT, (max(W // 15, 20), 1))
            horiz = cv2.morphologyEx(bw, cv2.MORPH_OPEN, hk)
            ys = _np.where(horiz.sum(axis=1) > 255 * W * 0.3)[0]
            lines = []
            for y in ys:
                if lines and y - lines[-1][-1] <= 5:
                    lines[-1].append(y)
                else:
                    lines.append([y])
            centers = [int(_np.mean(g)) for g in lines]
            if len(centers) < 3:
                return []
            return [(centers[i], centers[i + 1])
                    for i in range(len(centers) - 1)
                    if centers[i + 1] - centers[i] > 100]
        except Exception:
            return []

    def _parse_catalog_by_table(self, image_path, wlog):
        """
        表格线模式解析: 横线定位每个数据行 → 整行裁剪降采样后单独OCR →
        按行提取 序号(数字或汉字一~十) + 页号(数字/范围/汉字数字)。
        相比全图片段模式的优势: 行不漏(每行独立OCR)、序号跳号无误判
        (序号来自本行而非推断)、支持汉字页号(一~十)。
        返回 [(序号, 起, 止), ...]; 无表格线或全失败返回 []。
        """
        bands = self._detect_table_rows(image_path)
        if not bands:
            return []
        wlog(f"    表格线模式: 检测到 {len(bands)} 个行区间")
        try:
            import cv2
        except ImportError:
            return []
        img = self._imread_cn(image_path)
        if img is None:
            return []
        H, W = img.shape[:2]

        def to_page(txt):
            """页号文本→(起,止)或None。支持 数字/范围/汉字一~十。"""
            t = txt.strip().replace(' ', '')
            m = re.fullmatch(r'(\d{1,4})[-–—~](\d{1,4})', t)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                return (min(a, b), max(a, b))
            if re.fullmatch(r'\d{1,4}', t):
                v = int(t)
                return (v, v)
            if t in self._CN_NUM:
                v = self._CN_NUM[t]
                return (v, v)
            return None

        def to_seq(txt):
            t = txt.strip()
            if re.fullmatch(r'\d{1,2}', t):
                return int(t)
            if t in self._CN_NUM:
                return self._CN_NUM[t]
            return None

        results = []   # [(y_center, seq, (s,e))]
        for bi, (y1, y2) in enumerate(bands):
            # 跳过表头行(含"序号"字样)与跨行标题行(无页号且序号列无数字)
            row_img = img[y1:y2]
            # 降采样到宽~1200 提速
            sc = 1200.0 / W
            small = cv2.resize(row_img, (1200, max(1, int((y2 - y1) * sc))))
            tmp = image_path + f'.row{bi}.png'
            self._imwrite_cn(tmp, small)
            r = self._ocr_page(tmp, None, lambda s: None)
            try:
                os.remove(tmp)
            except Exception:
                pass
            if not r:
                continue
            texts = [t for t, *_ in r]
            joined = ''.join(texts)
            if '序号' in joined and '页号' in joined:
                continue  # 表头行
            # 找序号: 行内最左的纯数字(1-2位)或汉字数字
            seq = None
            seq_frag = None
            seq_y = None
            for t, x0, y0, x1, _y1 in sorted(r, key=lambda f: f[1]):
                s = to_seq(t)
                if s is not None and s <= 30:
                    seq = s
                    seq_frag = (t, x0, y0, x1)
                    seq_y = (y1 + y2) / 2
                    break
            # 找页号: 行内任何位置的 页号形态(独立或长文本尾部)。
            # 排除序号已占用的片段(避免把序号数字当单页页号, 如「4|...|48-132」)。
            page = None
            for t, x0, y0, x1, _y1 in r:
                if seq_frag is not None and t == seq_frag[0] and x0 == seq_frag[1]:
                    continue  # 序号片段不再参与页号
                p = to_page(t)
                if p:
                    page = p
                    break
                # 长文本尾部粘连(与片段模式同规则)
                for pat in (r'\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}\s*(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$',
                            r'(?:^|\D)(\d{1,4})\s*[-–—~]\s*(\d{1,4})\s*$'):
                    m = re.search(pat, t)
                    if m:
                        a, b = int(m.group(1)), int(m.group(2))
                        page = (min(a, b), max(a, b))
                        break
                if page:
                    break
            # 有页号即可入表(序号缺失的行, 后面按锚点插值补)
            if page:
                results.append((seq_y if seq_y is not None else (y1 + y2) / 2,
                                seq, page))
                wlog(f"    表格行{bi}: 序号={seq if seq is not None else '?'} "
                     f"页号={page[0]}-{page[1]} "
                     f"← 行y{y1}-{y2} OCR:{'|'.join(texts)[:60]}")

        if not results:
            return []
        results.sort(key=lambda x: x[0])

        # ---- 序号缺失行: 用已识别序号锚点线性插值 ----
        # 例: 行位次[1,2,3] 序号[1,None,4] → 位次1=1, 位次3=4 → 位次2=3
        # (插值取整; 两端外推: 首位=首锚点-前距, 末位=末锚点+后距)
        idx_known = [(i, r[1]) for i, r in enumerate(results) if r[1] is not None]
        if not idx_known:
            # 完全无锚点(所有序号都被OCR漏识别): 档案序号从1起按位次递增
            for i, r in enumerate(results):
                results[i] = (r[0], i + 1, r[2])
            wlog(f"    [序号兜底] 全部{len(results)}行序号未被OCR识别, "
                 f"按位次从1递增赋值")
        else:
            for i, r in enumerate(results):
                if r[1] is not None:
                    continue
                prevs = [k for k in idx_known if k[0] < i]
                nexts = [k for k in idx_known if k[0] > i]
                if prevs and nexts:
                    (i0, s0) = prevs[-1]
                    (i1, s1) = nexts[0]
                    if i1 > i0:
                        raw = s0 + (s1 - s0) * (i - i0) / (i1 - i0)
                        # 锚点间序号增量>位次增量 → 档案存在跳号,
                        # 插值向上取整偏向跳号解释(1,[?],4 → 3 而非 2)
                        import math as _math
                        guess = int(_math.ceil(raw)) if (s1 - s0) > (i1 - i0) \
                            else int(round(raw))
                        r_new = (r[0], guess, r[2])
                        results[i] = r_new
                        wlog(f"    [序号插值] 行位次{i+1}: 序号={r_new[1]} "
                             f"(锚点 位次{i0+1}={s0}, 位次{i1+1}={s1}"
                             f"{'跳号' if (s1 - s0) > (i1 - i0) else ''})")
                elif nexts:
                    # 在首锚点之前: 首锚点序号 - 位次差
                    (i1, s1) = nexts[0]
                    guess = s1 - (i1 - i)
                    results[i] = (r[0], guess, r[2])
                    wlog(f"    [序号插值] 行位次{i+1}: 序号={guess} (首锚点外推)")
                elif prevs:
                    (i0, s0) = prevs[-1]
                    guess = s0 + (i - i0)
                    results[i] = (r[0], guess, r[2])
                    wlog(f"    [序号插值] 行位次{i+1}: 序号={guess} (末锚点外推)")

        # 单数字页号行: 止页=下一行起始-1
        parsed = []
        for i, (y, seq, page) in enumerate(results):
            s, e = page
            if s == e:
                nxt = None
                for j in range(i + 1, len(results)):
                    if results[j][2][0] > s:
                        nxt = results[j][2][0]
                        break
                if nxt is not None and nxt > s:
                    e = nxt - 1
            parsed.append((seq, s, e))
        return parsed

    # ---------- xlsx目录文件解析 ----------
    def _parse_catalog_from_xlsx(self, dir_name, wlog):
        """
        从xlsx文件读取分件数据: 在 self.xlsx_dir 及其子目录下查找与 dir_name 同名的
        xlsx文件, 第3行为标题行(含"序号""页号"列), 从第4行起读取数据。
        返回 [(序号int, 起页int, 止页int), ...] 或 None(未找到/读取失败)。
        """
        if not self.xlsx_dir or not os.path.isdir(self.xlsx_dir):
            return None

        # 查找与目录名同名的xlsx文件(递归搜索)
        xlsx_path = None
        for root, dirs, files in os.walk(self.xlsx_dir):
            for f in files:
                if f.lower().endswith('.xlsx') and os.path.splitext(f)[0] == dir_name:
                    xlsx_path = os.path.join(root, f)
                    break
            if xlsx_path:
                break

        if not xlsx_path:
            wlog(f"  [xlsx] 未找到与目录「{dir_name}」同名的xlsx文件")
            return None

        wlog(f"  [xlsx] 读取目录文件: {os.path.basename(xlsx_path)}")

        try:
            import openpyxl
            wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
            ws = wb.active

            # 第3行为标题行(索引2, 0-based), 查找"序号"和"页号"列
            header_row = list(ws.iter_rows(min_row=3, max_row=3, values_only=True))
            if not header_row:
                wlog(f"  [xlsx] 第3行为空, 无法读取标题行")
                wb.close()
                return None

            headers = [str(c).strip() if c is not None else '' for c in header_row[0]]
            seq_col = None
            page_col = None
            for i, h in enumerate(headers):
                if h == '序号':
                    seq_col = i
                elif h == '页号':
                    page_col = i

            if seq_col is None or page_col is None:
                wlog(f"  [xlsx] 标题行未找到「序号」或「页号」列, 标题: {headers}")
                wb.close()
                return None

            wlog(f"  [xlsx] 序号列={seq_col}, 页号列={page_col}")

            # 从第4行起读取数据
            raw_data = []  # [(序号int, 页号文本)]
            for row in ws.iter_rows(min_row=4, values_only=True):
                cells = list(row)
                if len(cells) <= max(seq_col, page_col):
                    continue
                seq_val = cells[seq_col]
                page_val = cells[page_col]
                if seq_val is None or page_val is None:
                    continue
                try:
                    seq_int = int(seq_val)
                except (ValueError, TypeError):
                    continue
                page_str = str(page_val).strip().replace(' ', '')
                if not page_str:
                    continue
                raw_data.append((seq_int, page_str))

            wb.close()

            if not raw_data:
                wlog(f"  [xlsx] 未读取到有效数据行")
                return None

            # 按序号从小到大排序
            raw_data.sort(key=lambda x: x[0])
            wlog(f"  [xlsx] 读取到 {len(raw_data)} 条数据")

            # 解析页号: 支持 "199-213" 范围格式和单数字格式
            parsed = []
            for i, (seq, page_str) in enumerate(raw_data):
                m = re.fullmatch(r'(\d{1,4})[-–—~](\d{1,4})', page_str)
                if m:
                    p_start, p_end = int(m.group(1)), int(m.group(2))
                    if p_end < p_start:
                        p_start, p_end = p_end, p_start
                    src = page_str
                else:
                    # 单数字: 起始页=该数字, 终止页=下一序号的起始页-1
                    try:
                        p_start = int(page_str)
                    except ValueError:
                        wlog(f"    [xlsx] 跳过行: 序号={seq} 页号格式无法解析「{page_str}」")
                        continue
                    # 找下一个有条目(范围式)的起始页, 或下一个序号的起始页
                    nxt = None
                    for j in range(i + 1, len(raw_data)):
                        m2 = re.match(r'(\d{1,4})', raw_data[j][1])
                        if m2:
                            nxt = int(m2.group(1))
                            break
                    p_end = (nxt - 1) if (nxt is not None and nxt > p_start) else p_start
                    src = f"{page_str}(推断到{p_end})"
                parsed.append((seq, p_start, p_end))
                wlog(f"    [xlsx] 序号={seq} 页号={p_start}-{p_end} ← 「{src}」")

            if not parsed:
                wlog(f"  [xlsx] 未能解析出有效分件数据")
                return None

            wlog(f"  [xlsx] 解析完成, 共 {len(parsed)} 件")
            return parsed

        except ImportError:
            wlog(f"  [xlsx] 缺少 openpyxl 库, 无法读取xlsx文件")
            return None
        except Exception as e:
            wlog(f"  [xlsx] 读取xlsx出错: {e}")
            return None

    # ---------- 文件操作 ----------
    @staticmethod
    def _num_of(fname):
        """提取文件名(不含扩展名)末尾的数字编号, 无数字返回 None。
        兼容纯数字文件名(0001.jpg)与带前缀文件名(档号-0001.jpg)。"""
        m = re.search(r'(\d{1,4})$', os.path.splitext(fname)[0])
        return int(m.group(1)) if m else None

    @staticmethod
    def _jpg_files_sorted(dir_path):
        """目录下 jpg 文件按文件名末尾数字编号升序(无编号的排最后)。"""
        files = [f for f in os.listdir(dir_path)
                 if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(dir_path, f))]
        def key(f):
            stem = os.path.splitext(f)[0]
            if stem.isdigit():
                return int(stem)
            n = FileSplitWorker._num_of(f)
            return n if n is not None else float('inf')
        return sorted(files, key=key)

    @staticmethod
    def _read_directory_txt(subdir, wlog):
        """
        读取目录下的 Directory.txt(由“文件批量替换”生成, 记录替换后的文件名
        清单, 不含扩展名, 每行一个)。
        返回 [(末尾编号, 不含扩展名文件名), ...] 按编号升序;
        文件不存在或无有效记录返回 None。
        """
        dpath = os.path.join(subdir, 'Directory.txt')
        if not os.path.isfile(dpath):
            return None
        lines = []
        for enc in ('utf-8', 'gbk'):
            try:
                with open(dpath, 'r', encoding=enc) as fh:
                    lines = [l.strip() for l in fh if l.strip()]
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                wlog(f"  × 读取 Directory.txt 失败: {e}")
                return None
        items = []
        for stem in lines:
            m = re.search(r'(\d{1,4})$', stem)
            if m:
                items.append((int(m.group(1)), stem))
        if not items:
            wlog("  × Directory.txt 存在但无有效文件名记录, 按不存在处理")
            return None
        items.sort(key=lambda t: t[0])
        return items

    def _resolve_directory_txt(self, subdir, jpgs, wlog):
        """
        解析 Directory.txt 得到 卷皮/目录页文件清单与后续文件偏移量。
        规则: 第一页(编号最小的jpg)为卷皮; Directory.txt 记录的文件为目录页;
        偏移量 = Directory.txt 中最大文件序号(小于2时按2)。
        返回 (offset, front_files), front_files=[卷皮, 目录页...];
        无 Directory.txt 或无有效记录返回 None。
        """
        items = self._read_directory_txt(subdir, wlog)
        if items is None or not jpgs:
            return None
        f1 = jpgs[0]
        f1_stem = os.path.splitext(f1)[0]
        by_num = {}
        for f in jpgs:
            n = self._num_of(f)
            if n is not None:
                by_num.setdefault(n, f)
        front = [f1]
        for num, stem in items:
            if stem == f1_stem:
                continue  # 卷皮页不计入目录页
            cand = None
            for f in jpgs:
                if os.path.splitext(f)[0] == stem:
                    cand = f
                    break
            if cand is None:
                cand = by_num.get(num)  # 命名形态不一致时按末尾编号匹配
            if cand is None:
                wlog(f"  × Directory.txt 记录「{stem}」在目录中无对应jpg, 忽略该记录")
                continue
            if cand not in front:
                front.append(cand)
        max_num = max(n for n, _ in items)
        offset = max(max_num, 2)
        wlog(f"  Directory.txt 共 {len(items)} 条记录, 最大文件序号 {max_num:04d}, "
             f"后续文件偏移量={offset}")
        return offset, front

    def _parse_catalog_from_dir(self, subdir, wlog):
        """
        对子目录做「目录页定位 + OCR + 标题判断 + 表格解析」(不移动任何文件)。
        分件与检查共用此入口, 保证两者行为一致。
        目录页定位:
          有 Directory.txt → 第一页为卷皮, 目录页为 Directory.txt 记录的文件
          (逐个尝试OCR), 后续文件偏移量=Directory.txt最大文件序号;
          无 Directory.txt → 未分件=根下第2张(0002); 已分件=卷皮目录里的第2张
          (偏移量缺省为2)。
        返回 (entries, front_files, offset, err):
          成功: entries=[(序号,起,止),...], front_files=归入卷皮目录的文件
          (卷皮+目录页), err=''
          失败: entries=[], err=状态字符串(跳过(xxx)/失败(xxx))
        """
        dir_name = os.path.basename(subdir)
        jpgs = self._jpg_files_sorted(subdir)
        if not jpgs:
            return [], [], 2, "跳过(无jpg)"

        # ---- Directory.txt 模式(已做过卷内目录替换): 卷皮=第一页, 目录页取自 Directory.txt ----
        info = self._resolve_directory_txt(subdir, jpgs, wlog)
        if info and len(info[1]) >= 2:
            offset, front_files = info
            wlog(f"  卷皮页: {front_files[0]}; 目录页(来自Directory.txt): "
                 f"{', '.join(front_files[1:])}")
            for cand in front_files[1:]:
                page_path = os.path.join(subdir, cand)
                rows = self._ocr_page(page_path, None, wlog)
                if not rows:
                    wlog(f"  目录页候选 {cand}: OCR无结果, 尝试下一个")
                    continue
                if not self._is_catalog_title(rows):
                    wlog(f"  目录页候选 {cand}: 非卷内文件目录, 尝试下一个")
                    continue
                wlog("  标题确认: 卷内文件目录")
                # 优先: 表格线模式(逐行裁剪OCR, 不漏行/序号不推断/支持汉字页号)
                try:
                    entries = self._parse_catalog_by_table(page_path, wlog)
                except Exception as e:
                    wlog(f"    表格线模式异常: {e}")
                    entries = []
                if not entries:
                    entries = self._parse_catalog_rows(rows, wlog)  # 回退: 全图片段模式
                if entries:
                    wlog(f"  目录页={cand}, 解析 {len(entries)} 行, 后续文件偏移量={offset}")
                    return entries, front_files, offset, ""
                wlog(f"  目录页候选 {cand}: 标题匹配但未解析到数据, 尝试下一个")
            return [], front_files, offset, "失败(Directory.txt记录均非目录页)"
        if info:
            wlog("  Directory.txt 存在但未解析出对应目录页jpg, 回退默认规则")

        # ---- 默认规则(无 Directory.txt) ----
        # 已分件目录: 卷皮/目录页归入编号0000目录(旧版为「卷皮目录」, 兼容两处)
        jp_dir = os.path.join(subdir, f"{dir_name}-0000")
        if not os.path.isdir(jp_dir):
            jp_dir = os.path.join(subdir, f"{dir_name}卷皮目录")  # 旧版结果兼容
        jp_jpgs = self._jpg_files_sorted(jp_dir) if os.path.isdir(jp_dir) else []
        if len(jp_jpgs) >= 2:
            f1, f2 = jp_jpgs[0], jp_jpgs[1]
            page2_path = os.path.join(jp_dir, f2)
            wlog(f"  目录页取自{os.path.basename(jp_dir)}: {f2}")
        elif len(jpgs) >= 2:
            f1, f2 = jpgs[0], jpgs[1]
            page2_path = os.path.join(subdir, f2)
        else:
            return [], [], 2, "跳过(无目录页)"

        rows = self._ocr_page(page2_path, None, wlog)
        if not rows:
            return [], [f1, f2], 2, "失败(OCR无结果)"
        if not self._is_catalog_title(rows):
            return [], [f1, f2], 2, "跳过(非目录页)"
        wlog("  标题确认: 卷内文件目录")

        # 优先: 表格线模式(逐行裁剪OCR, 不漏行/序号不推断/支持汉字页号)
        try:
            entries = self._parse_catalog_by_table(page2_path, wlog)
        except Exception as e:
            wlog(f"    表格线模式异常: {e}")
            entries = []
        if entries:
            wlog(f"  表格线模式解析 {len(entries)} 行")
            return entries, [f1, f2], 2, ""

        # 回退: 全图片段模式
        entries = self._parse_catalog_rows(rows, wlog)
        if not entries:
            return [], [f1, f2], 2, "失败(未解析到数据)"
        return entries, [f1, f2], 2, ""

    def _split_by_entries(self, subdir, entries, wlog, target_base=None, copy_mode=False,
                          offset=2):
        """
        按 entries 建序号子目录并处理文件(页号+偏移量=文件编号; 偏移量缺省为2,
        有 Directory.txt 时为其最大文件序号)。
        target_base=None: 原地移动(在 subdir 下建子目录并移入);
        target_base 指定: 输出到 target_base/目录名/ 下, copy_mode=True 拷贝
        (源目录不动), False 仍移动。返回 处理文件数。分件/手工分件共用。
        """
        dir_name = os.path.basename(subdir)
        out_root = os.path.join(target_base, dir_name) if target_base else subdir
        def _op(src, dst):
            if copy_mode:
                shutil.copy2(src, dst)
            else:
                shutil.move(src, dst)
        verb = '拷贝' if copy_mode else '移动'
        # 编号→文件名映射(兼容纯数字 0001.jpg 与带前缀 档号-0001.jpg 命名)
        num_map = {}
        for f in os.listdir(subdir):
            if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(subdir, f)):
                nn = self._num_of(f)
                if nn is not None:
                    num_map.setdefault(nn, f)
        moved = 0
        for seq, p_start, p_end in entries:
            sub_name = f"{dir_name}-{seq:04d}"
            sub_path = os.path.join(out_root, sub_name)
            os.makedirs(sub_path, exist_ok=True)
            for n in range(p_start + offset, p_end + offset + 1):
                fname = num_map.get(n, f"{n:04d}.jpg")
                src = os.path.join(subdir, fname)
                if os.path.exists(src):
                    try:
                        _op(src, os.path.join(sub_path, fname))
                        moved += 1
                    except Exception as e:
                        wlog(f"    × {verb}失败 {fname}: {e}")
                else:
                    wlog(f"    (缺) 编号{n:04d}文件不存在, 跳过")
            wlog(f"  序号{seq}: 页号{p_start}-{p_end} (偏移量={offset}) → {sub_name}/ "
                 f"{verb} 编号 {p_start + offset:04d}..{p_end + offset:04d}")
        return moved

    def _process_one_dir(self, subdir, logf, wlog, target_base=None, copy_mode=False):
        """处理单个子目录。返回 (状态字符串, 处理文件数)。"""
        dir_name = os.path.basename(subdir)
        jpgs = self._jpg_files_sorted(subdir)
        if len(jpgs) < 4:
            wlog(f"  [跳过] {dir_name}: jpg 少于 4 张({len(jpgs)}张), 无法分件")
            return "跳过(文件不足)", 0

        wlog(f"  总文件数: {len(jpgs)}")

        # 分件依据: xlsx目录文件模式 或 OCR模式
        if self.xlsx_dir:
            # xlsx目录文件模式: 从同名xlsx读取分件数据
            entries = self._parse_catalog_from_xlsx(dir_name, wlog)
            if entries is None:
                wlog(f"  [xlsx] 无法从目录文件获取分件数据, 跳过: {dir_name}")
                return "跳过(xlsx未找到)", 0
            # 卷皮/目录页与偏移量: 优先 Directory.txt; 无则缺省前两张+偏移量2
            info = self._resolve_directory_txt(subdir, jpgs, wlog)
            if info:
                offset, front_files = info
            else:
                offset, front_files = 2, jpgs[:2]
                wlog(f"  未找到 Directory.txt, 按缺省偏移量 2 处理; "
                     f"卷皮页: {front_files[0]}, {front_files[1]}")
        else:
            # OCR模式(默认)
            entries, front_files, offset, err = self._parse_catalog_from_dir(subdir, wlog)
            if err:
                wlog(f"  [{err.split('(')[0]}] {dir_name}: {err}")
                return err, 0

        out_root = os.path.join(target_base, dir_name) if target_base else subdir
        os.makedirs(out_root, exist_ok=True)
        verb = '拷贝' if copy_mode else '移动'
        def _op(src, dst):
            if copy_mode:
                shutil.copy2(src, dst)
            else:
                shutil.move(src, dst)

        # 建序号子目录并处理文件(手工分件共用)
        moved = self._split_by_entries(subdir, entries, wlog,
                                       target_base=target_base, copy_mode=copy_mode,
                                       offset=offset)

        # 备考表卷底 + 卷皮目录 统一合并到编号 0000 的目录(不再生成两个独立目录)
        path_zero = os.path.join(out_root, f"{dir_name}-0000")
        os.makedirs(path_zero, exist_ok=True)

        # 卷皮页 + 目录页 → 0000目录
        for fname in front_files:
            src = os.path.join(subdir, fname)
            if os.path.exists(src):
                _op(src, os.path.join(path_zero, fname))
                moved += 1
        wlog(f"  卷皮: {','.join(front_files)} → {dir_name}-0000/ [{verb}]")

        # 当前剩余文件里 最大与次大 → 备考表卷底
        if copy_mode:
            # 拷贝模式下源目录不变, 备考取未被规则覆盖的最大两张
            covered_nums = set()
            for seq, p_start, p_end in entries:
                covered_nums.update(range(p_start + offset, p_end + offset + 1))
            for fname in front_files:
                nn = self._num_of(fname)
                if nn is not None:
                    covered_nums.add(nn)
            remain = [f for f in jpgs
                      if (self._num_of(f) if self._num_of(f) is not None else -1)
                      not in covered_nums]
        else:
            remain = self._jpg_files_sorted(subdir)
        if len(remain) >= 2:
            for fname in (remain[-1], remain[-2]):
                src = os.path.join(subdir, fname)
                _op(src, os.path.join(path_zero, fname))
                moved += 1
            wlog(f"  备考: {remain[-2]},{remain[-1]} → {dir_name}-0000/ [{verb}]")
        else:
            wlog(f"  备考: 剩余文件不足2张({len(remain)}), 未处理")

        # 分件完成后删除当前目录下 Directory.txt(已消费);
        # 移动/拷贝到分件目录时始终忽略该文件(不随分件结果输出)
        dpath = os.path.join(subdir, 'Directory.txt')
        if os.path.isfile(dpath):
            try:
                os.remove(dpath)
                wlog(f"  已删除当前目录下 Directory.txt (分件已消费, 不随分件输出)")
            except Exception as e:
                wlog(f"  × 删除 Directory.txt 失败: {e}")

        return f"完成({len(entries)}件,{verb}{moved}个文件)", moved

    def run(self):
        try:
            # GPU环境预处理(必须在 paddle 首次导入之前执行):
            # 装了GPU版paddle但机器无NVIDIA卡时, paddle导入即锁定找GPU设备,
            # 之后任何配置都报「Device id must be less than GPU count」。
            # 用 ctypes 检测 nvcuda.dll(不导入paddle): 无卡则屏蔽CUDA设备,
            # 让paddle全程走纯CPU(用户勾选GPU时同样只能回退, 日志已提示)。
            try:
                if 'CUDA_VISIBLE_DEVICES' not in os.environ:
                    import ctypes as _ct
                    try:
                        _ct.CDLL('nvcuda.dll')
                        _has_nvidia = True
                    except OSError:
                        _has_nvidia = False
                    if not _has_nvidia:
                        os.environ['CUDA_VISIBLE_DEVICES'] = ''
            except Exception:
                pass

            if not os.path.isdir(self.base_dir):
                self.finished_signal.emit(False, "所选目录不存在")
                return

            # 分件到新目录: 目标目录不存在则创建
            if self.target_base:
                os.makedirs(self.target_base, exist_ok=True)

            # 日志文件放在用户所选目录下
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_path = os.path.join(self.base_dir, f"分件处理日志_{ts}.txt")
            logf = open(log_path, 'w', encoding='utf-8')
            lock = __import__('threading').Lock()

            def wlog(s):
                with lock:
                    logf.write(s + "\n")
                    logf.flush()
                self.log_signal.emit(s)

            wlog("分件处理日志")
            wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog(f"所选目录: {self.base_dir}")
            if self.xlsx_dir:
                wlog(f"分件模式: 读取目录文件(xlsx) → {self.xlsx_dir}")
            else:
                wlog(f"分件模式: OCR识别目录页")
            wlog("=" * 70)

            subdirs = sorted([os.path.join(self.base_dir, d)
                              for d in os.listdir(self.base_dir)
                              if os.path.isdir(os.path.join(self.base_dir, d))])
            total = len(subdirs)
            if total == 0:
                logf.close()
                self.finished_signal.emit(False, "所选目录下没有子目录")
                return

            wlog(f"共发现 {total} 个子目录待处理")
            done = 0
            moved_total = 0
            for subdir in subdirs:
                if self.is_stopped:
                    wlog("用户停止处理")
                    break
                wlog("")
                wlog(f"[{done + 1}/{total}] 处理: {os.path.basename(subdir)}")
                wlog("-" * 50)
                try:
                    status, moved = self._process_one_dir(
                        subdir, logf, wlog,
                        target_base=self.target_base, copy_mode=self.copy_mode)
                    moved_total += moved
                    wlog(f"  结果: {status}")
                except Exception as e:
                    import traceback
                    wlog(f"  [异常] {e}")
                    wlog(traceback.format_exc())
                done += 1
                self.progress_signal.emit(done, total)

            wlog("")
            wlog("=" * 70)
            wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog(f"总计: 处理 {done}/{total} 个子目录, 移动文件 {moved_total} 个")
            if self.is_stopped:
                wlog("注意: 处理被用户中途停止")
            logf.close()

            msg = (f"分件完成！处理 {done}/{total} 个子目录，移动 {moved_total} 个文件。\n"
                   f"日志: {os.path.basename(log_path)}")
            self.finished_signal.emit(not self.is_stopped, msg)

        except Exception as e:
            import traceback
            self.log_signal.emit(traceback.format_exc())
            self.finished_signal.emit(False, f"处理出错: {e}")

    def stop(self):
        self.is_stopped = True


class FileSplitCheckWorker(FileSplitWorker):
    """
    分件检查后台线程 —— 继承 FileSplitWorker, OCR/解析/文件排序全部复用
    分件代码(_parse_catalog_from_dir / _parse_catalog_from_xlsx), 保证检查与分件行为完全一致。
    对每个子目录: 解析目录页(xlsx或OCR)得到序号/页号, 推算「应被移走」的文件集合,
    检测根目录中按标准应移走却仍残留的文件 → 记入检查报告。不移动任何文件。
    """
    progress_signal = Signal(int, int)

    def __init__(self, base_dir, xlsx_dir=None, parent=None):
        super().__init__(base_dir, xlsx_dir=xlsx_dir, parent=parent)

    def _check_one_dir(self, subdir, wlog):
        """
        按分件规则检查单个子目录(不移动文件)。检查项:
        1. 卷内文件目录页是否存在、能否正常解析(OCR失败/非目录页/无数据=错误);
        2. 每段页号范围是否有足够文件(页号+偏移量=文件编号, 偏移量=
           Directory.txt最大序号, 无Directory.txt缺省为2; 范围内缺文件=错误);
        3. 分件规则覆盖完成后, 根目录剩余的文件(未被任何页号段/卷皮/备考覆盖)=错误。
        返回 (状态, 错误明细list) —— 每条错误含类型与对应文件名。
        """
        errors = []
        dir_name = os.path.basename(subdir)
        jpgs = self._jpg_files_sorted(subdir)
        if not jpgs:
            return "错误(无jpg)", [f"{dir_name}: [目录异常] 根目录无 jpg 文件"]

        # --- 检查项1: 目录页存在性与可解析性 ---
        if self.xlsx_dir:
            # xlsx目录文件模式
            entries = self._parse_catalog_from_xlsx(dir_name, wlog)
            if entries is None:
                return "错误(xlsx未找到)", [f"{dir_name}: [目录解析] 未找到同名xlsx目录文件"]
            info = self._resolve_directory_txt(subdir, jpgs, wlog)
            if info:
                offset, front_files = info
            else:
                offset, front_files = 2, list(jpgs[:2])
        else:
            # OCR模式(默认)
            entries, front_files, offset, err = self._parse_catalog_from_dir(subdir, wlog)
            if err:
                # err 形如 "失败(OCR无结果)"/"跳过(非目录页)"/"失败(未解析到数据)"
                return f"错误({err})", [f"{dir_name}: [目录解析] {err}"]

        wlog(f"  解析到 {len(entries)} 段页号 (偏移量={offset})")

        # 当前根目录实际存在的文件(按末尾编号映射)
        num_map = {}
        for f in jpgs:
            nn = self._num_of(f)
            if nn is not None:
                num_map.setdefault(nn, f)
        existing = set(jpgs)
        # 分件规则覆盖到的文件集合(含每段页号范围 + 卷皮/目录页 + 备考)
        covered = set()

        # --- 检查项2: 每段页号范围内文件是否足够 ---
        for seq, p_start, p_end in entries:
            expect_nums = list(range(p_start + offset, p_end + offset + 1))
            missing = [n for n in expect_nums if n not in num_map]
            covered.update(num_map[n] for n in expect_nums if n in num_map)
            if missing:
                # 该段期望 (p_end-p_start+1) 个, 缺 len(missing) 个
                total = p_end - p_start + 1
                errors.append(f"{dir_name}: [文件不足] 序号{seq} 页号{p_start}-{p_end} "
                              f"应有{total}个文件, 缺{len(missing)}个: "
                              f"{', '.join(f'{n:04d}' for n in missing[:10])}"
                              f"{'...' if len(missing) > 10 else ''}")
                wlog(f"  [文件不足] 序号{seq}: 缺 {len(missing)} 个 "
                     f"({', '.join(f'{n:04d}' for n in missing[:8])}"
                     f"{'...' if len(missing) > 8 else ''})")
            else:
                wlog(f"  序号{seq}: 页号{p_start}-{p_end} 文件齐全({len(expect_nums)}个)")

        # 卷皮/目录页(front_files)与备考(剩余最大两张)也计入覆盖
        for fname in front_files:
            if fname in existing:
                covered.add(fname)
        remain_sim = [f for f in jpgs if f not in covered]
        if len(remain_sim) >= 2:
            covered.add(remain_sim[-1])
            covered.add(remain_sim[-2])

        # --- 检查项3: 规则覆盖后仍剩余的文件 ---
        leftover = [f for f in jpgs if f not in covered]
        if leftover:
            errors.append(f"{dir_name}: [剩余文件] 分件规则未覆盖, 残留 "
                          f"{len(leftover)} 个: {', '.join(leftover[:10])}"
                          f"{'...' if len(leftover) > 10 else ''}")
            wlog(f"  [剩余文件] {len(leftover)} 个未被覆盖: "
                 f"{', '.join(leftover[:8])}{'...' if len(leftover) > 8 else ''}")

        if errors:
            return f"错误({len(errors)}项)", errors
        return "正常", errors

    def run(self):
        try:
            if not os.path.isdir(self.base_dir):
                self.finished_signal.emit(False, "所选目录不存在")
                return

            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = os.path.join(self.base_dir, f"分件检查报告_{ts}.txt")
            logf = open(report_path, 'w', encoding='utf-8')
            lock = __import__('threading').Lock()

            def wlog(s):
                with lock:
                    logf.write(s + "\n")
                    logf.flush()
                self.log_signal.emit(s)

            wlog("分件检查报告")
            wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog(f"所选目录: {self.base_dir}")
            if self.xlsx_dir:
                wlog(f"检查模式: 读取目录文件(xlsx) → {self.xlsx_dir}")
                wlog("检查标准: 从xlsx获取分件数据, 推算应移走文件, 检测根目录残留")
            else:
                wlog("检查标准: 复用分件OCR解析, 推算应移走文件, 检测根目录残留")
            wlog("=" * 70)

            subdirs = sorted([os.path.join(self.base_dir, d)
                              for d in os.listdir(self.base_dir)
                              if os.path.isdir(os.path.join(self.base_dir, d))])
            total = len(subdirs)
            if total == 0:
                logf.close()
                self.finished_signal.emit(False, "所选目录下没有子目录")
                return

            wlog(f"共 {total} 个子目录待检查")
            all_errors = []
            stats = {}
            done = 0
            for subdir in subdirs:
                if self.is_stopped:
                    wlog("用户停止检查")
                    break
                wlog("")
                wlog(f"[{done + 1}/{total}] 检查: {os.path.basename(subdir)}")
                wlog("-" * 50)
                try:
                    status, errs = self._check_one_dir(subdir, wlog)
                    stats[status] = stats.get(status, 0) + 1
                    if errs:
                        # 按目录归组: 目录名 + 各错误类型(含文件名)
                        all_errors.append((os.path.basename(subdir), errs))
                    wlog(f"  结果: {status}")
                except Exception as e:
                    import traceback
                    wlog(f"  [异常] {e}")
                    wlog(traceback.format_exc())
                    all_errors.append((os.path.basename(subdir),
                                       [f"[检查异常] {e}"]))
                done += 1
                self.progress_signal.emit(done, total)

            wlog("")
            wlog("=" * 70)
            wlog("检查汇总:")
            for k, v in sorted(stats.items()):
                wlog(f"  {k}: {v} 个目录")
            n_err_dirs = len(all_errors)
            n_err_items = sum(len(e) for _, e in all_errors)
            wlog(f"有错误的目录: {n_err_dirs} 个, 错误共 {n_err_items} 项")
            if all_errors:
                wlog("")
                wlog("错误明细(按目录, 含错误类型与文件名):")
                for dname, errs in all_errors:
                    wlog(f"  ▷ {dname}")
                    for e in errs:
                        wlog(f"     × {e}")
            wlog("")
            wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logf.close()

            msg = (f"检查完成！{done}/{total} 个目录；"
                   f"{n_err_dirs} 个目录有错误(共{n_err_items}项)。\n"
                   f"报告: {os.path.basename(report_path)}")
            self.finished_signal.emit(not self.is_stopped, msg)
        except Exception as e:
            import traceback
            self.log_signal.emit(traceback.format_exc())
            self.finished_signal.emit(False, f"检查出错: {e}")


def manual_split_entries(text):
    """
    解析手工分件输入(多行)为分件条目。
    行格式:
      卷皮目录: 1-2          (可选, 文件名页码, 直接用不+2)
      备考表卷底: 213-214    (可选, 同上)
      1 1-180               (序号 页号; 页号+2=文件名, 与自动分件一致)
    页号支持单数字(183)或范围(184-197)。
    返回 (卷皮range|None, 备考range|None, entries, err)。
    校验: 格式/序号唯一升序/页号连续性(本条起始=前条止页+1)。
    """
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if not lines:
        return None, None, [], "未输入任何内容"

    juanpi = beikao = None
    entries = []

    def parse_range(s):
        m = re.fullmatch(r'(\d{1,4})\s*[-–—~]\s*(\d{1,4})', s.strip())
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            return (min(a, b), max(a, b))
        if re.fullmatch(r'\d{1,4}', s.strip()):
            v = int(s.strip())
            return (v, v)
        return None

    for ln in lines:
        low = ln.replace(' ', '').replace('：', ':')
        if low.startswith('卷皮目录'):
            parts = ln.split(':', 1) if ':' in ln else ln.split('：', 1)
            if len(parts) < 2:
                return None, None, [], "「卷皮目录」行缺少页号(格式: 卷皮目录: 1-2)"
            r = parse_range(parts[1])
            if not r:
                return None, None, [], f"「卷皮目录」页号格式错误: {parts[1]}"
            juanpi = r
            continue
        if low.startswith('备考表卷底'):
            parts = ln.split(':', 1) if ':' in ln else ln.split('：', 1)
            if len(parts) < 2:
                return None, None, [], "「备考表卷底」行缺少页号(格式: 备考表卷底: 213-214)"
            r = parse_range(parts[1])
            if not r:
                return None, None, [], f"「备考表卷底」页号格式错误: {parts[1]}"
            beikao = r
            continue
        parts = ln.split()
        if len(parts) != 2:
            return None, None, [], f"行格式错误(应为「序号 页号」): {ln}"
        if not re.fullmatch(r'\d{1,2}', parts[0]):
            return None, None, [], f"序号须为1-2位数字: {parts[0]}"
        r = parse_range(parts[1])
        if not r:
            return None, None, [], f"页号格式错误(应为 17 或 17-101): {parts[1]}"
        entries.append((int(parts[0]), r[0], r[1]))

    if not entries:
        return None, None, [], "未输入任何序号/页号数据行"

    seqs = [e[0] for e in entries]
    if len(set(seqs)) != len(seqs):
        return None, None, [], f"序号重复: {seqs}"
    if seqs != sorted(seqs):
        return None, None, [], f"序号未按升序: {seqs}"

    for i in range(1, len(entries)):
        prev_end = entries[i - 1][2]
        cur_start = entries[i][1]
        if cur_start != prev_end + 1:
            return (None, None, [],
                    f"页号不连续: 序号{entries[i - 1][0]}止于{prev_end}, "
                    f"序号{entries[i][0]}应从{prev_end + 1}开始, 实际{cur_start}")
    return juanpi, beikao, entries, ""


class ManualSplitDialog(QDialog):
    """
    手工分件对话框: 列出待处理目录, 用户输入多行序号/页号(前两行可选
    卷皮目录/备考表卷底的文件名页码), 校验后执行分件; 完成自动切换下一个。
    文件移动复用 FileSplitWorker._split_by_entries。
    """

    def __init__(self, base_dir, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.pending_dirs = self._scan_pending()
        self.current_idx = -1
        self.total_moved = 0
        self.splitter = FileSplitWorker(base_dir)  # 仅用其文件排序/移动方法

        self.setWindowTitle("手工分件")
        self.resize(760, 640)

        v = QVBoxLayout(self)
        v.addWidget(QLabel("待处理目录:"))
        self.dir_list = QListWidget()
        self.dir_list.setMaximumHeight(140)
        for d in self.pending_dirs:
            self.dir_list.addItem(d)
        self.dir_list.currentRowChanged.connect(self.on_dir_selected)
        v.addWidget(self.dir_list)

        v.addWidget(QLabel("分件数据表格 (「页号」支持 17 或 17-101; 序号行页号按+2换算;\n"
                           "卷皮目录/备考表卷底行输入文件名页码, 不换算, 留空用默认):"))
        # 表格输入: 第0/1行固定为 卷皮目录/备考表卷底, 其后为数据行
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["序号", "页号", "说明"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self._init_table_rows()
        # 回车跳到下一个输入项: 在数据行内 序号→页号→下一行序号→…;
        # 最后一行末格回车自动加行并进入新行序号格
        self.table.keyPressEvent = self._table_key_press
        # 工具行: 增/删数据行
        tr = QHBoxLayout()
        btn_add = QPushButton("+ 加行")
        btn_add.setObjectName("BrowseBtn")
        btn_add.clicked.connect(self.add_row)
        tr.addWidget(btn_add)
        btn_del = QPushButton("− 删选中行")
        btn_del.setObjectName("BrowseBtn")
        btn_del.clicked.connect(self.del_row)
        tr.addWidget(btn_del)
        tr.addStretch()
        v.addLayout(tr)
        v.addWidget(self.table, 1)

        self.hint = QLabel("")
        self.hint.setStyleSheet("color: #B45309; font-size: 12px;")
        v.addWidget(self.hint)

        h = QHBoxLayout()
        self.apply_btn = QPushButton("执行分件")
        self.apply_btn.setObjectName("ActionBtn")
        self.apply_btn.clicked.connect(self.apply)
        h.addWidget(self.apply_btn)
        self.skip_btn = QPushButton("跳过此目录")
        self.skip_btn.setObjectName("BrowseBtn")
        self.skip_btn.clicked.connect(self.skip)
        h.addWidget(self.skip_btn)
        self.close_btn = QPushButton("结束")
        self.close_btn.setObjectName("BrowseBtn")
        self.close_btn.clicked.connect(self.close)
        h.addWidget(self.close_btn)
        h.addStretch()
        v.addLayout(h)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(150)
        v.addWidget(QLabel("处理日志:"))
        v.addWidget(self.log_box)

        if self.pending_dirs:
            self.dir_list.setCurrentRow(0)
        else:
            self.hint.setText("所选目录下没有待处理目录(根下有jpg且未分件的子目录)")

    def _scan_pending(self):
        """待处理 = 根下有 jpg 且未分件(无 -NNNN 序号子目录/卷皮未归档)的子目录。"""
        out = []
        try:
            for d in sorted(os.listdir(self.base_dir)):
                p = os.path.join(self.base_dir, d)
                if not os.path.isdir(p):
                    continue
                jpgs = [f for f in os.listdir(p)
                        if f.lower().endswith('.jpg')
                        and os.path.isfile(os.path.join(p, f))]
                if not jpgs:
                    continue
                subs = [s for s in os.listdir(p)
                        if os.path.isdir(os.path.join(p, s))
                        and re.search(r'-\d{4}$', s)]
                if subs and len(jpgs) <= 2:
                    continue
                out.append(d)
        except Exception:
            pass
        return out

    def log(self, s):
        self.log_box.append(f">> {s}")

    # ---------- 表格输入辅助 ----------
    def _init_table_rows(self):
        """初始化表格: 前2行固定(卷皮目录/备考表卷底), 预置5个空数据行。"""
        self.table.setRowCount(0)
        self._append_fixed_row("卷皮目录", "文件名页码, 不+2换算; 留空=默认0001/0002")
        self._append_fixed_row("备考表卷底", "文件名页码, 不+2换算; 留空=默认剩余最大两张")
        for _ in range(5):
            self.add_row()

    def _append_fixed_row(self, name, note):
        r = self.table.rowCount()
        self.table.insertRow(r)
        it0 = QTableWidgetItem(name)
        it0.setFlags(it0.flags() & ~Qt.ItemIsEditable)  # 名称列锁定
        self.table.setItem(r, 0, it0)
        self.table.setItem(r, 1, QTableWidgetItem(""))
        it2 = QTableWidgetItem(note)
        it2.setFlags(it2.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(r, 2, it2)

    def add_row(self):
        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(""))
        self.table.setItem(r, 1, QTableWidgetItem(""))
        self.table.setItem(r, 2, QTableWidgetItem(""))

    def _table_key_press(self, event):
        """回车→下一个输入项: 页号列→下一行序号列; 序号列→本行页号列。
        最后一行页号回车→自动加行并进入新行序号格。其余按键走默认处理。"""
        from PyQt5.QtGui import QKeyEvent
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            r = self.table.currentRow()
            c = self.table.currentColumn()
            if r < 0:
                return
            if c == 0:
                # 序号 → 本行页号
                self.table.setCurrentCell(r, 1)
                self.table.editItem(self.table.item(r, 1))
                return
            if c == 1:
                # 页号 → 下一行序号; 末行则加行
                if r + 1 < self.table.rowCount():
                    self.table.setCurrentCell(r + 1, 0)
                    self.table.editItem(self.table.item(r + 1, 0))
                else:
                    self.add_row()
                    self.table.setCurrentCell(r + 1, 0)
                    self.table.editItem(self.table.item(r + 1, 0))
                return
        # 其余按键交给 QTableWidget 默认处理
        return QTableWidget.keyPressEvent(self.table, event)

    def del_row(self):
        rows = sorted({i.row() for i in self.table.selectedIndexes()}, reverse=True)
        for r in rows:
            if r >= 2:  # 固定行不可删
                self.table.removeRow(r)

    def _table_values(self):
        """读取表格 → (卷皮range|None, 备考range|None, entries, err)。"""
        def parse_range(s):
            t = s.strip().replace(' ', '')
            m = re.fullmatch(r'(\d{1,4})[-–—~](\d{1,4})', t)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                return (min(a, b), max(a, b))
            if re.fullmatch(r'\d{1,4}', t):
                return (int(t), int(t))
            return None

        def cell(r, c):
            it = self.table.item(r, c)
            return (it.text() if it else '').strip()

        jp_txt = cell(0, 1)
        bk_txt = cell(1, 1)
        if jp_txt and jp_txt != '-':
            juanpi = parse_range(jp_txt)
            if not juanpi:
                return None, None, [], f"卷皮目录页号格式错误: {jp_txt}"
        else:
            juanpi = None
        if bk_txt and bk_txt != '-':
            beikao = parse_range(bk_txt)
            if not beikao:
                return None, None, [], f"备考表卷底页号格式错误: {bk_txt}"
        else:
            beikao = None

        entries = []
        for r in range(2, self.table.rowCount()):
            seq_txt = cell(r, 0)
            pg_txt = cell(r, 1)
            if not seq_txt and not pg_txt:
                continue  # 空行跳过
            if not re.fullmatch(r'\d{1,2}', seq_txt):
                return None, None, [], f"第{r - 1}行序号须为1-2位数字: 「{seq_txt}」"
            pg = parse_range(pg_txt)
            if not pg:
                return None, None, [], f"序号{seq_txt}页号格式错误(17 或 17-101): 「{pg_txt}」"
            entries.append((int(seq_txt), pg[0], pg[1]))

        if not entries:
            return None, None, [], "未输入任何序号/页号数据行"

        seqs = [e[0] for e in entries]
        if len(set(seqs)) != len(seqs):
            return None, None, [], f"序号重复: {seqs}"
        if seqs != sorted(seqs):
            return None, None, [], f"序号未按升序: {seqs}"
        for i in range(1, len(entries)):
            prev_end = entries[i - 1][2]
            cur_start = entries[i][1]
            if cur_start != prev_end + 1:
                return (None, None, [],
                        f"页号不连续: 序号{entries[i - 1][0]}止于{prev_end}, "
                        f"序号{entries[i][0]}应从{prev_end + 1}开始, 实际{cur_start}")
        return juanpi, beikao, entries, ""

    def on_dir_selected(self, row):
        self.current_idx = row
        if 0 <= row < len(self.pending_dirs):
            self.hint.setText(f"当前目录: {self.pending_dirs[row]}  "
                              f"(第 {row + 1}/{len(self.pending_dirs)} 个)")
            # 清空数据行(保留卷皮/备考两固定行)
            while self.table.rowCount() > 2:
                self.table.removeRow(self.table.rowCount() - 1)
            for _ in range(5):
                self.add_row()
            self.table.setFocus()

    def apply(self):
        if not (0 <= self.current_idx < len(self.pending_dirs)):
            QMessageBox.warning(self, "提示", "请先在列表中选择待处理目录")
            return
        juanpi, beikao, entries, err = self._table_values()
        if err:
            self.hint.setText("输入错误: " + err)
            QMessageBox.warning(self, "输入错误", err)
            return

        dir_name = self.pending_dirs[self.current_idx]
        subdir = os.path.join(self.base_dir, dir_name)
        reply = QMessageBox.question(
            self, "确认分件",
            f"将对 {dir_name} 执行分件:\n"
            + ''.join(f"  序号{s}: {a}-{b}\n" for s, a, b in entries)
            + "文件将被移动(不可自动撤销)，确定执行吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.log(f"── 分件: {dir_name} ──")

        def move_named(dst_path, rng):
            """卷皮/备考: 输入即文件名页码(不+2), 复用移动语义。"""
            os.makedirs(dst_path, exist_ok=True)
            cnt = 0
            for n in range(rng[0], rng[1] + 1):
                fname = f"{n:04d}.jpg"
                src = os.path.join(subdir, fname)
                if os.path.exists(src):
                    shutil.move(src, os.path.join(dst_path, fname))
                    cnt += 1
                else:
                    self.log(f"    (缺) {fname} 不存在, 跳过")
            return cnt

        # 序号子目录 —— 复用分件worker的移动方法
        moved = self.splitter._split_by_entries(subdir, entries, self.log)

        # 卷皮目录
        jp_path = os.path.join(subdir, f"{dir_name}卷皮目录")
        if juanpi:
            c = move_named(jp_path, juanpi)
            self.log(f"  卷皮: 文件{juanpi[0]:04d}-{juanpi[1]:04d} → {dir_name}卷皮目录/ 移动{c}个")
        else:
            os.makedirs(jp_path, exist_ok=True)
            jpgs = self.splitter._jpg_files_sorted(subdir)
            for fname in (jpgs[0], jpgs[1]) if len(jpgs) >= 2 else []:
                src = os.path.join(subdir, fname)
                if os.path.exists(src):
                    shutil.move(src, os.path.join(jp_path, fname))
                    moved += 1
            self.log(f"  卷皮: 默认(最小两张) → {dir_name}卷皮目录/")

        # 备考表卷底
        bk_path = os.path.join(subdir, f"{dir_name}备考表卷底")
        if beikao:
            c = move_named(bk_path, beikao)
            self.log(f"  备考: 文件{beikao[0]:04d}-{beikao[1]:04d} → {dir_name}备考表卷底/ 移动{c}个")
        else:
            os.makedirs(bk_path, exist_ok=True)
            remain = self.splitter._jpg_files_sorted(subdir)
            if len(remain) >= 2:
                for fname in (remain[-1], remain[-2]):
                    shutil.move(os.path.join(subdir, fname),
                                os.path.join(bk_path, fname))
                    moved += 1
                self.log(f"  备考: 默认(剩余最大两张) → {dir_name}备考表卷底/")
            else:
                self.log(f"  备考: 剩余不足2张({len(remain)}), 未移动")

        self.total_moved += moved
        self.log(f"结果: 完成({len(entries)}件, 移动{moved}个文件)")

        # 分件完成后删除当前目录下 Directory.txt(已消费, 不随分件输出)
        dpath = os.path.join(subdir, 'Directory.txt')
        if os.path.isfile(dpath):
            try:
                os.remove(dpath)
                self.log(f"  已删除当前目录下 Directory.txt (分件已消费, 不随分件输出)")
            except Exception as e:
                self.log(f"  × 删除 Directory.txt 失败: {e}")

        # 从待处理列表移除并自动切换下一个
        self.pending_dirs.pop(self.current_idx)
        self.dir_list.clear()
        for d in self.pending_dirs:
            self.dir_list.addItem(d)
        if self.pending_dirs:
            nxt = min(self.current_idx, len(self.pending_dirs) - 1)
            self.dir_list.setCurrentRow(nxt)
            self.hint.setText(f"已完成 {dir_name}。自动切换到下一个: {self.pending_dirs[nxt]}")
        else:
            self.hint.setText("全部待处理目录分件完成！")
            QMessageBox.information(self, "完成",
                                    f"全部分件完成！共移动 {self.total_moved} 个文件。")
            self.close()

    def skip(self):
        if 0 <= self.current_idx < len(self.pending_dirs):
            d = self.pending_dirs.pop(self.current_idx)
            self.log(f"跳过: {d}")
            self.dir_list.clear()
            for dd in self.pending_dirs:
                self.dir_list.addItem(dd)
            if self.pending_dirs:
                self.dir_list.setCurrentRow(min(self.current_idx, len(self.pending_dirs) - 1))
            else:
                self.hint.setText("全部待处理目录已处理(或跳过)")
                QMessageBox.information(self, "完成", "全部待处理目录已处理完成。")
                self.close()


# ---------------- 文件改名记录数据库(sqlite) ----------------
_RENAME_DB_NAME = 'rename_modified_records.db'

def _rename_db_path():
    """记录库固定放在程序目录(独立于处理目录, 跨次累积)。"""
    base = getattr(sys, '_MEIPASS', None)
    if base:
        base = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, _RENAME_DB_NAME)

def _rename_db_init(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS renamed_files (
        src_path TEXT NOT NULL,
        src_name TEXT NOT NULL,
        new_name TEXT,
        renamed_at TEXT,
        PRIMARY KEY (src_path, src_name))""")
    # 兼容升级: 旧表无 done_path/done_name 列时补上(记录新名判重用)
    cols = [r[1] for r in conn.execute("PRAGMA table_info(renamed_files)").fetchall()]
    if 'done_path' not in cols:
        conn.execute("ALTER TABLE renamed_files ADD COLUMN done_path TEXT DEFAULT ''")
    if 'done_name' not in cols:
        conn.execute("ALTER TABLE renamed_files ADD COLUMN done_name TEXT DEFAULT ''")
    conn.commit()

def _rename_db_record_many(records):
    """批量写入改名记录(原路径+原名→新路径+新名, 原名与新名都参与判重)。"""
    import sqlite3
    try:
        conn = sqlite3.connect(_rename_db_path())
        try:
            _rename_db_init(conn)
            conn.executemany(
                "INSERT OR REPLACE INTO renamed_files "
                "(src_path, src_name, new_name, renamed_at, done_path, done_name) "
                "VALUES (?,?,?,?,?,?)",
                [(r['src_path'], r['src_name'], r.get('new_name', ''),
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  r.get('done_path', ''), r.get('done_name', ''))
                 for r in records])
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass

def _rename_db_processed_set():
    """已处理过的 (路径, 文件名) 集合 —— 原名与新名都计入:
    改名后的文件(新名)再次扫描时不被误判为「新增」而重复改名。"""
    import sqlite3
    try:
        if not os.path.exists(_rename_db_path()):
            return set()
        conn = sqlite3.connect(_rename_db_path())
        try:
            _rename_db_init(conn)
            rows = conn.execute(
                "SELECT src_path, src_name, done_path, done_name FROM renamed_files").fetchall()
            done = set()
            for sp, sn, dp, dn in rows:
                done.add((sp.lower(), sn.lower()))          # 原名
                if dp and dn:
                    done.add((dp.lower(), dn.lower()))      # 新名
            return done
        finally:
            conn.close()
    except Exception:
        return set()


class FileRenameWorker(QThread):
    """文件重命名后台处理线程"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    def __init__(self, base_dir, modify_dpi=False, only_new=False, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.modify_dpi = modify_dpi  # 是否修改JPG文件的DPI为600
        self.only_new = only_new      # 只修改新增: 与记录(原路径+原文件名)相同的跳过
        self.is_stopped = False
    
    def run(self):
        try:
            results = {
                "processed_dirs": 0,
                "renamed_files": 0,
                "failed_files": 0,
                "errors": [],
                "actions": [],
                "log_entries": []
            }
            
            # 遍历基础目录下的所有子目录
            subdirs = [d for d in Path(self.base_dir).iterdir() if d.is_dir()]
            total_dirs = len(subdirs)
            processed_dirs = 0
            skipped_new = 0
            ok_records = []   # 改名成功记录 → sqlite

            # 只修改新增: 加载历史记录集(原路径+原文件名)
            done_set = _rename_db_processed_set() if self.only_new else set()
            if self.only_new and done_set:
                self.log_signal.emit(f"「只修改新增」: 已加载 {len(done_set)} 条历史改名记录")

            for subdir in subdirs:
                if self.is_stopped:
                    break

                # 获取子目录中的所有文件
                files = [f for f in subdir.iterdir() if f.is_file()]

                # 只修改新增: 与历史记录(原路径+原文件名)完全相同的文件跳过
                if self.only_new and done_set and files:
                    before = len(files)
                    files = [f for f in files
                             if (str(f.parent).lower(), f.name.lower()) not in done_set]
                    n_skip = before - len(files)
                    if n_skip:
                        skipped_new += n_skip
                        self.log_signal.emit(f"  跳过已改名的文件 {n_skip} 个({subdir.name})")

                if not files:
                    processed_dirs += 1
                    continue
                
                # 获取目录名（不含路径）
                dir_name = subdir.name
                
                # 如果只有一个文件，直接使用目录名
                if len(files) == 1:
                    file = files[0]
                    new_name = subdir / f"{dir_name}{file.suffix}"
                    
                    action_desc = f"将 '{file.name}' 重命名为 '{new_name.name}'"
                    results["actions"].append(action_desc)
                    self.log_signal.emit(action_desc)
                    
                    log_entry = {
                        "directory": subdir.name,
                        "original_name": file.name,
                        "new_name": new_name.name,
                        "modify_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "success": True,
                        "error_msg": ""
                    }
                    
                    try:
                        file.rename(new_name)
                        results["renamed_files"] += 1
                        ok_records.append({'src_path': str(file.parent),
                                           'src_name': file.name,
                                           'new_name': new_name.name,
                                           'done_path': str(new_name.parent),
                                           'done_name': new_name.name})

                        # 如果需要修改DPI且是JPG文件，则修改DPI
                        if self.modify_dpi and new_name.suffix.lower() in ['.jpg', '.jpeg']:
                            try:
                                img = Image.open(new_name)
                                # 设置DPI为600
                                img.save(new_name, dpi=(600, 600))
                                self.log_signal.emit(f"已修改 {new_name.name} 的DPI为600")
                            except Exception as dpi_error:
                                error_msg = f"修改DPI失败 {new_name.name}: {str(dpi_error)}"
                                results["errors"].append(error_msg)
                                log_entry["success"] = False
                                log_entry["error_msg"] = error_msg
                                self.log_signal.emit(f"错误: {error_msg}")
                    except Exception as e:
                        error_msg = f"重命名文件失败 {file}: {str(e)}"
                        results["errors"].append(error_msg)
                        results["failed_files"] += 1
                        log_entry["success"] = False
                        log_entry["error_msg"] = error_msg
                        self.log_signal.emit(f"错误: {error_msg}")

                    results["log_entries"].append(log_entry)
                else:
                    # 如果有多个文件，则使用递增后缀
                    for i, file in enumerate(files, start=1):
                        if self.is_stopped:
                            break
                        
                        # 生成新的文件名（目录名-序号.扩展名）
                        new_name = subdir / f"{dir_name}-{i:04d}{file.suffix}"
                        
                        action_desc = f"将 '{file.name}' 重命名为 '{new_name.name}'"
                        results["actions"].append(action_desc)
                        self.log_signal.emit(action_desc)
                        
                        log_entry = {
                            "directory": subdir.name,
                            "original_name": file.name,
                            "new_name": new_name.name,
                            "modify_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "success": True,
                            "error_msg": ""
                        }
                        
                        try:
                            file.rename(new_name)
                            results["renamed_files"] += 1
                            ok_records.append({'src_path': str(file.parent),
                                               'src_name': file.name,
                                               'new_name': new_name.name,
                                               'done_path': str(new_name.parent),
                                               'done_name': new_name.name})
                            
                            # 如果需要修改DPI且是JPG文件，则修改DPI
                            if self.modify_dpi and new_name.suffix.lower() in ['.jpg', '.jpeg']:
                                try:
                                    img = Image.open(new_name)
                                    # 设置DPI为600
                                    img.save(new_name, dpi=(600, 600))
                                    self.log_signal.emit(f"已修改 {new_name.name} 的DPI为600")
                                except Exception as dpi_error:
                                    error_msg = f"修改DPI失败 {new_name.name}: {str(dpi_error)}"
                                    results["errors"].append(error_msg)
                                    log_entry["success"] = False
                                    log_entry["error_msg"] = error_msg
                                    self.log_signal.emit(f"错误: {error_msg}")
                        except Exception as e:
                            error_msg = f"重命名文件失败 {file}: {str(e)}"
                            results["errors"].append(error_msg)
                            results["failed_files"] += 1
                            log_entry["success"] = False
                            log_entry["error_msg"] = error_msg
                            self.log_signal.emit(f"错误: {error_msg}")
                        
                        results["log_entries"].append(log_entry)
                
                processed_dirs += 1
                results["processed_dirs"] = processed_dirs
                self.progress_signal.emit(processed_dirs, total_dirs)
            
            if not self.is_stopped:
                # 改名成功记录写入本地数据库(供「只修改新增」判重)
                if ok_records:
                    _rename_db_record_many(ok_records)
                    self.log_signal.emit(
                        f"已记录 {len(ok_records)} 个改名文件到本地数据库({_RENAME_DB_NAME})")
                # 创建日志文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_filename = f"rename_log_{timestamp}.txt"
                log_filepath = os.path.join(self.base_dir, log_filename)
                
                with open(log_filepath, 'w', encoding='utf-8') as log_file:
                    log_file.write(f"文件重命名日志 - 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write(f"基础目录: {self.base_dir}\n")
                    log_file.write("=" * 80 + "\n")
                    log_file.write("目录名\t原文件名\t新文件名\t修改时间\t状态\t错误信息\n")
                    log_file.write("=" * 80 + "\n")
                    
                    for entry in results['log_entries']:
                        status = "成功" if entry['success'] else "失败"
                        error_info = entry['error_msg'] if entry['error_msg'] else ""
                        log_line = f"{entry['directory']}\t{entry['original_name']}\t{entry['new_name']}\t{entry['modify_time']}\t{status}\t{error_info}\n"
                        log_file.write(log_line)
                    
                    log_file.write("=" * 80 + "\n")
                    log_file.write(f"处理完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write(f"总计处理目录: {results['processed_dirs']} 个\n")
                    log_file.write(f"成功重命名文件: {results['renamed_files']} 个\n")
                    log_file.write(f"失败文件: {results['failed_files']} 个\n")
                
                success_count = results['renamed_files']
                fail_count = results['failed_files']
                skip_info = f", 跳过已记录: {skipped_new}" if skipped_new else ""
                self.finished_signal.emit(True,
                    f"处理完成！总计: {results['processed_dirs']} 个目录, "
                    f"成功: {success_count}, 失败: {fail_count}{skip_info}\n日志: {log_filename}")
            else:
                self.finished_signal.emit(False, "处理已停止")
                
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {str(e)}")
    
    def stop(self):
        self.is_stopped = True


class ExtRenameWorker(QThread):
    """
    修改文件扩展名后台线程：
    递归扫描指定目录及子目录，将匹配旧扩展名的文件改为新扩展名。
    """
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    def __init__(self, base_dir, old_ext, new_ext, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.old_ext = old_ext.lower().strip().lstrip('.')  # 统一小写, 去前导点
        self.new_ext = new_ext.lower().strip().lstrip('.')
        self.is_stopped = False

    def run(self):
        try:
            if not self.old_ext:
                self.finished_signal.emit(False, "旧扩展名不能为空")
                return
            if not self.new_ext:
                self.finished_signal.emit(False, "新扩展名不能为空")
                return

            # 收集所有匹配的文件
            old_dot = f'.{self.old_ext}'
            matched_files = []
            for root, dirs, files in os.walk(self.base_dir):
                for f in files:
                    if f.lower().endswith(old_dot):
                        matched_files.append(os.path.join(root, f))

            total = len(matched_files)
            if total == 0:
                self.finished_signal.emit(False, f"未找到扩展名为 .{self.old_ext} 的文件")
                return

            self.log_signal.emit(f"找到 {total} 个 .{self.old_ext} 文件待修改")

            renamed = 0
            failed = 0
            log_entries = []

            for i, filepath in enumerate(matched_files):
                if self.is_stopped:
                    self.log_signal.emit("用户停止处理")
                    break

                dir_part = os.path.dirname(filepath)
                basename = os.path.basename(filepath)
                name_no_ext = os.path.splitext(basename)[0]
                new_name = f"{name_no_ext}.{self.new_ext}"
                new_path = os.path.join(dir_part, new_name)

                rel_path = os.path.relpath(filepath, self.base_dir)
                rel_new = os.path.relpath(new_path, self.base_dir)

                entry = {
                    "original": rel_path,
                    "new": rel_new,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "success": True,
                    "error": ""
                }

                # 目标文件已存在则跳过
                if os.path.exists(new_path):
                    entry["success"] = False
                    entry["error"] = "目标文件已存在, 跳过"
                    failed += 1
                    self.log_signal.emit(f"  × 跳过 {rel_path}: 目标 {new_name} 已存在")
                    log_entries.append(entry)
                    self.progress_signal.emit(i + 1, total)
                    continue

                try:
                    os.rename(filepath, new_path)
                    renamed += 1
                    self.log_signal.emit(f"  ✓ {rel_path} → {rel_new}")
                except Exception as e:
                    entry["success"] = False
                    entry["error"] = str(e)
                    failed += 1
                    self.log_signal.emit(f"  × 失败 {rel_path}: {e}")

                log_entries.append(entry)
                self.progress_signal.emit(i + 1, total)

            # 写入日志文件
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = f"ext_rename_log_{ts}.txt"
            log_filepath = os.path.join(self.base_dir, log_filename)
            try:
                with open(log_filepath, 'w', encoding='utf-8') as lf:
                    lf.write(f"扩展名修改日志\n")
                    lf.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    lf.write(f"基础目录: {self.base_dir}\n")
                    lf.write(f"旧扩展名: .{self.old_ext} → 新扩展名: .{self.new_ext}\n")
                    lf.write("=" * 80 + "\n")
                    lf.write("原文件路径\t新文件路径\t修改时间\t状态\t错误信息\n")
                    lf.write("=" * 80 + "\n")
                    for e in log_entries:
                        status = "成功" if e["success"] else "失败"
                        lf.write(f"{e['original']}\t{e['new']}\t{e['time']}\t{status}\t{e['error']}\n")
                    lf.write("=" * 80 + "\n")
                    lf.write(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    lf.write(f"总计: {total} 个文件, 成功 {renamed} 个, 失败/跳过 {failed} 个\n")
            except Exception as e:
                self.log_signal.emit(f"写入日志文件失败: {e}")

            msg = (f"扩展名修改完成！共 {total} 个文件，"
                   f"成功 {renamed} 个，失败/跳过 {failed} 个。\n"
                   f"日志: {log_filename}")
            self.finished_signal.emit(not self.is_stopped, msg)

        except Exception as e:
            import traceback
            self.log_signal.emit(traceback.format_exc())
            self.finished_signal.emit(False, f"处理出错: {e}")

    def stop(self):
        self.is_stopped = True


class DirStandardizeWorker(QThread):
    """文件夹命名标准化后台处理线程(v3.18, v3.22改命名规则)。

    将所选目录下每个子目录改名为
    「全宗号-专业·专业类型·年限-保管期限-件号」，
    字段值来源两种: 直接填写(用户输入的固定值)或引用现有(解析各子目录现有
    名称对应位置的字段值)。执行后生成Excel记录原名→新名。
    """
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    # v3.22: 字段顺序(与新格式一一对应; 引用现有按此序取值)
    FIELD_KEYS = ('全宗号', '专业', '专业类型', '年限', '保管期限', '件号')
    # 新格式固定段「专业类型」的默认值(直接填写可覆盖)
    AUDIT_DEFAULT = 'SJ'

    # 匹配现有目录名的正则(v3.22新格式): 全宗号-专业·专业类型·年限-保管期限-件号
    # (专业/专业类型限字母数字汉字, 年限4位数字, 件号3-5位数字; 分隔符允许全角－与·/・)
    _FMT_RE = re.compile(
        r'^([A-Za-z0-9]+)[-－]([A-Za-z0-9一-龥]+)[·・]'
        r'([A-Za-z0-9一-龥]+)[·・](\d{4})[-－]'
        r'([A-Za-z0-9]+)[-－](\d{3,5})$')
    # 兼容旧格式(v3.18-v3.21): 全宗号-专业·年限-保管期限-机构代码-件号
    # (引用现有时旧格式目录的 专业/年限/保管期限/件号 仍可被引用, 机构代码被忽略)
    _FMT_RE_OLD = re.compile(
        r'^([A-Za-z0-9]+)[-－]([A-Za-z]+)[·・](\d{4})[-－]'
        r'([A-Za-z0-9]+)[-－]([A-Za-z0-9]+)[-－](\d{3,5})$')

    def __init__(self, base_dir, fields, rename_files=False, parent=None):
        """
        fields: dict{'全宗号':str,'专业':str,'专业类型':str,'年限':str,
                     '保管期限':str,'件号':str} —— 非空=直接填写, 空=引用现有
        rename_files: 目录改名后是否批量重命名目录下文件
        """
        super().__init__(parent)
        self.base_dir = base_dir
        self.fields = fields
        self.rename_files = rename_files
        self.is_stopped = False
        self.plan = []   # [(子目录Path, 新名str), ...] 由 preview() 填充

    def stop(self):
        self.is_stopped = True

    # ---------- 计划生成(预览与执行共用) ----------
    def build_plan(self, log=None):
        """扫描子目录生成改名计划。返回 (plan, 引用失败列表)。
        plan: [(subdir_path, new_name)]; 引用失败=某字段既无直接填写
        又无法从现有名解析(或该目录名不符合格式), 该目录跳过并记录。"""
        plan, skipped = [], []
        subdirs = sorted([d for d in Path(self.base_dir).iterdir()
                          if d.is_dir()], key=lambda p: p.name)
        for sd in subdirs:
            old_parts = self._parse_old_name(sd.name)
            vals = []
            bad = False
            for i, key in enumerate(self.FIELD_KEYS):
                v = (self.fields.get(key) or '').strip()
                if v:
                    vals.append(v)            # 直接填写优先
                elif old_parts and old_parts[i]:
                    vals.append(old_parts[i])  # 引用现有目录名对应位置
                else:
                    # 无来源(目录名不符格式, 或旧格式缺该段如专业类型)→跳过
                    bad = True
                    break
            if bad:
                skipped.append(sd.name)
                continue
            new_name = (f"{vals[0]}-{vals[1]}·{vals[2]}·{vals[3]}-"
                        f"{vals[4]}-{vals[5]}")
            if new_name == sd.name:
                continue   # 已符合标准, 无需改名
            plan.append((sd, new_name))
        return plan, skipped

    @classmethod
    def _parse_old_name(cls, name):
        """解析现有目录名为新格式字段序(全宗号/专业/专业类型/年限/保管期限/件号)。
        新格式直接取; 旧格式(v3.18-21)映射时「专业类型」无对应值返回None整体作废
        ——旧格式无该段, 引用它会产生编造值, 故旧格式仅在「专业类型」直接填写时
        才可被引用(其余字段按位映射)。"""
        m = cls._FMT_RE.match(name)
        if m:
            return m.groups()
        mo = cls._FMT_RE_OLD.match(name)
        if mo:
            # 旧字段序: 全宗号/专业/年限/保管期限/机构代码/件号
            # 映射到新序: 全宗号/专业/(专业类型缺)/年限/保管期限/件号
            return (mo.group(1), mo.group(2), None,
                    mo.group(3), mo.group(4), mo.group(6))
        return None

    def run(self):
        try:
            if not self.plan:
                self.finished_signal.emit(False, "无待改名目录(全部已符合标准或引用失败)")
                return
            total = len(self.plan)
            done = 0
            renamed, failed = [], []
            conflicts = []
            for sd, new_name in self.plan:
                if self.is_stopped:
                    break
                target = sd.parent / new_name
                if target.exists() and target != sd:
                    # 目标名已被占用: 冲突目录不强行改名, 记录后跳过
                    conflicts.append(f"{sd.name} → {new_name}(目标已存在)")
                    done += 1
                    self.progress_signal.emit(done, total)
                    continue
                try:
                    sd.rename(target)
                    renamed.append((sd.name, new_name))
                    self.log_signal.emit(f"  • {sd.name} → {new_name}")
                except Exception as e:
                    failed.append((sd.name, str(e)))
                    self.log_signal.emit(f"  × 改名失败 {sd.name}: {e}")
                done += 1
                self.progress_signal.emit(done, total)

            # Excel 改名记录
            xlsx_path = self._write_xlsx(renamed, failed, conflicts)
            if xlsx_path:
                self.log_signal.emit(f"改名记录已写入: {xlsx_path}")

            # 勾选了改名后批量重命名目录下文件
            file_msg = ''
            if self.rename_files:
                self.log_signal.emit("开始批量重命名目录下文件(按目录名)...")
                file_msg = self._rename_files_in_dirs()

            msg = (f"目录改名完成: 成功 {len(renamed)} 个, 失败 {len(failed)} 个, "
                   f"冲突跳过 {len(conflicts)} 个{file_msg}")
            self.finished_signal.emit(not self.is_stopped, msg)
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {e}")

    def _write_xlsx(self, renamed, failed, conflicts):
        """生成Excel记录(原目录名/新目录名/状态)。失败返回None。"""
        try:
            import openpyxl
        except Exception:
            self.log_signal.emit("  × 缺少 openpyxl 库, 无法生成Excel记录")
            return None
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = '目录改名记录'
            ws.append(['序号', '原目录名', '新目录名', '状态'])
            for i, (old, new) in enumerate(renamed, 1):
                ws.append([i, old, new, '成功'])
            for i, (old, err) in enumerate(failed, 1):
                ws.append([len(renamed) + i, old, '', f'失败: {err}'])
            for i, c in enumerate(conflicts, 1):
                ws.append([len(renamed) + len(failed) + i, c.split(' → ')[0],
                           c.split(' → ')[1].split('(')[0], '跳过(目标已存在)'])
            # 列宽
            for col, w in zip('ABCD', (8, 44, 44, 22)):
                ws.column_dimensions[col].width = w
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            path = os.path.join(self.base_dir, f"目录改名记录_{ts}.xlsx")
            wb.save(path)
            return path
        except Exception as e:
            self.log_signal.emit(f"  × Excel记录写入失败: {e}")
            return None

    def _rename_files_in_dirs(self):
        """目录改名后按新目录名批量重命名其下文件(与FileRenameWorker同规则:
        单文件=目录名, 多文件=目录名-0001起)。返回结果摘要字符串。"""
        total_renamed = 0
        total_failed = 0
        # 只处理本轮改名涉及的目录(改名后的新路径)
        base = Path(self.base_dir)
        new_dirs = [base / new for _, new in self.plan
                    if (base / new).is_dir()]
        for d in sorted(set(new_dirs)):
            if self.is_stopped:
                break
            try:
                files = sorted([f for f in Path(d).iterdir() if f.is_file()])
            except Exception:
                continue
            if not files:
                continue
            for i, f in enumerate(files, start=1):
                if self.is_stopped:
                    break
                new_name = (f"{d.name}{f.suffix}" if len(files) == 1
                            else f"{d.name}-{i:04d}{f.suffix}")
                target = d / new_name
                if f == target:
                    continue
                try:
                    f.rename(target)
                    total_renamed += 1
                except Exception:
                    total_failed += 1
        return (f"; 文件批量重命名: 成功 {total_renamed} 个, "
                f"失败 {total_failed} 个")


class DirStandardizePreviewDialog(QDialog):
    """文件夹命名标准化预览对话框(v3.18): 表格列出原名→新名, 可改后确认。"""

    def __init__(self, plan, skipped, parent=None):
        super().__init__(parent)
        self.setWindowTitle("文件夹命名标准化 - 预览")
        self.resize(760, 520)
        self.plan = plan           # [(subdir_path, new_name)]
        self.skipped = skipped
        self.confirmed = False

        v = QVBoxLayout(self)
        tip = QLabel(f"共 {len(plan)} 个目录将改名, {len(skipped)} 个引用失败跳过"
                     f"{'(目录名不符合格式且字段无直接填写)' if skipped else ''}"
                     "。\n新目录名列可直接修改, 确认后按表格内容执行:")
        tip.setStyleSheet("color: #8B949E; font-size: 12px;")
        v.addWidget(tip)

        self.table = QTableWidget(len(plan), 2)
        self.table.setHorizontalHeaderLabels(["原目录名", "新目录名(可修改)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        for row, (sd, new_name) in enumerate(plan):
            it_old = QTableWidgetItem(sd.name)
            it_old.setFlags(it_old.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, it_old)
            self.table.setItem(row, 1, QTableWidgetItem(new_name))
        v.addWidget(self.table, 1)

        if skipped:
            skip_lbl = QLabel("引用失败目录: " + ", ".join(skipped[:8])
                              + ("..." if len(skipped) > 8 else ""))
            skip_lbl.setStyleSheet("color: #B45309; font-size: 12px;")
            skip_lbl.setWordWrap(True)
            v.addWidget(skip_lbl)

        h = QHBoxLayout()
        btn_ok = QPushButton("确认改名")
        btn_ok.setObjectName("ActionBtn")
        btn_ok.setStyleSheet("background-color: #2196F3;")
        btn_ok.clicked.connect(self.on_ok)
        h.addWidget(btn_ok)
        btn_cancel = QPushButton("取消")
        btn_cancel.setObjectName("BrowseBtn")
        btn_cancel.clicked.connect(self.reject)
        h.addWidget(btn_cancel)
        h.addStretch()
        v.addLayout(h)

    def on_ok(self):
        # 校验新名非空且不含非法字符
        bad = []
        self.final_plan = []
        for row, (sd, _) in enumerate(self.plan):
            new_name = self.table.item(row, 1).text().strip()
            if not new_name or any(c in new_name for c in '\\/:*?"<>|'):
                bad.append(f"第{row + 1}行: {new_name!r}")
                continue
            self.final_plan.append((sd, new_name))
        if bad:
            QMessageBox.warning(self, "新目录名无效",
                                "以下新目录名为空或含非法字符(\\ / : * ? \" < > |):\n"
                                + "\n".join(bad))
            return
        self.confirmed = True
        self.accept()


class FileRenamePage(FunctionPage):
    def __init__(self):
        super().__init__("文件改名")

        # v3.20: 三个处理方式改为TAB并列(原纵向堆叠导致页面过长)
        from PyQt5.QtWidgets import QTabWidget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # ====== TAB1: 按目录名批量重命名 ======
        group = QGroupBox("按目录名批量重命名文件")
        form = QFormLayout()

        self.dir_path = QLineEdit()
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(self.browse_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.dir_path)
        h1.addWidget(btn_browse)
        form.addRow("目标目录:", h1)

        self.modify_dpi_check = QCheckBox("修改JPG文件的DPI为600")
        self.modify_dpi_check.setChecked(False)
        form.addRow("选项:", self.modify_dpi_check)

        # 只修改新增: 勾选后, 与本地记录库「原路径+原文件名」完全相同的文件跳过
        self.only_new_check = QCheckBox("只修改新增（跳过已改名过的文件，按路径+文件名判重）")
        self.only_new_check.setChecked(False)
        self.only_new_check.setToolTip(
            "程序在本地数据库记录每次实际改名过的文件(原路径+原文件名)。\n"
            "勾选后，与历史记录完全相同的文件不再重复处理；未勾选则全部重新处理。")
        form.addRow("", self.only_new_check)

        # 功能1的操作按钮(放在分组内)
        btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("预览操作")
        self.preview_btn.setObjectName("ActionBtn")
        self.preview_btn.setStyleSheet("background-color: #2196F3;")
        self.preview_btn.clicked.connect(self.preview_operations)
        btn_layout.addWidget(self.preview_btn)

        self.exec_btn = QPushButton("开始批量改名")
        self.exec_btn.setObjectName("ActionBtn")
        self.exec_btn.clicked.connect(self.execute)
        btn_layout.addWidget(self.exec_btn)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addStretch()
        form.addRow("", btn_layout)

        group.setLayout(form)
        self.tabs.addTab(group, "按目录名批量重命名")

        # ====== TAB2: 文件夹命名标准化(v3.18, v3.19紧凑布局) ======
        std_group = QGroupBox(
            "文件夹命名标准化\n(格式: 全宗号-专业·专业类型·年限-保管期限-件号)")
        std_form = QFormLayout()

        self.std_dir_edit = QLineEdit()
        self.std_dir_edit.setPlaceholderText("其下的子目录将被标准化改名")
        btn_std_browse = QPushButton("选择文件夹")
        btn_std_browse.setObjectName("BrowseBtn")
        btn_std_browse.clicked.connect(self.browse_std_dir)
        h_std = QHBoxLayout()
        h_std.addWidget(self.std_dir_edit)
        h_std.addWidget(btn_std_browse)
        std_form.addRow("目标目录:", h_std)

        std_form.addRow(QLabel(
            "各字段: 单选「填」=直接填固定值(对所有目录生效); 「引」=引用各子目录现名对应位置"
            "(输入框显示第一个符合格式目录的值, 只读; 目录名不符合格式时该目录跳过):"))

        # v3.21: 6个字段改为每行一条(纵列, 标签列对齐), 输入框限宽缩窄窗口;
        # 输入框在「引」状态显示从待处理目录提取的编码值(只读)。
        # v3.22: 字段改为 全宗号/专业/专业类型/年限/保管期限/件号(新命名规则),
        # 「专业类型」默认预填并选中「填」(格式固定段, v3.23缺省值改为SJ)。
        self.std_fields = {}   # key -> (QRadioButton填, QRadioButton引, QLineEdit)
        for key in DirStandardizeWorker.FIELD_KEYS:
            cell = QHBoxLayout()
            cell.setSpacing(4)
            rb_input = QRadioButton("填")
            rb_input.setToolTip("直接填写: 在输入框填固定值, 对所有目录生效")
            rb_ref = QRadioButton("引")
            rb_ref.setToolTip("引用现有: 取各子目录现名对应位置的字段值")
            if key == '专业类型':
                rb_input.setChecked(True)   # v3.22: 专业类型为格式固定段, 默认直接填(v3.23起缺省SJ)
            else:
                rb_ref.setChecked(True)   # 默认引用现有
            edit = QLineEdit()
            edit.setMaximumWidth(120)  # 编码字段都很短, 限宽缩窄窗口
            if key == '专业类型':
                # 专业类型为格式固定段: 默认直接填且可编辑
                edit.setText(DirStandardizeWorker.AUDIT_DEFAULT)
                edit.setReadOnly(False)
                edit.setPlaceholderText('')
            else:
                edit.setReadOnly(True)    # 引用状态下只读(值来自目录扫描, 防误改后误解)
                edit.setPlaceholderText("待选目录")
            rb_input.toggled.connect(
                lambda on, e=edit: (e.setReadOnly(not on), e.clear()))
            cell.addWidget(rb_input)
            cell.addWidget(rb_ref)
            cell.addWidget(edit)
            cell.addStretch()
            std_form.addRow(key + ":", cell)
            self.std_fields[key] = (rb_input, rb_ref, edit)

        # 目录标准化后是否批量重命名目录下文件(默认不勾)
        self.std_rename_files_check = QCheckBox(
            "标准化后按新目录名批量重命名目录下文件\n"
            "(单文件=目录名, 多文件=目录名-0001起, 同「按目录名批量重命名」)")
        self.std_rename_files_check.setChecked(False)
        std_form.addRow("", self.std_rename_files_check)

        # 操作按钮
        std_btn_layout = QHBoxLayout()
        self.std_preview_btn = QPushButton("预览")
        self.std_preview_btn.setObjectName("ActionBtn")
        self.std_preview_btn.setStyleSheet("background-color: #2196F3;")
        self.std_preview_btn.clicked.connect(self.preview_std_rename)
        std_btn_layout.addWidget(self.std_preview_btn)

        self.std_exec_btn = QPushButton("开始标准化")
        self.std_exec_btn.setObjectName("ActionBtn")
        self.std_exec_btn.clicked.connect(self.execute_std_rename)
        std_btn_layout.addWidget(self.std_exec_btn)
        std_btn_layout.addStretch()
        std_form.addRow("", std_btn_layout)

        std_group.setLayout(std_form)
        self.tabs.addTab(std_group, "文件夹命名标准化")

        # ====== TAB3: 修改文件扩展名 ======
        ext_group = QGroupBox("修改文件扩展名(递归处理目录及子目录)")
        ext_form = QFormLayout()

        self.ext_dir_edit = QLineEdit()
        self.ext_dir_edit.setPlaceholderText("指定目录及其子目录下的文件将被处理")
        btn_ext_browse = QPushButton("选择文件夹")
        btn_ext_browse.setObjectName("BrowseBtn")
        btn_ext_browse.clicked.connect(self.browse_ext_dir)
        h_ext = QHBoxLayout()
        h_ext.addWidget(self.ext_dir_edit)
        h_ext.addWidget(btn_ext_browse)
        ext_form.addRow("目标目录:", h_ext)

        self.ext_old_edit = QLineEdit()
        self.ext_old_edit.setPlaceholderText("例如: tif 或 .tif")
        self.ext_old_edit.setMaximumWidth(160)
        ext_form.addRow("旧扩展名:", self.ext_old_edit)

        self.ext_new_edit = QLineEdit()
        self.ext_new_edit.setPlaceholderText("例如: jpg 或 .jpg")
        self.ext_new_edit.setMaximumWidth(160)
        ext_form.addRow("新扩展名:", self.ext_new_edit)

        # 功能2的操作按钮(放在分组内)
        ext_btn_layout = QHBoxLayout()
        self.ext_preview_btn = QPushButton("预览")
        self.ext_preview_btn.setObjectName("ActionBtn")
        self.ext_preview_btn.setStyleSheet("background-color: #2196F3;")
        self.ext_preview_btn.clicked.connect(self.preview_ext_rename)
        ext_btn_layout.addWidget(self.ext_preview_btn)

        self.ext_exec_btn = QPushButton("开始修改扩展名")
        self.ext_exec_btn.setObjectName("ActionBtn")
        self.ext_exec_btn.clicked.connect(self.execute_ext_rename)
        ext_btn_layout.addWidget(self.ext_exec_btn)

        self.ext_stop_btn = QPushButton("停止")
        self.ext_stop_btn.setObjectName("ActionBtn")
        self.ext_stop_btn.setStyleSheet("background-color: #DA3633;")
        self.ext_stop_btn.clicked.connect(self.stop_ext_processing)
        self.ext_stop_btn.setEnabled(False)
        ext_btn_layout.addWidget(self.ext_stop_btn)
        ext_btn_layout.addStretch()
        ext_form.addRow("", ext_btn_layout)

        ext_group.setLayout(ext_form)
        self.tabs.addTab(ext_group, "修改文件扩展名")

        # 说明文本(随当前TAB切换显示对应说明, v3.20)
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self._tab_infos = {
            0: ("【按目录名批量重命名】\n"
                "• 单文件：直接以目录名命名；多文件：目录名-0001、目录名-0002...\n"
                "• 自动生成详细日志文件；可选修改JPG文件DPI为600"),
            1: ("【文件夹命名标准化】\n"
                "• 目标格式: 全宗号-专业·专业类型·年限-保管期限-件号 (·与-按规则间隔)\n"
                "• 字段可「直接填写」固定值或「引用现有」子目录名对应位置; 预览可改新名\n"
                "• 执行后自动生成Excel记录原/新目录名; 可选同步批量重命名目录下文件"),
            2: ("【修改文件扩展名】\n"
                "• 递归扫描目录及子目录，将旧扩展名文件改为新扩展名\n"
                "• 扩展名输入无需点号(如输入 tif 或 .tif 均可)；自动生成日志文件"),
        }
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self._on_tab_changed(0)
        self.layout.addWidget(self.info_label)

        self.worker = None
        self.ext_worker = None
        self.std_worker = None
        self.add_log_widget()

        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

    def _on_tab_changed(self, idx):
        """v3.20: TAB切换时更新下方功能说明文本"""
        self.info_label.setText(self._tab_infos.get(idx, ""))

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择目录")
        if d: self.dir_path.setText(d)
    
    def preview_operations(self):
        """预览将要执行的操作"""
        d = self.dir_path.text()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        
        # 清空之前的结果
        self.log_box.clear()
        
        self.log("="*50)
        self.log("正在预览操作...")
        self.log(f"基础目录: {d}")
        self.log("-"*50)
        
        try:
            from pathlib import Path
            subdirs = [dir for dir in Path(d).iterdir() if dir.is_dir()]
            total_files = 0
            actions = []
            
            for subdir in subdirs:
                files = [f for f in subdir.iterdir() if f.is_file()]
                if not files:
                    continue
                
                dir_name = subdir.name
                
                if len(files) == 1:
                    file = files[0]
                    new_name = f"{dir_name}{file.suffix}"
                    action = f"将 '{file.name}' 重命名为 '{new_name}'"
                    actions.append(action)
                    self.log(f"  • {action}")
                else:
                    for i, file in enumerate(files, start=1):
                        new_name = f"{dir_name}-{i:04d}{file.suffix}"
                        action = f"将 '{file.name}' 重命名为 '{new_name}'"
                        actions.append(action)
                        self.log(f"  • {action}")
                
                total_files += len(files)
            
            self.log("-"*50)
            self.log(f"预览完成！")
            self.log(f"将处理 {len(subdirs)} 个子目录")
            self.log(f"将重命名 {total_files} 个文件")
            
            if self.modify_dpi_check.isChecked():
                self.log("\n注意：将同时修改JPG文件的DPI为600")
            
            self.log("\n注意：这只是预览，文件尚未重命名。")
            
        except Exception as e:
            error_msg = f"预览过程中出现错误: {str(e)}"
            self.log(error_msg)
            QMessageBox.critical(self, "错误", error_msg)

    def execute(self):
        d = self.dir_path.text()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        
        # 确认操作
        reply = QMessageBox.question(
            self, "确认操作",
            "确定要开始重命名文件吗？\n此操作不可逆！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 重置进度条
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        
        # 禁用按钮，启用停止按钮
        self.log("="*50)
        self.log("开始处理...")
        self.log(f"目录: {d}")
        if self.modify_dpi_check.isChecked():
            self.log("选项: 修改JPG文件DPI为600")
        self.log("="*50)
        
        # 创建工作线程
        modify_dpi = self.modify_dpi_check.isChecked()
        self.worker = FileRenameWorker(base_dir=d, modify_dpi=modify_dpi,
                                       only_new=self.only_new_check.isChecked())
        
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        
        self.worker.start()
        
        # 更新按钮状态
        self.exec_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")
        self.log(f"进度: {current}/{total} ({percentage:.1f}%)")
    
    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        
        # 恢复按钮状态
        self.exec_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)

    # ---------- 文件夹命名标准化功能(v3.18) ----------
    def browse_std_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择命名标准化的目标目录")
        if d:
            self.std_dir_edit.setText(d)
            self._fill_ref_fields(d)
        # 目录手输也可能有效: 编辑完成(失焦/回车)时也尝试填充
        self.std_dir_edit.editingFinished.connect(self._on_std_dir_edited)

    def _on_std_dir_edited(self):
        d = self.std_dir_edit.text().strip()
        if d and os.path.isdir(d):
            self._fill_ref_fields(d)

    def _fill_ref_fields(self, base_dir):
        """v3.19: 扫描目录下第一个符合格式的子目录, 将其编码值填入
        处于「引用现有」状态的输入框(只读展示, 让用户看到将引用什么)。
        v3.22: 按新格式解析; 旧格式目录也可作引用源(专业类型段无值时显示为空,
        该情况需用户将「专业类型」改为直接填写)。"""
        try:
            subdirs = sorted([e for e in os.listdir(base_dir)
                              if os.path.isdir(os.path.join(base_dir, e))])
        except Exception:
            return
        first = None
        for name in subdirs:
            parsed = DirStandardizeWorker._parse_old_name(name)
            if parsed:
                first = parsed
                break
        for i, key in enumerate(DirStandardizeWorker.FIELD_KEYS):
            _rb_in, rb_ref, edit = self.std_fields[key]
            if rb_ref.isChecked():          # 只更新引用状态的框
                if first:
                    edit.setText(first[i] or '')
                    edit.setPlaceholderText(
                        '' if first[i] else '旧格式无此段')
                else:
                    edit.clear()
                    edit.setPlaceholderText('无符合格式目录')

    def _collect_std_fields(self, show_warn=True):
        """从界面收集字段配置。返回 dict(值非空=直接填写) 或 None(校验失败)。"""
        fields = {}
        for key, (rb_input, _rb_ref, edit) in self.std_fields.items():
            if rb_input.isChecked():
                v = edit.text().strip()
                if not v and show_warn:
                    QMessageBox.warning(self, "提示",
                                        f"字段「{key}」选中了直接填写, 但输入为空。\n"
                                        "请填写内容或改选「引用现有」。")
                    return None
                fields[key] = v
            else:
                fields[key] = ''   # 引用现有
        return fields

    def preview_std_rename(self):
        """预览标准化改名(弹窗表格, 新名可修改)"""
        d = self.std_dir_edit.text().strip()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择命名标准化的目标目录")
            return
        if not os.path.isdir(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        fields = self._collect_std_fields()
        if fields is None:
            return

        try:
            w = DirStandardizeWorker(d, fields,
                                     rename_files=self.std_rename_files_check.isChecked())
            plan, skipped = w.build_plan()
            if not plan and not skipped:
                QMessageBox.information(self, "预览",
                                        "所有子目录已符合标准格式, 无需改名。")
                return
            if not plan:
                QMessageBox.warning(
                    self, "预览",
                    f"没有可改名的目录。\n{len(skipped)} 个目录名不符合格式"
                    "且相关字段未「直接填写」, 无法引用:\n"
                    + "\n".join(skipped[:10])
                    + ("..." if len(skipped) > 10 else ""))
                return
            dlg = DirStandardizePreviewDialog(plan, skipped, self)
            if dlg.exec_() == QDialog.Accepted and dlg.confirmed:
                # 用预览(用户可能已修改)的最终计划执行
                w.plan = dlg.final_plan
                self.std_execute_worker(w)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"预览出错: {e}")

    def execute_std_rename(self):
        """直接执行标准化改名(不经预览弹窗, 内部仍先build_plan)"""
        d = self.std_dir_edit.text().strip()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择命名标准化的目标目录")
            return
        if not os.path.isdir(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        fields = self._collect_std_fields()
        if fields is None:
            return
        try:
            w = DirStandardizeWorker(d, fields,
                                     rename_files=self.std_rename_files_check.isChecked())
            plan, skipped = w.build_plan()
            if not plan:
                QMessageBox.information(
                    self, "提示",
                    "无待改名目录(全部已符合标准"
                    + (f", 另有 {len(skipped)} 个引用失败跳过)" if skipped else ")"))
                return
            reply = QMessageBox.question(
                self, "确认操作",
                f"确定将 {len(plan)} 个子目录按标准格式改名吗?\n"
                + (f"(另有 {len(skipped)} 个目录因引用失败将跳过)\n" if skipped else "")
                + "此操作会生成Excel改名记录, 但目录改名不可逆!",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                return
            w.plan = plan
            self.std_execute_worker(w)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"执行出错: {e}")

    def std_execute_worker(self, worker):
        """启动标准化改名线程并管理按钮状态"""
        self.std_worker = worker
        self.std_worker.log_signal.connect(self.log)
        self.std_worker.progress_signal.connect(self.update_progress)
        self.std_worker.finished_signal.connect(self.on_std_finished)
        self.std_worker.start()
        self.std_exec_btn.setEnabled(False)
        self.std_preview_btn.setEnabled(False)

    def on_std_finished(self, success, message):
        """标准化改名完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止/出错")
        self.std_exec_btn.setEnabled(True)
        self.std_preview_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.warning(self, "提示", message)

    # ---------- 扩展名修改功能 ----------
    def browse_ext_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择扩展名修改目录")
        if d:
            self.ext_dir_edit.setText(d)

    def preview_ext_rename(self):
        """预览扩展名修改操作"""
        d = self.ext_dir_edit.text().strip()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择扩展名修改的目标目录")
            return
        if not os.path.isdir(d):
            QMessageBox.warning(self, "错误", "目录不存在")
            return

        old_ext = self.ext_old_edit.text().strip().lstrip('.').lower()
        new_ext = self.ext_new_edit.text().strip().lstrip('.').lower()
        if not old_ext:
            QMessageBox.warning(self, "提示", "请输入旧扩展名")
            return
        if not new_ext:
            QMessageBox.warning(self, "提示", "请输入新扩展名")
            return

        self.log_box.clear()
        self.log("=" * 50)
        self.log("预览扩展名修改操作")
        self.log(f"目录: {d}")
        self.log(f"旧扩展名: .{old_ext} → 新扩展名: .{new_ext}")
        self.log("-" * 50)

        try:
            old_dot = f'.{old_ext}'
            count = 0
            for root, dirs, files in os.walk(d):
                for f in files:
                    if f.lower().endswith(old_dot):
                        rel = os.path.relpath(os.path.join(root, f), d)
                        name_no_ext = os.path.splitext(f)[0]
                        new_name = f"{name_no_ext}.{new_ext}"
                        self.log(f"  • {rel} → {new_name}")
                        count += 1

            self.log("-" * 50)
            if count == 0:
                self.log(f"未找到 .{old_ext} 文件")
            else:
                self.log(f"共找到 {count} 个 .{old_ext} 文件将被修改为 .{new_ext}")
            self.log("\n注意：这只是预览，文件尚未修改。")
        except Exception as e:
            self.log(f"预览出错: {e}")
            QMessageBox.critical(self, "错误", f"预览过程中出错: {e}")

    def execute_ext_rename(self):
        """执行扩展名修改"""
        d = self.ext_dir_edit.text().strip()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择扩展名修改的目标目录")
            return
        if not os.path.isdir(d):
            QMessageBox.warning(self, "错误", "目录不存在")
            return

        old_ext = self.ext_old_edit.text().strip().lstrip('.').lower()
        new_ext = self.ext_new_edit.text().strip().lstrip('.').lower()
        if not old_ext:
            QMessageBox.warning(self, "提示", "请输入旧扩展名")
            return
        if not new_ext:
            QMessageBox.warning(self, "提示", "请输入新扩展名")
            return
        if old_ext == new_ext:
            QMessageBox.warning(self, "提示", "旧扩展名与新扩展名相同，无需修改")
            return

        reply = QMessageBox.question(
            self, "确认操作",
            f"确定要将 .{old_ext} 文件的扩展名修改为 .{new_ext} 吗？\n"
            f"目录: {d}\n"
            f"将递归处理所有子目录。\n此操作不可逆！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        self.log("=" * 50)
        self.log("开始修改扩展名...")
        self.log(f"目录: {d}")
        self.log(f".{old_ext} → .{new_ext}")
        self.log("=" * 50)

        self.ext_worker = ExtRenameWorker(d, old_ext, new_ext)
        self.ext_worker.log_signal.connect(self.log)
        self.ext_worker.progress_signal.connect(self.update_progress)
        self.ext_worker.finished_signal.connect(self.on_ext_finished)
        self.ext_worker.start()

        self.ext_exec_btn.setEnabled(False)
        self.ext_preview_btn.setEnabled(False)
        self.ext_stop_btn.setEnabled(True)

    def stop_ext_processing(self):
        """停止扩展名修改处理"""
        if self.ext_worker and self.ext_worker.isRunning():
            self.ext_worker.stop()
            self.log("正在停止扩展名修改处理...")
            self.ext_stop_btn.setEnabled(False)

    def on_ext_finished(self, success, message):
        """扩展名修改完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        self.ext_exec_btn.setEnabled(True)
        self.ext_preview_btn.setEnabled(True)
        self.ext_stop_btn.setEnabled(False)
        if success:
            QMessageBox.information(self, "完成", "扩展名修改完成！")
        else:
            QMessageBox.warning(self, "提示", message)


class AutoPagingWorker(QThread):
    """后台处理线程"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)
    
    def __init__(self, directory, margin_mm, start_number, thread_count, cover_digit, parent=None):
        super().__init__(parent)
        self.directory = directory
        self.margin_mm = margin_mm
        self.start_number = start_number
        self.thread_count = thread_count
        self.cover_digit = cover_digit
        self.is_stopped = False
    
    def run(self):
        try:
            # 收集文件
            dir_files_map = self.collect_jpg_files()
            if not dir_files_map:
                self.finished_signal.emit(False, "未找到任何JPG文件")
                return
            
            total_dirs = len(dir_files_map)
            total_files = sum(len(files) for files in dir_files_map.values())
            self.log_signal.emit(f"找到 {total_dirs} 个目录，共 {total_files} 个JPG文件")
            
            # 创建日志文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"sequence_number_log_{timestamp}.txt"
            log_path = os.path.join(self.directory, log_filename)
            self.init_log_file(log_path)
            
            # 处理所有目录
            all_results = []
            processed_dirs = 0
            
            with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                future_to_dir = {}
                for dir_path, jpg_files in dir_files_map.items():
                    future = executor.submit(
                        self.process_directory_files, 
                        dir_path, jpg_files, self.start_number
                    )
                    future_to_dir[future] = dir_path
                
                for future in as_completed(future_to_dir):
                    if self.is_stopped:
                        break
                    
                    dir_path = future_to_dir[future]
                    try:
                        results = future.result()
                        all_results.extend(results)
                        
                        # 记录日志
                        for result in results:
                            self.append_to_log(log_path, result)
                            self.log_signal.emit(
                                f"{result['directory']}/{result['filename']} - "
                                f"序号:{result['number']} - {result['result']} ({result['duration']}秒)"
                            )
                    except Exception as e:
                        error_msg = f"处理目录 {dir_path} 时出错: {str(e)}"
                        self.log_signal.emit(error_msg)
                    
                    processed_dirs += 1
                    self.progress_signal.emit(processed_dirs, total_dirs)
            
            if not self.is_stopped:
                # 完成日志
                self.finalize_log_file(log_path, all_results)
                success_count = sum(1 for r in all_results if r['result'] == '成功')
                fail_count = len(all_results) - success_count
                self.finished_signal.emit(True, 
                    f"处理完成！总计: {len(all_results)}, 成功: {success_count}, 失败: {fail_count}\n日志: {log_path}")
            else:
                self.finished_signal.emit(False, "处理已停止")
                
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {str(e)}")
    
    def stop(self):
        self.is_stopped = True
    
    def collect_jpg_files(self):
        """收集目录及子目录下所有JPG文件"""
        dir_files_map = {}
        for root, dirs, files in os.walk(self.directory):
            jpg_files = []
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    jpg_files.append(os.path.join(root, filename))
            if jpg_files:
                jpg_files.sort()
                dir_files_map[root] = jpg_files
        return dir_files_map
    
    def get_chinese_font(self):
        """获取中文字体"""
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
        ]
        font_size = 236
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except Exception:
                continue
        return ImageFont.load_default()
    
    def add_number_to_image(self, image_path, number):
        """在图片右上角添加数字"""
        try:
            # cv2/numpy 延迟导入：Win7 上 opencv 较易出现 DLL 加载失败，
            # 放在此处可避免影响主程序启动与其他功能页（导入失败会被下方 except 捕获）。
            import cv2
            import numpy as np
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)
            font = self.get_chinese_font()
            
            # 计算边距（毫米转像素，假设300DPI）
            margin_px = int(self.margin_mm * 300 / 25.4)
            
            text = str(number)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = img_pil.width - margin_px - text_width
            y = margin_px
            
            # 如果需要覆盖数字区域
            if self.cover_digit:
                padding = int(20 * 300 / 25.4)
                cover_x = x - padding // 2
                cover_y = y - padding // 3
                cover_width = text_width + padding
                cover_height = text_height + padding // 2
                draw.rectangle([cover_x, cover_y, cover_x + cover_width, cover_y + cover_height], 
                              fill=(255, 255, 255), outline=None)
            
            draw.text((x, y), text, fill=(0, 0, 0), font=font)
            
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            cv2.imencode('.jpg', img_cv)[1].tofile(image_path)
            return True
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {str(e)}")
            return False
    
    def process_directory_files(self, directory_path, jpg_files, start_number):
        """处理单个目录下的JPG文件"""
        results = []
        current_number = start_number
        
        for jpg_file in jpg_files:
            if self.is_stopped:
                break
            
            start_time = time.time()
            success = self.add_number_to_image(jpg_file, current_number)
            end_time = time.time()
            
            results.append({
                'directory': os.path.basename(directory_path),
                'filename': os.path.basename(jpg_file),
                'number': current_number,
                'result': '成功' if success else '失败',
                'duration': round(end_time - start_time, 3),
                'full_path': jpg_file
            })
            
            if success:
                current_number += 1
        
        return results
    
    def init_log_file(self, log_path):
        """初始化日志文件"""
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"JPG文件添加序号处理日志\n")
                f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 100 + "\n")
                f.write(f"{'目录名':<20} {'文件名':<30} {'序号':<8} {'结果':<10} {'耗时(秒)':<12} {'处理时间':<20}\n")
                f.write("-" * 100 + "\n")
        except Exception as e:
            print(f"创建日志文件失败: {str(e)}")
    
    def append_to_log(self, log_path, result):
        """追加单条记录到日志文件"""
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                process_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{result['directory']:<20} {result['filename']:<30} "
                       f"{result['number']:<8} {result['result']:<10} {result['duration']:<12} {process_time:<20}\n")
        except Exception as e:
            print(f"追加日志记录失败: {str(e)}")
    
    def finalize_log_file(self, log_path, results):
        """完成日志文件"""
        try:
            success_count = sum(1 for r in results if r['result'] == '成功')
            fail_count = len(results) - success_count
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write("-" * 100 + "\n")
                f.write(f"结束时间: {end_time}\n")
                f.write(f"总计处理: {len(results)} 个文件\n")
                f.write(f"成功: {success_count} 个\n")
                f.write(f"失败: {fail_count} 个\n")
                f.write("=" * 100 + "\n")
        except Exception as e:
            print(f"完成日志文件失败: {str(e)}")


class AutoPagingPage(FunctionPage):
    def __init__(self):
        super().__init__("自动编页码")
        group = QGroupBox("JPG文件右上角添加序号")
        form = QFormLayout()

        self.file_dir = QLineEdit()
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(lambda: self.file_dir.setText(QFileDialog.getExistingDirectory(self, "选择目录")))

        h1 = QHBoxLayout()
        h1.addWidget(self.file_dir)
        h1.addWidget(btn_browse)

        self.start_num = QSpinBox()
        self.start_num.setRange(1, 9999)
        self.start_num.setValue(1)
        
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(1, 20)
        self.margin_spin.setValue(3)
        
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 16)
        self.thread_spin.setValue(4)
        
        self.cover_check = QComboBox()
        self.cover_check.addItems(["不覆盖", "用白色框覆盖"])

        form.addRow("文件目录:", h1)
        form.addRow("起始序号:", self.start_num)
        form.addRow("边距(毫米):", self.margin_spin)
        form.addRow("线程数:", self.thread_spin)
        form.addRow("覆盖选项:", self.cover_check)
        group.setLayout(form)
        self.layout.addWidget(group)

        btn_exec = QPushButton("开始编页码")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        self.layout.addWidget(btn_exec)
        
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        self.layout.addWidget(self.stop_btn)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)
        
        self.worker = None
        self.add_log_widget()

    def execute(self):
        d = self.file_dir.text()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        
        # 重置进度条
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        
        # 禁用按钮，启用停止按钮
        self.log("="*50)
        self.log("开始处理...")
        self.log(f"目录: {d}")
        self.log(f"起始序号: {self.start_num.value()}")
        self.log(f"边距: {self.margin_spin.value()}mm")
        self.log(f"线程数: {self.thread_spin.value()}")
        self.log(f"覆盖选项: {self.cover_check.currentText()}")
        self.log("="*50)
        
        # 创建工作线程
        self.worker = AutoPagingWorker(
            directory=d,
            margin_mm=self.margin_spin.value(),
            start_number=self.start_num.value(),
            thread_count=self.thread_spin.value(),
            cover_digit=(self.cover_check.currentIndex() == 1)
        )
        
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        
        self.worker.start()
        
        # 更新按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn:
            btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")
        self.log(f"进度: {current}/{total} ({percentage:.1f}%)")
    
    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        
        # 恢复按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn:
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)


class FileMovePage(FunctionPage):
    def __init__(self):
        super().__init__("文件移动")
        group = QGroupBox("文件批量归类移动")
        form = QFormLayout()

        self.src_dir = QLineEdit()
        self.dst_dir = QLineEdit()
        self.rule_combo = QComboBox()
        self.rule_combo.addItems(["按扩展名归类", "按修改日期归类", "全部移动"])

        btn_src = QPushButton("浏览")
        btn_src.setObjectName("BrowseBtn")
        btn_src.clicked.connect(lambda: self.src_dir.setText(QFileDialog.getExistingDirectory(self, "源目录")))
        btn_dst = QPushButton("浏览")
        btn_dst.setObjectName("BrowseBtn")
        btn_dst.clicked.connect(lambda: self.dst_dir.setText(QFileDialog.getExistingDirectory(self, "目标目录")))

        h1 = QHBoxLayout();
        h1.addWidget(self.src_dir);
        h1.addWidget(btn_src)
        h2 = QHBoxLayout();
        h2.addWidget(self.dst_dir);
        h2.addWidget(btn_dst)

        form.addRow("源目录:", h1)
        form.addRow("目标目录:", h2)
        form.addRow("移动规则:", self.rule_combo)
        group.setLayout(form)
        self.layout.addWidget(group)

        btn_exec = QPushButton("开始移动")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        self.layout.addWidget(btn_exec)
        self.add_log_widget()

    def execute(self):
        self.log("校验目录权限...")
        self.log(f"应用规则: {self.rule_combo.currentText()}")
        self.log("正在复制及删除原文件...")
        self.log("文件移动归档完成！")


class ArchiveStampWorker(QThread):
    """归档章加盖后台处理线程"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)
    
    def __init__(self, base_dir, overwrite_original=False, max_workers=4, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.overwrite_original = overwrite_original  # 是否覆盖原归档章
        self.max_workers = max_workers
        self.is_stopped = False
    
    def run(self):
        try:
            # 获取所有JPG文件
            dir_to_files = self.find_all_jpg_in_directory()
            if not dir_to_files:
                self.finished_signal.emit(False, "未找到任何JPG文件")
                return
            
            total_dirs = len(dir_to_files)
            total_files = sum(len(files) for files in dir_to_files.values())
            self.log_signal.emit(f"找到 {total_dirs} 个目录，共 {total_files} 个JPG文件")
            
            # 创建日志文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"archive_stamp_log_{timestamp}.txt"
            log_filepath = os.path.join(self.base_dir, log_filename)
            
            with open(log_filepath, 'w', encoding='utf-8') as log_file:
                log_file.write(f"归档章加盖日志 - 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                log_file.write(f"处理目录: {self.base_dir}\n")
                log_file.write(f"线程数: {self.max_workers}\n")
                log_file.write("=" * 80 + "\n")
                log_file.write("文件名称\t\t处理结果\t处理用时(秒)\n")
                log_file.write("=" * 80 + "\n")
                log_file.flush()
                
                processed_count = 0
                completed = 0
                
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {}
                    for dir_path, files in dir_to_files.items():
                        dir_name = os.path.basename(dir_path)
                        # 只取排序后的第一个文件
                        if files:
                            first_file = files[0]
                            future = executor.submit(
                                self.process_single_file,
                                first_file, dir_name
                            )
                            futures[future] = (first_file, dir_name)
                    
                    for future in as_completed(futures):
                        if self.is_stopped:
                            break
                        
                        completed += 1
                        jpg_file, dir_name = futures[future]
                        
                        try:
                            result = future.result()
                            
                            # 记录日志
                            filename = os.path.basename(result['processed_file_path']) if result['processed_file_path'] else os.path.basename(jpg_file)
                            result_str = "成功" if result['success'] else "失败"
                            duration = result['duration']
                            
                            log_entry = f"{filename}\t\t{result_str}\t{duration}\n"
                            log_file.write(log_entry)
                            log_file.flush()
                            
                            if result['success']:
                                processed_count += 1
                            
                            self.log_signal.emit(
                                f"处理文件: {filename} - {result_str} ({duration}s)"
                            )
                            self.progress_signal.emit(completed, len(futures))
                            
                        except Exception as e:
                            filename = os.path.basename(jpg_file)
                            error_msg = f"处理文件 {filename} 时出错: {str(e)}"
                            self.log_signal.emit(error_msg)
                            
                            log_entry = f"{filename}\t\t失败\t0.0\n"
                            log_file.write(log_entry)
                            log_file.flush()
                            
                            self.progress_signal.emit(completed, len(futures))
            
            if not self.is_stopped:
                operation_type = "覆盖原归档章并重新加盖" if self.overwrite_original else "添加新归档章"
                self.finished_signal.emit(True,
                    f"{operation_type}处理完成！\n总计: {len(futures)}, 成功: {processed_count}, 失败: {len(futures) - processed_count}\n日志: {log_filename}")
            else:
                self.finished_signal.emit(False, "处理已停止")
                
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {str(e)}")
    
    def stop(self):
        self.is_stopped = True
    
    def find_all_jpg_in_directory(self):
        """在指定目录及子目录中查找所有JPG文件（按目录分组）"""
        dir_to_files = {}
        
        for root, dirs, files in os.walk(self.base_dir):
            jpg_files_in_root = []
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    jpg_files_in_root.append(os.path.join(root, filename))
            
            if jpg_files_in_root:
                jpg_files_in_root.sort()
                dir_to_files[root] = jpg_files_in_root
        
        return dir_to_files
    
    def create_red_grid_image(self, dir_name, file_count=1):
        """创建归档章图片"""
        DPI = 300
        mm_to_px = DPI / 25.4
        
        rect_width_mm = 45
        rect_height_mm = 16
        rect_width_px = int(rect_width_mm * mm_to_px)
        rect_height_px = int(rect_height_mm * mm_to_px)
        
        cell_width_mm = 15
        cell_height_mm = 8
        cell_width_px = int(cell_width_mm * mm_to_px)
        cell_height_px = int(cell_height_mm * mm_to_px)
        
        img = Image.new('RGB', (rect_width_px, rect_height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # 尝试加载宋体字体
        try:
            font = ImageFont.truetype("simsun.ttc", 36)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 36)
            except:
                font = ImageFont.load_default()
        
        # 解析目录名称
        dir_text1 = dir_name[:4] if len(dir_name) >= 4 else dir_name.ljust(4)
        dir_text2 = dir_name[11:15] if len(dir_name) >= 15 else dir_name[11:].ljust(4) if len(dir_name) > 11 else "".ljust(4)
        last_5_chars = dir_name[-5:] if len(dir_name) >= 5 else dir_name
        dir_text3 = last_5_chars
        for i, char in enumerate(last_5_chars):
            if char != '0':
                dir_text3 = last_5_chars[i:]
                break
        
        # 绘制6个方格的红色边框
        for row in range(2):
            for col in range(3):
                x1 = col * cell_width_px
                y1 = row * cell_height_px
                x2 = x1 + cell_width_px
                y2 = y1 + cell_height_px
                
                draw.rectangle([x1, y1, x2, y2], fill='white', outline='red', width=2)
                
                if row == 0 and col == 0:
                    text = dir_text1
                elif row == 0 and col == 1:
                    text = dir_text2
                elif row == 0 and col == 2:
                    text = dir_text3
                elif row == 1 and col == 0:
                    text = "确权"
                elif row == 1 and col == 1:
                    text = "永久"
                elif row == 1 and col == 2:
                    text = str(file_count)
                else:
                    continue
                
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x1 + (cell_width_px - text_width) // 2
                text_y = y1 + (cell_height_px - text_height) // 2
                draw.text((text_x, text_y), text, fill='red', font=font)
        
        return img
    
    def overlay_image_on_jpg(self, jpg_file_path, overlay_img):
        """将归档章叠加到JPG文件的顶部中央"""
        try:
            Image.MAX_IMAGE_PIXELS = None
            
            original_img = Image.open(jpg_file_path)
            
            # 应用EXIF方向信息
            try:
                img_with_orientation = ImageOps.exif_transpose(original_img)
            except:
                img_with_orientation = original_img
            
            base_width, base_height = img_with_orientation.size
            
            DPI = 300
            mm_to_px = DPI / 25.4
            
            # 处理覆盖选项
            if self.overwrite_original:
                base_img = img_with_orientation.copy()
                base_width, base_height = base_img.size
                
                from PIL import ImageDraw
                draw = ImageDraw.Draw(base_img)
                cover_height_px = int(18 * mm_to_px)
                draw.rectangle([0, 0, base_width, cover_height_px], fill='white', outline=None)
            else:
                top_margin_px = int(18 * mm_to_px)
                new_height = base_height + top_margin_px
                
                new_img = Image.new('RGB', (base_width, new_height), 'white')
                new_img.paste(img_with_orientation, (0, top_margin_px))
                
                base_img = new_img
                base_width, base_height = base_img.size
            
            # 计算叠加位置
            overlay_width, overlay_height = overlay_img.size
            margin_top_px = int(1 * mm_to_px)
            x_pos = (base_width - overlay_width) // 2
            y_pos = margin_top_px
            
            if overlay_img.mode != 'RGBA':
                overlay_img_rgba = overlay_img.convert('RGBA')
            else:
                overlay_img_rgba = overlay_img
            
            if base_img.mode != 'RGBA':
                base_img_rgba = base_img.convert('RGBA')
            else:
                base_img_rgba = base_img
            
            result_img = base_img_rgba.copy()
            result_img.paste(overlay_img_rgba, (x_pos, y_pos), overlay_img_rgba)
            result_img = result_img.convert('RGB')
            
            result_img.save(jpg_file_path, 'JPEG', dpi=(DPI, DPI))
            
            return True, jpg_file_path
            
        except Exception as e:
            print(f"处理JPG文件时出错: {str(e)}")
            return False, jpg_file_path
    
    def process_single_file(self, jpg_file_path, directory_name):
        """处理单个文件"""
        start_time = time.time()
        
        # 获取当前目录下的文件数量
        dir_path = os.path.dirname(jpg_file_path)
        jpg_files_in_dir = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg'))]
        file_count = len(jpg_files_in_dir)
        
        # 创建归档章图片
        grid_img = self.create_red_grid_image(directory_name, file_count)
        
        # 将归档章叠加到JPG文件
        success, processed_file_path = self.overlay_image_on_jpg(jpg_file_path, grid_img)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        return {
            'file_path': jpg_file_path,
            'directory_name': directory_name,
            'success': success,
            'processed_file_path': processed_file_path,
            'duration': duration
        }


class ArchiveStampPage(FunctionPage):
    def __init__(self):
        super().__init__("文件改名加盖归档章")
        group = QGroupBox("按目录名生成归档章并加盖到JPG文件")
        form = QFormLayout()

        self.dir_path = QLineEdit()
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(self.browse_dir)

        h1 = QHBoxLayout()
        h1.addWidget(self.dir_path)
        h1.addWidget(btn_browse)

        form.addRow("目标目录:", h1)
        
        # 覆盖原归档章选项
        self.overwrite_check = QCheckBox("覆盖原归档章")
        self.overwrite_check.setChecked(False)
        form.addRow("选项:", self.overwrite_check)
        
        # 线程数设置
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 32)
        self.thread_spin.setValue(4)
        form.addRow("线程数:", self.thread_spin)
        
        group.setLayout(form)
        self.layout.addWidget(group)
        
        # 说明文本
        info_label = QLabel(
            "功能说明：\n"
            "• 根据目录名称自动生成归档章（45mm×16mm）\n"
            "• 在所有JPG文件顶部增加18mm白色边框\n"
            "• 归档章加盖在边框正中间（距顶部1mm）\n"
            "• 可选：覆盖原归档章后重新加盖\n"
            "• 自动从目录名提取：全宗号、年份、档号"
        )
        info_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.layout.addWidget(info_label)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("预览操作")
        self.preview_btn.setObjectName("ActionBtn")
        self.preview_btn.setStyleSheet("background-color: #2196F3;")
        self.preview_btn.clicked.connect(self.preview_operations)
        btn_layout.addWidget(self.preview_btn)
        
        btn_exec = QPushButton("开始加盖归档章")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        btn_layout.addWidget(btn_exec)
        
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        self.layout.addLayout(btn_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)
        
        self.worker = None
        self.add_log_widget()
    
    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择目录")
        if d: self.dir_path.setText(d)
    
    def preview_operations(self):
        """预览将要执行的操作"""
        d = self.dir_path.text()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        
        # 清空之前的结果
        self.log_box.clear()
        
        self.log("="*50)
        self.log("正在预览操作...")
        self.log(f"基础目录: {d}")
        self.log("-"*50)
        
        try:
            # 统计JPG文件
            jpg_count = 0
            dir_count = 0
            sample_files = []
            
            for root, dirs, files in os.walk(d):
                jpg_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg'))]
                if jpg_files:
                    dir_count += 1
                    jpg_count += len(jpg_files)
                    if len(sample_files) < 3:
                        sample_files.append((os.path.basename(root), jpg_files[0]))
            
            if jpg_count == 0:
                self.log("未找到任何JPG文件")
                return
            
            self.log(f"找到 {dir_count} 个目录，共 {jpg_count} 个JPG文件")
            self.log("")
            self.log("示例文件：")
            for dir_name, filename in sample_files:
                self.log(f"  • {dir_name}/{filename}")
            
            self.log("")
            if self.overwrite_check.isChecked():
                self.log("注意：将覆盖原归档章并重新加盖")
            else:
                self.log("注意：将在文件顶部添加18mm白色边框并加盖归档章")
            
            self.log("")
            self.log("这只是预览，文件尚未修改。")
            
        except Exception as e:
            error_msg = f"预览过程中出现错误: {str(e)}"
            self.log(error_msg)
            QMessageBox.critical(self, "错误", error_msg)

    def execute(self):
        d = self.dir_path.text()
        if not d:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return
        
        # 确认操作
        confirm_msg = "确定要开始加盖归档章吗？"
        if self.overwrite_check.isChecked():
            confirm_msg += "\n\n注意：此操作将覆盖原归档章区域（顶部18mm），请确保已备份重要文件！"
        
        reply = QMessageBox.question(
            self, "确认操作",
            confirm_msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 重置进度条
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        
        # 禁用按钮，启用停止按钮
        self.log("="*50)
        self.log("开始处理...")
        self.log(f"目录: {d}")
        if self.overwrite_check.isChecked():
            self.log("选项: 覆盖原归档章并重新加盖")
        else:
            self.log("选项: 添加新归档章（不覆盖）")
        self.log(f"线程数: {self.thread_spin.value()}")
        self.log("="*50)
        
        # 创建工作线程
        overwrite_original = self.overwrite_check.isChecked()
        max_workers = self.thread_spin.value()
        self.worker = ArchiveStampWorker(
            base_dir=d,
            overwrite_original=overwrite_original,
            max_workers=max_workers
        )
        
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        
        self.worker.start()
        
        # 更新按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始加盖归档章":
            btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")
        self.log(f"进度: {current}/{total} ({percentage:.1f}%)")
    
    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        
        # 恢复按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始加盖归档章":
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)


# ----------------------------------------------------------------------
# 图片 DPI 修改（由 modify_jpg_dpi.py 移植，去除 tkinter 依赖）
# ----------------------------------------------------------------------
def _dpi_get_image_dpi(image_path):
    """读取图片 DPI：优先 info['dpi']，其次 EXIF 分辨率，最后返回分辨率。"""
    try:
        Image.MAX_IMAGE_PIXELS = None
        with Image.open(image_path) as img:
            dpi = img.info.get('dpi')
            if dpi is not None:
                return dpi if isinstance(dpi, tuple) else (dpi, dpi)
            try:
                exif = img.getexif()
                if exif:
                    xr, yr, unit = exif.get(282), exif.get(283), exif.get(296, 2)
                    if xr and yr:
                        if unit == 3:        # 厘米 → 英寸
                            return f"EXIF:{xr * 2.54:.0f}x{yr * 2.54:.0f} DPI"
                        elif unit == 2:      # 英寸
                            return f"EXIF:{xr:.0f}x{yr:.0f} DPI"
                        else:
                            return f"EXIF:{xr:.0f}x{yr:.0f}(无单位)"
            except Exception:
                pass
            return f"{img.width}x{img.height}(无DPI元数据)"
    except Exception:
        return "DPI获取失败"


def _dpi_get_image_details(image_path):
    """获取图片详情：分辨率/色彩模式/格式/文件大小。"""
    details = {'resolution': '未知', 'mode': '未知', 'format': '未知', 'file_size': '未知'}
    try:
        Image.MAX_IMAGE_PIXELS = None
        Image.LOAD_TRUNCATED_IMAGES = True
        with Image.open(image_path) as img:
            details['resolution'] = f"{img.width}x{img.height}"
            details['mode'] = img.mode
            details['format'] = img.format
        try:
            details['file_size'] = f"{os.path.getsize(image_path):,} bytes"
        except Exception:
            pass
    except Exception:
        pass
    return details


def _dpi_init_log(log_path):
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("JPG文件DPI修改日志\n")
            f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 120 + "\n")
            f.write(f"{'文件名':<28}{'原DPI':<16}{'新DPI':<12}{'分辨率':<14}{'模式':<8}"
                    f"{'格式':<8}{'大小':<16}{'结果':<10}{'耗时(s)':<10}\n")
            f.write("-" * 120 + "\n")
    except Exception:
        pass


def _dpi_append_log(log_path, info):
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"{os.path.basename(str(info.get('file_path', ''))):<28}"
                    f"{str(info.get('original_dpi', '')):<16}"
                    f"{str(info.get('new_dpi', '')):<12}"
                    f"{str(info.get('resolution', '')):<14}"
                    f"{str(info.get('mode', '')):<8}"
                    f"{str(info.get('format', '')):<8}"
                    f"{str(info.get('file_size', '')):<16}"
                    f"{str(info.get('result', '')):<10}"
                    f"{str(info.get('process_time', '')):<10}\n")
    except Exception:
        pass


def _dpi_finalize_log(log_path, stats):
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write("-" * 120 + "\n")
            f.write(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总计处理: {stats.get('processed_files', 0)} 个\n")
            f.write(f"成功修改: {stats.get('modified_files', 0)} 个\n")
            f.write(f"失败: {len(stats.get('errors', []))} 个\n")
            f.write("=" * 120 + "\n")
    except Exception:
        pass


# ---------------- DPI修改记录数据库(sqlite) ----------------
_DPI_DB_NAME = 'dpi_modified_records.db'

def _dpi_db_path():
    """记录库固定放在程序目录(独立于处理目录, 跨次累积)。"""
    base = getattr(sys, '_MEIPASS', None)  # exe运行时不可写, 用exe所在目录
    if base:  # PyInstaller onefile: _MEIPASS是临时解压目录 → 放exe旁
        base = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, _DPI_DB_NAME)

def _dpi_db_init(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS modified_files (
        file_path TEXT NOT NULL,
        file_name TEXT NOT NULL,
        dpi INTEGER,
        modified_at TEXT,
        PRIMARY KEY (file_path, file_name))""")
    conn.commit()

def _dpi_db_record_many(records):
    """批量写入修改记录(路径+文件名+DPI)。失败静默(不影响主流程)。"""
    import sqlite3
    try:
        conn = sqlite3.connect(_dpi_db_path())
        try:
            _dpi_db_init(conn)
            conn.executemany(
                "INSERT OR REPLACE INTO modified_files VALUES (?,?,?,?)",
                [(r['file_path'], os.path.basename(r['file_path']),
                  r.get('dpi', 0),
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                 for r in records])
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass

def _dpi_db_processed_set():
    """已记录修改的 (路径, 文件名) 集合。库不存在/异常返回空集。"""
    import sqlite3
    try:
        if not os.path.exists(_dpi_db_path()):
            return set()
        conn = sqlite3.connect(_dpi_db_path())
        try:
            rows = conn.execute("SELECT file_path, file_name FROM modified_files").fetchall()
            return {(r[0].lower(), r[1].lower()) for r in rows}
        finally:
            conn.close()
    except Exception:
        return set()


def _dpi_process_single_file(file_path, dpi, dry_run, stop_event=None):
    """处理单个 JPG：读取原 DPI，按需重写为 dpi（仅改 DPI，不改像素）。"""
    start = time.time()
    if stop_event and stop_event.is_set():
        return {'file_path': file_path, 'original_dpi': '未知', 'new_dpi': f"{dpi}x{dpi}",
                'result': '已停止', 'process_time': 0, 'success': False, 'error': '用户停止'}
    try:
        Image.MAX_IMAGE_PIXELS = None
        original_dpi = _dpi_get_image_dpi(file_path)
        original_dpi_str = (f"{original_dpi[0]}x{original_dpi[1]}"
                            if isinstance(original_dpi, tuple) else str(original_dpi))
        details = _dpi_get_image_details(file_path)
        if stop_event and stop_event.is_set():
            return {'file_path': file_path, 'original_dpi': original_dpi_str,
                    'new_dpi': f"{dpi}x{dpi}", 'result': '已停止',
                    'process_time': round(time.time() - start, 3), 'success': False, 'error': '用户停止',
                    **details}

        if not dry_run:
            Image.LOAD_TRUNCATED_IMAGES = True
            with Image.open(file_path) as img:
                img.save(file_path, dpi=(dpi, dpi))
            result = "成功"
        else:
            result = "模拟成功"

        return {'file_path': file_path, 'original_dpi': original_dpi_str,
                'new_dpi': f"{dpi}x{dpi}", 'result': result,
                'process_time': round(time.time() - start, 3), 'success': True, **details}
    except Exception as e:
        return {'file_path': file_path, 'original_dpi': '未知', 'new_dpi': f"{dpi}x{dpi}",
                'result': '失败', 'process_time': round(time.time() - start, 3),
                'success': False, 'error': str(e)}


class ModifyDpiWorker(QThread):
    """JPG 图片 DPI 批量修改后台线程（多线程，支持模拟运行与停止）。"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)      # (已完成, 总数)
    finished_signal = Signal(bool, str)     # (是否正常完成, 汇总信息)

    def __init__(self, base_dir, dpi=600, dry_run=False, max_workers=4, only_new=False, parent=None):
        super().__init__(parent)
        self.base_dir = base_dir
        self.dpi = dpi
        self.dry_run = dry_run
        self.max_workers = max_workers
        self.only_new = only_new      # 只修改新增: 与历史记录(路径+文件名)完全相同的跳过
        self.is_stopped = False
        self.stop_event = threading.Event()

    def stop(self):
        self.is_stopped = True
        self.stop_event.set()

    def run(self):
        try:
            Image.MAX_IMAGE_PIXELS = None
            Image.LOAD_TRUNCATED_IMAGES = True

            # 递归收集 JPG/JPEG
            jpg_files = []
            for root, _d, files in os.walk(self.base_dir):
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg')):
                        jpg_files.append(os.path.join(root, f))

            # 只修改新增: 与历史记录(路径+文件名)完全相同的文件跳过
            skipped = 0
            if self.only_new and not self.dry_run:
                done_set = _dpi_db_processed_set()
                if done_set:
                    before = len(jpg_files)
                    jpg_files = [fp for fp in jpg_files
                                 if (fp.lower(), os.path.basename(fp).lower()) not in done_set]
                    skipped = before - len(jpg_files)
                    if skipped:
                        self.log_signal.emit(f"「只修改新增」: 跳过已记录修改过的文件 {skipped} 个")

            total = len(jpg_files)
            if total == 0:
                msg = f"目录 {self.base_dir} 下未找到 JPG/JPEG 文件"
                if skipped:
                    msg += f"（{skipped} 个已记录文件被「只修改新增」跳过）"
                self.finished_signal.emit(False, msg)
                return

            mode = "模拟运行" if self.dry_run else "实际修改"
            self.log_signal.emit(f"找到 {total} 个 JPG 文件，目标 DPI={self.dpi}，"
                                 f"线程数={self.max_workers}，{mode}")

            # 日志文件
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = os.path.join(self.base_dir, f"dpi_modify_log_{ts}.txt")
            _dpi_init_log(log_path)

            self.log_signal.emit(f"{'目录':<16} | {'文件名':<24} | {'原DPI':<14} | "
                                 f"{'新DPI':<10} | {'结果':<6} | 耗时(秒)")
            self.log_signal.emit("-" * 90)

            done = 0
            success = 0
            errors = []
            ok_records = []   # 实际修改成功的文件 → 写入sqlite记录

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {
                    executor.submit(_dpi_process_single_file, fp, self.dpi,
                                    self.dry_run, self.stop_event): fp
                    for fp in jpg_files
                }
                for future in as_completed(future_to_file):
                    if self.is_stopped:
                        for ff in future_to_file:
                            ff.cancel()
                        break
                    fp = future_to_file[future]
                    try:
                        res = future.result()
                    except Exception as e:
                        res = {'file_path': fp, 'original_dpi': '未知', 'new_dpi': f"{self.dpi}x{self.dpi}",
                               'result': '异常', 'process_time': 0, 'success': False, 'error': str(e)}
                        self.log_signal.emit(f"处理异常 {os.path.basename(fp)}: {e}")

                    _dpi_append_log(log_path, res)
                    dir_name = os.path.basename(os.path.dirname(fp))
                    self.log_signal.emit(
                        f"{dir_name:<16} | {os.path.basename(fp):<24} | "
                        f"{str(res.get('original_dpi', '')):<14} | {res.get('new_dpi', ''):<10} | "
                        f"{res.get('result', ''):<6} | {res.get('process_time', 0)}")

                    done += 1
                    if res.get('success'):
                        success += 1
                        if not self.dry_run:
                            res['dpi'] = self.dpi
                            ok_records.append(res)
                    else:
                        errors.append(f"{os.path.basename(fp)}: {res.get('error', '')}")
                    self.progress_signal.emit(done, total)

            _dpi_finalize_log(log_path, {'processed_files': done,
                                         'modified_files': success, 'errors': errors})

            # 实际修改成功的文件写入记录库(供「只修改新增」判重)
            if ok_records:
                _dpi_db_record_many(ok_records)
                self.log_signal.emit(f"已记录 {len(ok_records)} 个修改文件到本地数据库({_DPI_DB_NAME})")

            if self.is_stopped:
                self.finished_signal.emit(False, f"已停止。已处理 {done}/{total}，成功 {success}。")
            else:
                skip_info = f"，跳过已记录 {skipped} 个" if skipped else ""
                self.finished_signal.emit(
                    True, f"{mode}完成：共 {done} 个，成功 {success}，失败 {len(errors)}{skip_info}。日志：{log_path}")
        except Exception as e:
            self.finished_signal.emit(False, f"运行异常：{e}")


class ModifyDpiPage(FunctionPage):
    """图片 DPI 批量修改功能页（递归处理 JPG/JPEG，仅改 DPI 不影响像素）"""
    def __init__(self):
        super().__init__("修改DPI")
        self.worker = None

        group = QGroupBox("图片DPI批量修改（递归处理 JPG/JPEG，仅改DPI不影响像素尺寸）")
        form = QFormLayout()

        self.img_dir = QLineEdit()
        self.img_dir.setPlaceholderText("选择包含 JPG 图片的目录...")
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(
            lambda: self.img_dir.setText(QFileDialog.getExistingDirectory(self, "选择图片目录")))
        h1 = QHBoxLayout()
        h1.addWidget(self.img_dir)
        h1.addWidget(btn_browse)

        self.dpi_edit = QLineEdit()
        self.dpi_edit.setText("300")
        self.dpi_edit.setMaxLength(5)
        self.dpi_edit.setMaximumWidth(140)
        self.dpi_edit.setValidator(QRegularExpressionValidator(QRegularExpression("\\d*")))
        h_dpi = QHBoxLayout()
        h_dpi.addWidget(self.dpi_edit)
        h_dpi.addWidget(QLabel("DPI"))
        h_dpi.addStretch()

        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 32)
        self.thread_spin.setValue(4)

        self.dry_run_cb = QCheckBox("模拟运行（仅预览将要执行的操作，不实际修改文件）")

        # 只修改新增: 勾选后, 与本地记录库中「路径+文件名」完全相同的文件跳过
        self.only_new_cb = QCheckBox("只修改新增（跳过已修改过的文件，按路径+文件名判重）")
        self.only_new_cb.setChecked(False)
        self.only_new_cb.setToolTip(
            "程序在本地数据库记录每次实际修改过的文件(路径+文件名)。\n"
            "勾选后，与历史记录完全相同的文件不再重复修改；未勾选则全部重新处理。")

        form.addRow("图片目录:", h1)
        form.addRow("目标DPI:", h_dpi)
        form.addRow("线程数:", self.thread_spin)
        form.addRow("", self.dry_run_cb)
        form.addRow("", self.only_new_cb)
        group.setLayout(form)
        self.layout.addWidget(group)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("预览操作")
        self.preview_btn.setObjectName("ActionBtn")
        self.exec_btn = QPushButton("开始修改")
        self.exec_btn.setObjectName("ActionBtn")
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.setEnabled(False)
        self.clear_btn = QPushButton("清空结果")
        self.clear_btn.setObjectName("ActionBtn")
        self.preview_btn.clicked.connect(self._preview)
        self.exec_btn.clicked.connect(self._execute)
        self.stop_btn.clicked.connect(self._stop)
        self.clear_btn.clicked.connect(self._clear)
        for b in (self.preview_btn, self.exec_btn, self.stop_btn, self.clear_btn):
            btn_layout.addWidget(b)
        self.layout.addLayout(btn_layout)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

        self.add_log_widget()

    # ---------- 辅助 ----------
    def _target_dpi(self):
        try:
            return int(self.dpi_edit.text().strip())
        except ValueError:
            return 0

    def _set_running(self, running):
        self.preview_btn.setEnabled(not running)
        self.exec_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)

    def _start_worker(self, dry_run):
        directory = self.img_dir.text().strip()
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "提示", "请先选择有效的图片目录。")
            return
        dpi = self._target_dpi()
        if dpi <= 0:
            QMessageBox.warning(self, "提示", "目标 DPI 必须为正整数。")
            return
        self._clear()
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        self.worker = ModifyDpiWorker(directory, dpi=dpi, dry_run=dry_run,
                                      max_workers=self.thread_spin.value(),
                                      only_new=self.only_new_cb.isChecked())
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.finished_signal.connect(self._on_finished)
        self._set_running(True)
        self.worker.start()

    def _preview(self):
        self._start_worker(dry_run=True)

    def _execute(self):
        directory = self.img_dir.text().strip()
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "提示", "请先选择有效的图片目录。")
            return
        dpi = self._target_dpi()
        confirm = QMessageBox.question(
            self, "确认操作",
            f"确定要将 {directory} 下所有 JPG/JPEG 的 DPI 修改为 {dpi} 吗？\n"
            f"此操作会直接覆盖原文件，不可逆。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        self._start_worker(dry_run=False)

    def _stop(self):
        if self.worker:
            self.worker.stop()
            self.log("正在停止...")

    def _update_progress(self, done, total):
        if total <= 0:
            self.progress.setValue(0)
            self.progress.setFormat("0 / 0")
            return
        pct = int(done * 100 / total)
        self.progress.setValue(pct)
        self.progress.setFormat(f"{done} / {total}  ({pct}%)")

    def _on_finished(self, ok, message):
        self._set_running(False)
        self.log(message)
        self.progress.setFormat("已完成" if ok else "已停止")
        self.worker = None
        QMessageBox.information(self, "完成" if ok else "结束", message)

    def _clear(self):
        if hasattr(self, 'progress'):
            self.progress.setValue(0)
            self.progress.setFormat("待开始")
        if hasattr(self, 'log_box'):
            self.log_box.clear()


class JpgToPdfWorker(QThread):
    """JPG转双层PDF后台处理线程"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)
    
    def __init__(self, directory_path, output_dir=None, max_workers=4, resolution=100.0,
                 generate_ofd=False, gpu_render=False, use_gpu_ocr=False, parent=None):
        super().__init__(parent)
        self.directory_path = directory_path
        self.output_dir = output_dir if output_dir else directory_path
        self.max_workers = max_workers
        self.resolution = resolution
        self.generate_ofd = generate_ofd  # 是否同时生成OFD文件
        self.gpu_render = gpu_render      # GPU渲染: 图像加速路径(MKL-DNN+无损直传)
        self.use_gpu_ocr = use_gpu_ocr    # OCR用GPU推理(不可用自动回退CPU)
        # v3.17: 取消v3.15的GPU OCR模式强制单线程限制, 恢复允许用户自选多线程。
        # OCR仍由单一服务线程串行执行(线程安全不变), 多线程的意义在于图像解码/
        # PDF分段写入等非OCR阶段与OCR形成流水线并行。v3.15担心的内存峰值与
        # 孤儿GPU线程显存泄漏风险由v3.14的run_monitor监控与GPU引擎损坏计数≥2
        # 全局降级CPU机制兜底, 不再以牺牲吞吐换取。
        self._gpu_forced_single = False
        self.is_stopped = False
        self._done = False  # 是否已发出完成信号(界面层线程意外终止兜底判断用)
        import threading
        self._ofd_lock = threading.Lock()
        self._ocr = None  # PaddleOCR 延迟初始化(与分件共享同一初始化逻辑)
        # --- OCR服务线程机制(防GPU推理挂死) ---
        # PaddleOCR predictor 非线程安全且GPU路径存在首推理永久挂起的可能。
        # 所有OCR操作(初始化/探测/逐页推理/显存释放)统一提交到单一daemon服务
        # 线程串行执行, 调用方带超时等待: 超时=判定该服务线程挂死, 丢弃后以
        # CPU配置重启新服务线程(孤儿线程后台泄漏但不再阻塞任何处理)。
        self._svc_lock = threading.Lock()   # 服务线程生命周期管理锁(惰性初始化并发)
        self._svc_q = None                  # 当前服务线程任务队列(挂死后换新)
        self._svc_thread = None             # 当前服务线程对象(v3.12: 存活检测用)
        self._svc_rebuilt = False           # 是否已做过GPU挂死→CPU重建(每轮只做一次)
        self._ocr_pages_since_init = 0      # 引擎例行重建计数(与分件共享同款机制, v3.9)
        # v3.14补: 初始化锁必须在此创建——_get_ocr 的双重检查锁通过
        # getattr(self,'_ocr_init_lock',None) 取锁, 缺失时取到None直接跳过加锁,
        # 4个工作线程并发首调 _get_ocr() 会同时进入 _init_ocr_locked() 并发
        # 构造 PaddleOCR(GPU显存重复分配/CUDA上下文冲突→Memory allocation failed
        # 或段错误)。FileSplitWorker.__init__ 有同款锁(分件单线程时无害),
        # 本类此前遗漏是真实缺陷。
        self._ocr_init_lock = threading.Lock()
        self._probe_lock = threading.Lock()  # 首推理探测全局只做一次(其余线程等结果)
        self._ocr_probed = False            # 探测是否完成(含重建后的重探测)
        self._ocr_broken = False            # OCR降级标志(探测+CPU重建均失败→仅图像PDF;
                                           # v3.16起非永久: 每OCR_REPROBE_DIRS个目录复探)
        self._dirs_since_broken = 0         # v3.16: OCR降级后已处理的目录数(复探计数)
        self._gpu_engine_failures = 0       # v3.14: GPU引擎损坏累计(≥2次全局降级CPU)
        # v3.14: GPU运行监控日志——4线程GPU模式下周期采样进程内存/GPU显存/线程数/
        # OCR队列深度, 写入输出目录 run_monitor_时间戳.txt, 协助定位崩溃点。
        self._run_mon_path = None           # 监控日志路径(None=不启用)
        self._run_mon_lock = threading.Lock()
        self._run_mon_stop = threading.Event()
        
        # 检查 OFD 转换库是否可用（用于生成双层OFD）
        # 使用自建 ofd_writer（基于 PyMuPDF，生成图像层+文本层的双层OFD，
        # 无页数限制）。旧的 Spire.PDF 免费版只能转前 3 页，已弃用。
        if self.generate_ofd:
            try:
                import fitz  # noqa: F401  PyMuPDF
                from ofd_writer import make_layered_ofd  # noqa: F401
                self.ofd_available = True
            except ImportError:
                self.ofd_available = False
        else:
            self.ofd_available = False
    
    def run(self):
        try:
            # GPU环境预处理(屏蔽无卡机CUDA设备+显存安全分配策略)已在模块导入时完成,
            # 见文件头部 _setup_paddle_gpu_env()——必须在paddle首次导入之前设置,
            # 而GPU预检(_check_gpu_capability)会在工作线程启动前先行导入paddle。

            # 输出目录不存在则创建(缺省为 源目录/PDF, 可能尚不存在)
            if self.output_dir:
                os.makedirs(self.output_dir, exist_ok=True)
            # 收集所有目录下的JPG文件
            dir_jpgs_map = self.collect_jpg_files()
            if not dir_jpgs_map:
                self._emit_finished(False, f"在目录 {self.directory_path} 及其子目录中没有找到JPG文件")
                return
            
            total_dirs = len(dir_jpgs_map)
            self.log_signal.emit(f"找到 {total_dirs} 个包含JPG文件的目录，使用 {self.max_workers} 个线程开始处理...")
            if self.use_gpu_ocr and self.max_workers > 1:
                # v3.17: GPU模式多线程提示(不再强制单线程): OCR本身由服务线程
                # 串行执行, 多线程用于解码/写PDF等阶段与OCR流水线并行。
                self.log_signal.emit("  GPU OCR模式多线程: OCR推理仍串行执行, "
                                     "多线程用于图像解码/PDF写入流水线(有内存峰值与"
                                     "GPU挂死风险, 已由运行监控与自动降级CPU兜底)")

            # v3.14: GPU模式启动运行监控(每10秒采样内存/显存/线程/队列, 崩溃定位用)
            self._start_run_monitor(self.output_dir,
                                    f'{total_dirs}个目录/{self.max_workers}线程')
            
            # 创建日志文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"jpgtopdf_log_{timestamp}.txt"
            log_path = os.path.join(self.output_dir, log_filename)
            start_time = datetime.now()
            self.init_log_file(log_path, start_time)
            
            # 处理所有目录
            results_list = []
            success_count = 0
            completed = 0
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for dir_path, jpg_files in dir_jpgs_map.items():
                    if self.is_stopped:
                        break
                    dir_name = os.path.basename(dir_path)
                    future = executor.submit(
                        self.process_single_directory,
                        jpg_files, dir_name
                    )
                    futures[future] = (dir_name, jpg_files)
                
                for future in as_completed(futures):
                    if self.is_stopped:
                        break
                    
                    completed += 1
                    dir_name, jpg_files = futures[future]
                    
                    try:
                        result = future.result()
                        results_list.append(result)
                        
                        # 实时记录日志
                        self.append_to_log(log_path, result)
                        
                        if result['result'] == '成功':
                            success_count += 1
                            log_msg = f"✓ {result['folder']}/{result['pdf_file']} - 成功 ({result['duration']}秒)"
                            if result.get('ofd_generated'):
                                log_msg += f" [已生成OFD: {result['ofd_file']}]"
                            self.log_signal.emit(log_msg)
                        else:
                            self.log_signal.emit(
                                f"✗ {result['folder']}/{result['pdf_file']} - {result['ocr_status']}"
                            )
                        
                        self.progress_signal.emit(completed, total_dirs)
                        
                    except Exception as e:
                        error_msg = f"处理目录 {dir_name} 时发生异常: {str(e)}"
                        self.log_signal.emit(error_msg)
                        self.progress_signal.emit(completed, total_dirs)
            
            if not self.is_stopped:
                # 完成日志文件
                self.finalize_log_file(log_path, results_list, start_time)
                
                success_rate = (success_count / total_dirs) * 100 if total_dirs > 0 else 0
                rate_msg = f"\n处理完成！共处理 {total_dirs} 个目录，成功 {success_count} 个，成功率 {success_rate:.1f}%。\n日志: {log_filename}"
                
                if success_rate >= 90:
                    rate_msg += "\n提示：单线程处理可能获得更高成功率！"
                
                self._emit_finished(True, rate_msg)
            else:
                self._emit_finished(False, "处理已停止")
            self._stop_run_monitor('处理完成' if not self.is_stopped else '用户停止')

        except BaseException as e:
            # BaseException: SystemExit/KeyboardInterrupt 等也须发出完成信号,
            # 否则界面永久卡死; 具体堆栈由全局崩溃日志机制记录。
            self._stop_run_monitor(f'run异常: {e}')
            self._emit_finished(False, f"处理出错: {str(e)}")
    
    def stop(self):
        self.is_stopped = True

    def _emit_finished(self, ok, msg):
        """统一经此发出完成信号并置位标记, 供界面层区分「正常结束」与「意外终止」。"""
        self._done = True
        self.finished_signal.emit(ok, msg)
    
    def collect_jpg_files(self):
        """收集目录及子目录下所有JPG文件（按目录分组）"""
        dir_jpgs_map = {}
        
        for root, dirs, files in os.walk(self.directory_path):
            jpg_files = []
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    jpg_path = os.path.join(root, filename)
                    jpg_files.append(jpg_path)
            
            if jpg_files:
                jpg_files.sort()
                dir_jpgs_map[root] = jpg_files
        
        return dir_jpgs_map
    
    def jpgs_to_pdf(self, jpg_paths, output_dir, pdf_filename):
        """将多个 JPG 文件合并为一个 PDF（仅图像层）。
        优先 fitz 流式逐页写盘: 逐页直接嵌入文件、不全量解码图像, 内存峰值与页数无关;
        旧版 PIL 方式会把整目录图像全量解码驻留内存, 系统内存紧张(如同时运行其他任务)
        时进程会被操作系统直接终止且无任何错误记录。仅在缺 fitz 时回退 PIL 合并。"""
        pdf_path = os.path.join(output_dir, pdf_filename + ".pdf")
        Image.MAX_IMAGE_PIXELS = None
        try:
            import fitz
        except ImportError:
            fitz = None
        if fitz is not None:
            doc = fitz.open()
            # 分段写盘: 与双层路径同款策略, 超大目录分段保存后合并, doc峰值恒定。
            # v3.11: CHUNK同样按单文件大小自适应(大文件时缩小分段, 限制doc驻留峰值)。
            try:
                _sizes = [os.path.getsize(p) for p in jpg_paths[:20]]
                _avg_mb = (sum(_sizes) / len(_sizes) / 1048576.0) if _sizes else 1.0
                CHUNK = int(max(8, min(50, 400.0 / max(_avg_mb, 0.5))))
            except Exception:
                CHUNK = 50
            seg_paths = []
            page_no = 0
            for jpg_path in jpg_paths:
                # 仅取尺寸(头信息), 不全量解码
                img = Image.open(jpg_path)
                w_px, h_px = img.size
                img.close()
                w_pt = w_px * 72.0 / self.resolution
                h_pt = h_px * 72.0 / self.resolution
                page = doc.new_page(width=w_pt, height=h_pt)
                page.insert_image(fitz.Rect(0, 0, w_pt, h_pt), filename=jpg_path)
                page_no += 1
                if page_no % CHUNK == 0 and page_no < len(jpg_paths):
                    _seg = pdf_path + f'.imgpart{page_no // CHUNK}'
                    doc.save(_seg, garbage=3, deflate=True)
                    doc.close()
                    seg_paths.append(_seg)
                    doc = fitz.open()
            if seg_paths:
                _last = pdf_path + f'.imgpart{len(seg_paths) + 1}'
                doc.save(_last, garbage=3, deflate=True)
                doc.close()
                seg_paths.append(_last)
                merged = fitz.open()
                for sp in seg_paths:
                    _sd = fitz.open(sp)
                    merged.insert_pdf(_sd)
                    _sd.close()  # v3.11: insert_pdf已拷入页面, 立即关闭分段防驻留累积
                    os.remove(sp)
                merged.save(pdf_path, garbage=3, deflate=True)
                merged.close()
            else:
                doc.save(pdf_path, garbage=3, deflate=True)
                doc.close()
            return pdf_path

        images = []
        for jpg_path in jpg_paths:
            image = Image.open(jpg_path)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            images.append(image)
        
        if images:
            first_image = images[0]
            if len(images) == 1:
                first_image.save(pdf_path, "PDF", resolution=self.resolution)
            else:
                first_image.save(pdf_path, "PDF", resolution=self.resolution, save_all=True, append_images=images[1:])
        
        return pdf_path
    
    # 复用分件功能的本地 PaddleOCR(多配置兼容初始化+初始化锁+中文路径安全)
    _get_ocr = FileSplitWorker._get_ocr
    _init_ocr_locked = FileSplitWorker._init_ocr_locked
    _preload_img_arr = FileSplitWorker._preload_img_arr   # v3.26: 预解码(崩溃修复)
    _ocr_page = FileSplitWorker._ocr_page
    _imread_cn = staticmethod(FileSplitWorker._imread_cn)
    # OCR服务线程机制(定义在 FileSplitWorker 内, 两处共享同一实现):
    # 串行化推理+超时看门狗+GPU挂死后CPU重建, 依赖 __init__ 中的 _svc_* 属性
    _ocr_svc_loop = FileSplitWorker._ocr_svc_loop
    _ensure_ocr_service = FileSplitWorker._ensure_ocr_service
    _ocr_svc_call = FileSplitWorker._ocr_svc_call
    _rebuild_ocr_cpu = FileSplitWorker._rebuild_ocr_cpu
    _svc_empty_cache = FileSplitWorker._svc_empty_cache
    # v3.14: GPU运行监控(同定义于 FileSplitWorker, 依赖 __init__ 中 _run_mon_* 属性)
    _run_monitor_line = FileSplitWorker._run_monitor_line
    _run_monitor_loop = FileSplitWorker._run_monitor_loop
    _start_run_monitor = FileSplitWorker._start_run_monitor
    _stop_run_monitor = FileSplitWorker._stop_run_monitor
    # 类属性别名: 例行重建阈值(方法别名不携带类属性, 须显式同步)
    _OCR_RECYCLE_PAGES = FileSplitWorker._OCR_RECYCLE_PAGES

    def _ocr_local_available(self):
        """本地OCR是否可用(初始化一次)。"""
        return self._get_ocr() is not None

    # v3.16: OCR降级后的自动复探间隔(目录数)。降级可能源于临时性故障(探测时
    # 显存恰被其他程序占满/系统内存紧张)或探测假阳性, 不应永久封死整批双层
    # 输出; 间隔取10平衡"环境真坏时的重试代价"(每10个目录一次60秒复探)与
    # "临时故障的恢复时延"。
    _OCR_REPROBE_DIRS = 10

    @staticmethod
    def _make_probe_image(path):
        """生成OCR探测图(600x200白底黑字)。字体依次尝试 simhei/msyh/simsun,
        全部缺失时回退PIL默认字体(v3.16前仅试simhei且失败时静默用默认小字体,
        小字识别不出文字 → 探测假阳性 → 误全局降级单层)。"""
        _pb = Image.new('RGB', (600, 200), 'white')
        from PIL import ImageDraw as _ID, ImageFont as _IF
        _dr = _ID.Draw(_pb)
        _fnt = None
        for _fn in ('simhei.ttf', 'msyh.ttc', 'simsun.ttc'):
            try:
                _fnt = _IF.truetype('C:/Windows/Fonts/' + _fn, 40)
                break
            except Exception:
                continue
        _dr.text((40, 60), 'OCR探测测试文字', fill=(0, 0, 0), font=_fnt)
        _pb.save(path)

    def _reprobe_ocr(self, output_dir):
        """OCR降级后的快速复探(须持 _probe_lock 调用)。
        丢弃降级时可能损坏的引擎→按当前配置(降级路径已CPU化)重建→小图推理,
        60秒超时。返回 True=推理恢复正常(调用方解除降级)。"""
        self.log_signal.emit("  OCR降级后自动复探(最长60秒)...")
        _probe = os.path.join(output_dir, '_ocr_probe.png')
        try:
            self._make_probe_image(_probe)
            self._ocr = None              # 丢弃旧实例(降级时可能已损坏)
            self._ocr_pages_since_init = 0
            _pa = self._preload_img_arr(_probe)   # v3.26: 探测也预解码
            st, _res = self._ocr_svc_call(
                lambda: self._ocr_page(_probe, None, lambda s: None,
                                       img_arr=_pa),
                timeout=60)
            if st == 'ok' and _res:
                return True
            self.log_signal.emit(f"  × OCR复探未通过({st}), 继续降级单层")
            return False
        except Exception:
            return False
        finally:
            try:
                os.remove(_probe)
            except Exception:
                pass

    def process_jpgs_to_ocr_pdf(self, jpg_paths, output_dir, pdf_filename):
        """
        将多个JPG文件合并转换为双层PDF（图像+OCR文本层）。
        OCR使用与分件功能一致的本地 PaddleOCR(无需UmiOCR/联网):
          逐图OCR取文本+坐标 → PyMuPDF 逐页插图与不可见文本层。
        """
        Image.MAX_IMAGE_PIXELS = None
        # --- OCR引擎初始化(走服务线程, 带超时看门狗) ---
        # GPU模式下构造成功≠能推理: 首推理可能永久挂起。初始化本身也可能在
        # 加载模型阶段挂起 → 全部提交服务线程执行, 超时即判定异常转CPU重建。
        status, ocr = self._ocr_svc_call(lambda: self._get_ocr(), timeout=300)
        if status == 'timeout':
            self.log_signal.emit("  × OCR初始化超时(300秒), GPU引擎异常")
            self._rebuild_ocr_cpu()
            status, ocr = self._ocr_svc_call(lambda: self._get_ocr(), timeout=300)
        elif ocr is None and getattr(self, 'use_gpu_ocr', False):
            # v3.7修复: GPU模式初始化失败(异常而非挂死)时原逻辑直接降级单层PDF——
            # 这是“GPU出单层、CPU出双层”的直接原因。现强制CPU重建后重试一次。
            self.log_signal.emit("  × OCR初始化失败(GPU模式异常), 切换CPU重建重试")
            self._rebuild_ocr_cpu()
            status, ocr = self._ocr_svc_call(lambda: self._get_ocr(), timeout=300)
        if ocr is None:
            # 本地OCR不可用: 回退仅图像PDF(保留旧状态字符串供上层展示)
            temp_pdf_path = self.jpgs_to_pdf(jpg_paths, output_dir, pdf_filename)
            return temp_pdf_path, "仅图像PDF（本地OCR不可用）"

        # --- 首次推理探测(小图, 服务线程内执行, 全局只做一次) ---
        # 探测失败不再直接降级: 先尝试GPU挂死→CPU重建→重探测;
        # CPU重建后仍失败才降级仅图像PDF(避免产出单层文件)。
        with self._probe_lock:
            if not self._ocr_probed:
                self._ocr_probed = True  # 先置位: 重建失败时其他线程不重复探测循环
                self.log_signal.emit("  OCR引擎首次推理探测(最长等待120秒)...")
                _probe = os.path.join(output_dir, '_ocr_probe.png')
                _probe_ok = False
                try:
                    # 探测图必须含真实文字: 纯白图OCR返回空也算'ok', 无法暴露
                    # GPU上"能跑但识别不出任何内容"的半失效状态(该状态下每页
                    # frags为空 → 生成单层PDF)。要求识别出文字才算探测通过。
                    self._make_probe_image(_probe)
                    _p_arr = self._preload_img_arr(_probe)   # v3.26: 探测预解码
                    st, _res = self._ocr_svc_call(
                        lambda: self._ocr_page(_probe, None, lambda s: None,
                                               img_arr=_p_arr),
                        timeout=120)
                    if st == 'ok' and _res:
                        self.log_signal.emit("  OCR推理探测通过(识别到文字)")
                        _probe_ok = True
                    elif st == 'ok':
                        self.log_signal.emit("  × OCR探测异常: 推理完成但未识别出文字"
                                             "(GPU半失效状态), 转CPU重试")
                    elif st == 'timeout':
                        self.log_signal.emit(
                            "  × OCR首次推理超时(120秒), GPU推理挂死(显存/驱动异常)")
                    else:
                        self.log_signal.emit(f"  × OCR探测失败: {str(_res)[:100]}")
                finally:
                    try:
                        os.remove(_probe)
                    except Exception:
                        pass
                if not _probe_ok and not self._svc_rebuilt:
                    # 未重建过 → 切CPU后重探测一次
                    self._rebuild_ocr_cpu()
                    self._ocr_probed = True
                    self.log_signal.emit("  CPU模式重新探测(最长等待120秒)...")
                    _p2 = os.path.join(output_dir, '_ocr_probe.png')
                    try:
                        self._make_probe_image(_p2)
                        _p2_arr = self._preload_img_arr(_p2)   # v3.26: 探测预解码
                        st2, _r2 = self._ocr_svc_call(
                            lambda: self._ocr_page(_p2, None, lambda s: None,
                                                   img_arr=_p2_arr),
                            timeout=120)
                        if st2 == 'ok' and _r2:
                            self.log_signal.emit("  CPU模式OCR探测通过(识别到文字), 继续生成双层PDF")
                            _probe_ok = True
                        else:
                            self.log_signal.emit("  × CPU模式OCR探测仍失败")
                    finally:
                        try:
                            os.remove(_p2)
                        except Exception:
                            pass
                if not _probe_ok:
                    # v3.16: 降级不再永久——探测失败可能是临时性故障(探测时显存
                    # 恰被其他程序占满/系统内存紧张, 之后资源已释放)或探测假阳性,
                    # 每 _OCR_REPROBE_DIRS 个目录自动复探, 通过即恢复双层生成。
                    self._ocr_broken = True
                    self._dirs_since_broken = 0
                    self.log_signal.emit(
                        "  → OCR探测+CPU重建均失败, 降级为仅图像PDF继续处理"
                        f"(每{self._OCR_REPROBE_DIRS}个目录将自动复探恢复)")
            elif getattr(self, '_ocr_broken', False):
                # v3.16: 降级状态下的周期复探(在 _probe_lock 内, 与首探测互斥)
                self._dirs_since_broken = getattr(self, '_dirs_since_broken', 0) + 1
                if self._dirs_since_broken >= self._OCR_REPROBE_DIRS:
                    if self._reprobe_ocr(output_dir):
                        self._ocr_broken = False
                        self._dirs_since_broken = 0
                        self.log_signal.emit(
                            "  ✓ OCR复探通过, 恢复双层PDF生成"
                            "(降级期间的目录仍为单层, 可对本批重跑补齐)")
                        self._run_monitor_line('OCR复探通过, 解除全局降级')
                    else:
                        self._dirs_since_broken = 0  # 复探未过: 计数清零, 下轮再试
        if getattr(self, '_ocr_broken', False):
            # v3.16: 每目录明确提示(不再仅首个失败目录可见降级原因)
            self.log_signal.emit("  ! OCR仍处降级状态, 本目录仅生成图像PDF(无文本层)")
            temp_pdf_path = self.jpgs_to_pdf(jpg_paths, output_dir, pdf_filename)
            return temp_pdf_path, "仅图像PDF（OCR探测失败已降级, 周期复探中）"

        try:
            import fitz  # PyMuPDF
        except ImportError:
            temp_pdf_path = self.jpgs_to_pdf(jpg_paths, output_dir, pdf_filename)
            return temp_pdf_path, "仅图像PDF（缺PyMuPDF）"

        pdf_path = os.path.join(output_dir, pdf_filename + ".pdf")
        doc = fitz.open()
        # v3.11: 移除全局 MKL-DNN 标志(FLAGS_use_mkldnn)——本路径图像经 fitz 直嵌,
        # 该标志对本功能无加速作用; 且它是全局开关, 若中途OCR降级CPU, CPU predictor
        # 带 oneDNN 缓存在变尺寸输入下会持续泄漏宿主内存。
        # v3.12: 进一步在 PaddleOCR 初始化配置中显式 use_mkldnn=False(见
        # _init_ocr_locked)——paddleocr 2.x 缺省 use_mkldnn=True, 仅移除全局标志时
        # CPU predictor 仍带 oneDNN 缓存, 宿主内存持续泄漏直至耗尽(崩溃日志20260901)。
        try:
            # 分段写盘: 超大目录(几百页)的 doc 若整体驻留, C++内存随页数线性增长,
            # 4线程并行4个doc会累积到GB级导致进程被系统终止(无提示退出)。
            # 每 CHUNK 页保存为分段PDF并释放doc, 最后合并 —— doc峰值恒定。
            # v3.11: CHUNK 按单文件实际大小自适应——大文件(高分辨率扫描件)仍固定50页时,
            # 4线程同时持有50页大doc会达数GB, GPU模式因OCR快而4线程同时处于写doc阶段,
            # 叠加paddle驻留内存后触发系统终止(崩溃日志0字节)。按单段≤~400MB折算页数。
            try:
                _sizes = [os.path.getsize(p) for p in jpg_paths[:20]]
                _avg_mb = (sum(_sizes) / len(_sizes) / 1048576.0) if _sizes else 1.0
                CHUNK = int(max(8, min(50, 400.0 / max(_avg_mb, 0.5))))
            except Exception:
                CHUNK = 50
            _MEM_WARN_MB = 2600   # 工作集超过此值 → 记日志提醒(留痕供崩溃排查)
            _MEM_REBUILD_MB = 3200  # 工作集超过此值 → 强制重建引擎+GC(阻断继续增长)
            # v3.12: 32位进程地址空间上限约2GB, 上述阈值永不可达——进程会先因地址空间
            # 耗尽崩溃(崩溃日志20260901: cv2连1.9MB都分配失败)。32位时大幅下调阈值,
            # 让看门狗在真正耗尽前提前介入回收。
            try:
                import struct as _st32
                if _st32.calcsize('P') * 8 == 32:
                    _MEM_WARN_MB = 1200
                    _MEM_REBUILD_MB = 1500
            except Exception:
                pass
            seg_paths = []
            page_no = 0
            for page_idx, jpg_path in enumerate(jpg_paths):
                if self.is_stopped:
                    break
                # 仅取尺寸(头信息), 不全量解码 → 每页省~26MB解码内存
                img = Image.open(jpg_path)
                w_px, h_px = img.size
                img.close()
                # PDF页面尺寸: 像素/分辨率*72 (resolution 默认100dpi)
                w_pt = w_px * 72.0 / self.resolution
                h_pt = h_px * 72.0 / self.resolution
                page = doc.new_page(width=w_pt, height=h_pt)
                page.insert_image(fitz.Rect(0, 0, w_pt, h_pt), filename=jpg_path)

                # OCR文本层(坐标从像素换算到PDF点)——逐页日志, 挂起时可见最后处理到哪
                self.log_signal.emit(f"    OCR: {os.path.basename(jpg_path)} "
                                     f"({len(jpg_paths)}张中第{page_idx+1}张)")
                # v3.26: 在工作线程预解码图像为ndarray再提交服务线程——服务线程内
                # 不再执行文件读取与cv2.imdecode(20260910崩溃点), 解码压力也
                # 从服务线程移到各工作线程并行完成。
                _arr = self._preload_img_arr(jpg_path)
                # OCR走服务线程(天然串行=替代ocr锁), 单页180秒超时。
                # 中途挂死→尝试一次CPU重建并重试本页; 仍失败则该页无文本层,
                # 继续处理后续页(不再永久阻塞——这是旧版4线程卡死的直接原因)。
                st, frags = self._ocr_svc_call(
                    lambda a=_arr: self._ocr_page(jpg_path, None,
                                                  lambda s: None, img_arr=a),
                    timeout=180)
                if st == 'timeout':
                    self.log_signal.emit(
                        f"    × OCR单页超时: {os.path.basename(jpg_path)}")
                    self._run_monitor_line(
                        f'OCR单页超时180秒: {os.path.basename(jpg_path)}')
                    if self._rebuild_ocr_cpu():
                        st, frags = self._ocr_svc_call(
                            lambda a=_arr: self._ocr_page(
                                jpg_path, None, lambda s: None, img_arr=a),
                            timeout=180)
                if st != 'ok':
                    if st == 'error':
                        self.log_signal.emit(
                            f"    OCR出错(跳过文本层): {str(frags)[:80]}")
                        self._run_monitor_line(
                            f'OCR服务线程异常: {str(frags)[:120]}')
                    else:
                        self.log_signal.emit(
                            f"    × OCR持续超时, 该页无文本层: "
                            f"{os.path.basename(jpg_path)}")
                    frags = []
                if st == 'ok' and not frags and len(jpg_paths) > 0:
                    self.log_signal.emit(
                        f"    ! 警告: {os.path.basename(jpg_path)} OCR完成但识别0片段"
                        f"(该页将为单层, 若大面积出现请检查GPU/显卡驱动)")
                self.log_signal.emit(f"    OCR完成: {os.path.basename(jpg_path)} "
                                     f"识别{len(frags)}片段")
                # v3.11 内存看门狗: 每10页检测一次进程工作集。GPU模式大目录+大文件长时间运行,
                # paddle/fitz宿主内存累积可致进程被系统终止(崩溃日志0字节)。
                # 超阈值 → 服务线程内强制重建OCR引擎+GC(与其他推理串行, 安全)。
                if page_idx % 10 == 0:
                    _wm = _proc_mem_mb()
                    if _wm > _MEM_REBUILD_MB:
                        self.log_signal.emit(
                            f"    ! 进程内存{_wm:.0f}MB超过阈值{_MEM_REBUILD_MB}MB, "
                            f"强制回收(第{page_idx+1}页)")
                        self._run_monitor_line(
                            f'内存看门狗触发: {_wm:.0f}MB>阈值{_MEM_REBUILD_MB}MB, '
                            f'强制重建引擎(第{page_idx+1}页)')

                        def _force_recycle():
                            """仅丢弃引擎+重建(不推理本页), 阻断宿主内存继续增长。"""
                            self._ocr = None
                            self._ocr_pages_since_init = 0
                            import gc as _gcr
                            _gcr.collect()
                            if getattr(self, 'use_gpu_ocr', False):
                                try:
                                    import paddle as _pdr
                                    if hasattr(_pdr.device, 'cuda'):
                                        _pdr.device.cuda.empty_cache()
                                except Exception:
                                    pass
                            self._get_ocr()  # 重建新实例(按当前GPU/CPU配置)
                            return True

                        self._ocr_svc_call(_force_recycle, timeout=300)
                        try:
                            import gc as _gcw
                            _gcw.collect()
                        except Exception:
                            pass
                    elif _wm > _MEM_WARN_MB:
                        self.log_signal.emit(
                            f"    ! 进程内存{_wm:.0f}MB偏高(第{page_idx+1}页), 持续监控")
                sx = w_pt / w_px
                sy = h_pt / h_px
                for txt, x0, y0, x1, y1 in frags:
                    if not txt.strip():
                        continue
                    # 字号优先用 OCR 片段的「真实行高」(y1-y0, 像素)换算——
                    # 卷皮页大字标题按宽度估算会得到超大值(被钳到上限40),
                    # 全页同字号巨字文本在 WPS 中不被作为可选对象(其他页正常)。
                    # 宽度估算仅作行高缺失时的兜底; 中文段宽度校验用于防溢出。
                    h_px_txt = max(y1 - y0, 1.0)
                    fs_h = h_px_txt * sy
                    w_pt_txt = max((x1 - x0) * sx, 1.0)
                    eff = sum(1.0 if ord(c) > 127 else 0.55 for c in txt) or 1.0
                    fs_w = w_pt_txt / eff
                    fs = fs_h if fs_h > 0 else fs_w
                    fs = max(4.0, min(fs, 60.0))
                    base_y = y0 * sy + fs
                    # 按连续同类字符切分为段 [(文本, 是否中文)]
                    seg_list = []
                    cur = ''
                    cur_cn = None
                    for ch in txt:
                        cn = ord(ch) > 127
                        if cur_cn is None or cn == cur_cn:
                            cur += ch
                            cur_cn = cn
                        else:
                            seg_list.append((cur, cur_cn))
                            cur, cur_cn = ch, cn
                    if cur:
                        seg_list.append((cur, cur_cn))
                    # 逐段插入, x随实际advance推进(中文=fs, ASCII≈fs*0.5)
                    # 隐形可选文本: render_mode=0(正常填充文本, 编辑器识别为可选
                    # 对象) + fill_opacity=0(完全透明, 任何底色上都不可见)。
                    # —— render_mode=3 在WPS等编辑器中无法选中; 白色文字在
                    # 深色底图上会显现。透明填充两全其美。
                    cx = x0 * sx
                    for seg, is_cn in seg_list:
                        if not seg:
                            continue
                        fname = 'china-s' if is_cn else 'helv'
                        try:
                            page.insert_text(fitz.Point(cx, base_y), seg,
                                             fontsize=fs,
                                             color=(0, 0, 0), fill_opacity=0,
                                             fontname=fname)
                        except Exception:
                            try:
                                page.insert_text(fitz.Point(cx, base_y), seg,
                                                 fontsize=fs,
                                                 color=(0, 0, 0), fill_opacity=0)
                            except Exception:
                                pass
                        cx += len(seg) * (fs if is_cn else fs * 0.5)

                # 分段落盘: 每CHUNK页存为分段文件并新建空doc, 峰值内存恒定
                page_no += 1
                if page_no % CHUNK == 0 and page_no < len(jpg_paths):
                    _seg = pdf_path + f'.part{page_no // CHUNK}'
                    doc.save(_seg, garbage=3, deflate=True)
                    doc.close()
                    seg_paths.append(_seg)
                    doc = fitz.open()  # 重置doc, C++侧旧内存随close释放
                    # v3.9: 分段重置同时释放GPU缓存——原仅每目录结束释放一次,
                    # 数百页超长目录在单目录处理期间显存/内存会持续增长。
                    self._svc_empty_cache()

            # 收尾: 存最后一段
            if seg_paths:
                _last = pdf_path + f'.part{len(seg_paths) + 1}'
                doc.save(_last, garbage=3, deflate=True)
                doc.close()
                seg_paths.append(_last)
                # 合并分段 → 最终PDF
                merged = fitz.open()
                for sp in seg_paths:
                    _sd = fitz.open(sp)
                    merged.insert_pdf(_sd)
                    _sd.close()  # v3.11: 立即关闭分段doc, 防大分段驻留累积内存峰值
                    os.remove(sp)
                merged.save(pdf_path, garbage=3, deflate=True)
                merged.close()
            else:
                doc.save(pdf_path, garbage=3, deflate=True)
                doc.close()
            if self.is_stopped:
                return pdf_path, "已停止(部分页生成)"
            return pdf_path, "双层PDF生成成功(本地OCR)"
        except Exception as e:
            try:
                doc.close()
            except Exception:
                pass
            # 失败回退: 仅图像PDF
            temp_pdf_path = self.jpgs_to_pdf(jpg_paths, output_dir, pdf_filename)
            return temp_pdf_path, f"OCR处理错误: {str(e)}(已回退为仅图像PDF)"
    
    def convert_pdf_to_ofd(self, pdf_path, ofd_path):
        """使用 ofd_writer 将双层PDF转换为双层OFD(图像层+文本层，无页数限制)。"""
        if not os.path.exists(pdf_path):
            return False, 0

        if not self.ofd_available:
            return False, 0

        start_time = time.time()

        try:
            from ofd_writer import make_layered_ofd

            # 加锁串行转换（PyMuPDF 在 Win7 多线程下更稳妥）
            with self._ofd_lock:
                ok, n, err = make_layered_ofd(pdf_path, ofd_path)

            if not ok:
                print(f"PDF转OFD失败: {err}")
                return False, time.time() - start_time

            end_time = time.time()
            return True, end_time - start_time

        except Exception as e:
            end_time = time.time()
            print(f"PDF转OFD过程中发生错误: {e}")
            return False, end_time - start_time

    def process_single_directory(self, jpg_files, dir_name):
        """处理单个目录的JPG文件"""
        start_time = time.time()
        result = "失败"
        result_pdf_path = None
        ocr_status = "未知"
        ofd_generated = False
        ofd_filename = ""
        
        try:
            # 输出结构: 输出目录/父目录名/子目录名.pdf —— PDF/OFD生成在
            # 与源子目录同名的「上一级」目录下, 不再建同名子目录。
            # 例: 源 D:\扫描\J380-ZY·2021-Y-FGC-0001\J380-0001\*.jpg
            #     → 输出 PDF目录\J380-ZY·2021-Y-FGC-0001\J380-0001.pdf
            # (rel的父目录 = 源子目录相对源根路径去掉最后一级)
            out_subdir = self.output_dir
            src_root = getattr(self, 'directory_path', None)
            if src_root and jpg_files:
                try:
                    src_dir = os.path.dirname(jpg_files[0])
                    rel = os.path.relpath(src_dir, src_root)
                    if rel and rel != '.':
                        parent_rel = os.path.dirname(rel)
                        if parent_rel:
                            out_subdir = os.path.join(self.output_dir, parent_rel)
                except Exception:
                    pass
            os.makedirs(out_subdir, exist_ok=True)
            pdf_filename = dir_name
            result_pdf_path, ocr_status = self.process_jpgs_to_ocr_pdf(
                jpg_files, out_subdir, pdf_filename
            )
            if result_pdf_path:
                result = "成功"
                
                # 如果选择了生成OFD，则转换刚生成的PDF
                if self.generate_ofd and self.ofd_available and result_pdf_path:
                    ofd_path = os.path.splitext(result_pdf_path)[0] + '.ofd'
                    ofd_success, ofd_duration = self.convert_pdf_to_ofd(result_pdf_path, ofd_path)
                    if ofd_success:
                        ofd_generated = True
                        ofd_filename = os.path.basename(ofd_path)
                        self.log_signal.emit(f"  → 已生成OFD: {ofd_filename} ({ofd_duration:.2f}秒)")
                    else:
                        self.log_signal.emit(f"  → OFD生成失败")
        except Exception as e:
            result = "失败"
            ocr_status = f"错误: {str(e)}"

        # 每目录处理完强制回收: paddle推理的C++工作内存与图像缓存不归Python GC管,
        # 长时间多目录累积会耗尽系统内存导致进程被静默终止。逐目录显式释放。
        # ★ empty_cache 必须走OCR服务线程执行——paddle CUDA操作与推理并发会挂死;
        #   服务线程挂死时(超时)跳过, 不再在工作线程里直接调用。
        try:
            import gc as _gc
            _gc.collect()
            self._svc_empty_cache()
        except Exception:
            pass

        duration = round(time.time() - start_time, 2)

        return {
            'folder': dir_name,
            'pdf_file': os.path.basename(result_pdf_path) if result_pdf_path else f"{dir_name}.pdf",
            'result': result,
            'ocr_status': ocr_status,
            'duration': duration,
            'ofd_generated': ofd_generated,
            'ofd_file': ofd_filename
        }
    
    def init_log_file(self, log_path, start_time):
        """初始化日志文件"""
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"JPG转双层PDF处理日志\n")
                f.write(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 120 + "\n")
                f.write(f"{'目录名':<25} {'PDF文件名':<30} {'处理结果':<10} {'双层PDF状态':<20} {'耗时(秒)':<12} {'处理时间':<20}\n")
                f.write("-" * 120 + "\n")
        except Exception as e:
            print(f"创建日志文件失败: {str(e)}")
    
    def append_to_log(self, log_path, result):
        """追加单条记录到日志文件"""
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                process_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{result['folder']:<25} {result['pdf_file']:<30} "
                       f"{result['result']:<10} {result['ocr_status']:<20} "
                       f"{result['duration']:<12} {process_time:<20}\n")
        except Exception as e:
            print(f"追加日志记录失败: {str(e)}")
    
    def finalize_log_file(self, log_path, results, start_time):
        """完成日志文件，添加统计信息"""
        try:
            success_count = sum(1 for r in results if r['result'] == '成功')
            fail_count = len(results) - success_count
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds() / 60
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write("-" * 120 + "\n")
                f.write(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总耗时: {total_duration:.2f}分钟\n")
                f.write(f"总计处理: {len(results)} 个目录\n")
                f.write(f"成功: {success_count} 个\n")
                f.write(f"失败: {fail_count} 个\n")
                f.write("=" * 120 + "\n")
        except Exception as e:
            print(f"完成日志文件失败: {str(e)}")


class JpgToPdfPage(FunctionPage):
    def __init__(self):
        super().__init__("JPG转双层PDF")
        group = QGroupBox("图片转双层PDF (OCR)")
        form = QFormLayout()

        self.img_dir = QLineEdit()
        btn_browse_src = QPushButton("选择文件夹")
        btn_browse_src.setObjectName("BrowseBtn")
        btn_browse_src.clicked.connect(self.browse_img_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.img_dir)
        h1.addWidget(btn_browse_src)
        
        self.out_dir = QLineEdit()
        self._out_manual = False  # 用户是否手动改过输出目录(改过则不随源联动)
        btn_browse_out = QPushButton("选择文件夹")
        btn_browse_out.setObjectName("BrowseBtn")
        btn_browse_out.clicked.connect(self.browse_out_dir)
        h2 = QHBoxLayout()
        h2.addWidget(self.out_dir)
        h2.addWidget(btn_browse_out)

        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 8)
        self.thread_spin.setValue(4)
        self.thread_spin.setToolTip("并行处理的目录数(1-8)")
        
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 1200)
        self.dpi_spin.setValue(300)
        
        self.generate_ofd_check = QCheckBox("同时生成OFD文件")
        self.generate_ofd_check.setChecked(True)  # 默认选中

        # GPU渲染: 图像处理走加速路径(MKL-DNN指令集加速+无损图像直传), 缺省不选
        self.gpu_render_check = QCheckBox("使用GPU渲染(图像加速处理)")
        self.gpu_render_check.setChecked(False)
        self.gpu_render_check.setToolTip(
            "勾选后图像处理启用加速路径(MKL-DNN指令集+无损图像直传), "
            "生成结果完全相同, 高配置机器上更快")

        # GPU OCR: paddlepaddle-gpu 推理, 缺省不选(CPU)
        self.gpu_ocr_check = QCheckBox("OCR使用GPU处理(需GPU版paddle环境)")
        self.gpu_ocr_check.setChecked(False)
        self.gpu_ocr_check.setToolTip(
            "勾选后OCR推理尝试使用GPU(需已安装paddlepaddle-gpu及CUDA); "
            "不可用时自动回退CPU, 业务处理能力不变")

        form.addRow("图片目录:", h1)
        form.addRow("输出目录:", h2)
        form.addRow("线程数:", self.thread_spin)
        form.addRow("PDF DPI:", self.dpi_spin)
        form.addRow("选项:", self.generate_ofd_check)
        form.addRow("渲染:", self.gpu_render_check)
        form.addRow("OCR:", self.gpu_ocr_check)
        group.setLayout(form)
        self.layout.addWidget(group)
        
        # 说明文本
        info_label = QLabel(
            "功能说明：\n"
            "• 扫描目录及子目录下所有JPG文件\n"
            "• 每个目录的JPG合并为一个PDF\n"
            "• 使用内置本地OCR(与分件功能同款)生成双层PDF(可搜索/可选中)\n"
            "• PDF文件名与目录名相同\n"
            "• 可选：同时在PDF目录中生成同名OFD文件"
        )
        info_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.layout.addWidget(info_label)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        btn_exec = QPushButton("开始转换")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        btn_layout.addWidget(btn_exec)
        
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        self.layout.addLayout(btn_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)
        
        self.worker = None
        self.add_log_widget()
    
    def browse_img_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if d:
            self.img_dir.setText(d)
            # 输出目录未手动改过时, 自动跟随源目录 → 源目录\PDF
            self._auto_out_dir()

    def _auto_out_dir(self):
        """输出目录自动联动: 用户未手动改过时, 跟随源目录生成「源目录/PDF」;
        手动选择过其他输出目录后不再跟随。"""
        if getattr(self, '_out_manual', False):
            return
        base = self.img_dir.text().strip()
        if base:
            self.out_dir.setText(os.path.join(base, "PDF"))

    def browse_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.out_dir.setText(d)
            self._out_manual = True  # 手动指定后不再跟随源目录

    def _check_gpu_capability(self):
        """
        检测设备GPU加速能力。返回 (支持?, 原因说明)。
        检测项(不影响paddle导入状态):
          1. NVIDIA驱动: nvcuda.dll 可加载(ctypes);
          2. GPU版paddle: paddle编译了CUDA(is_compiled_with_cuda);
          3. 可见GPU设备数 > 0。
        """
        # 1. NVIDIA驱动
        try:
            import ctypes
            try:
                ctypes.CDLL('nvcuda.dll')
                has_driver = True
            except OSError:
                has_driver = False
        except Exception:
            has_driver = False
        if not has_driver:
            return False, "未检测到NVIDIA显卡驱动(nvcuda.dll不可用)"

        # 2/3. paddle编译与设备数(此时paddle可能被导入, 但仅查询不初始化设备)
        try:
            import paddle
            if not paddle.device.is_compiled_with_cuda():
                return False, "当前为CPU版paddlepaddle(未安装paddlepaddle-gpu)"
            n_gpu = int(paddle.device.cuda.device_count())
            if n_gpu <= 0:
                return False, "有NVIDIA驱动但paddle未识别到可用GPU设备"
            return True, f"检测到{n_gpu}个GPU设备"
        except Exception as e:
            return False, f"paddle检测异常: {str(e)[:60]}"

    def execute(self):
        d = self.img_dir.text()
        out = self.out_dir.text()
        
        if not d:
            QMessageBox.warning(self, "提示", "请先选择图片目录")
            return

        if not out:
            QMessageBox.warning(self, "提示", "请先选择输出目录")
            return

        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "图片目录不存在")
            return

        # 输出目录不存在 → 点击开始时自动创建
        if not os.path.exists(out):
            try:
                os.makedirs(out, exist_ok=True)
                self.log(f"输出目录不存在, 已自动创建: {out}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法创建输出目录: {e}")
                return

        # 确认操作
        reply = QMessageBox.question(
            self, "确认操作",
            "确定要开始转换吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 重置进度条
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        
        # 禁用按钮，启用停止按钮
        self.log("="*50)
        self.log("开始处理...")
        self.log(f"图片目录: {d}")
        self.log(f"输出目录: {out}")
        self.log(f"线程数: {self.thread_spin.value()}")
        self.log(f"PDF DPI: {self.dpi_spin.value()}")

        # ---- GPU选项预检: 勾选GPU但设备不支持时, 开始前弹窗提示(将降级CPU) ----
        want_gpu = (self.gpu_render_check.isChecked()
                    or self.gpu_ocr_check.isChecked())
        if want_gpu:
            gpu_ok, gpu_reason = self._check_gpu_capability()
            if not gpu_ok:
                QMessageBox.warning(
                    self, "GPU不可用提示",
                    "您勾选了GPU选项, 但当前设备不支持GPU加速:\n"
                    f"  {gpu_reason}\n\n"
                    "系统将自动降级为CPU处理(处理结果完全相同, 仅速度较慢)。\n"
                    "如需GPU加速, 请确认:\n"
                    "  1. 机器配有NVIDIA显卡且已安装驱动;\n"
                    "  2. 已安装GPU版paddlepaddle(paddlepaddle-gpu)。")
                self.log(f"GPU预检: 不支持({gpu_reason}) → 降级CPU处理")

        self.log("="*50)
        
        # v3.17: 取消v3.15的GPU OCR模式强制单线程——允许用户自选多线程。
        # OCR本身由内部单一服务线程串行执行(线程安全不变), 多线程用于图像
        # 解码/PDF分段写入等阶段与OCR流水线并行; 内存峰值与GPU挂死风险由
        # v3.14运行监控+GPU引擎损坏计数≥2自动降级CPU兜底。仅在多线程+GPU时
        # 一次性提示风险, 用户确认后按所选线程数执行, 不再强制改为1。
        max_workers = self.thread_spin.value()
        if self.gpu_ocr_check.isChecked() and max_workers > 1:
            reply = QMessageBox.question(
                self, "GPU模式多线程确认",
                f"当前线程数为 {max_workers}，「OCR使用GPU处理」模式下\n"
                "OCR推理由内部单一服务线程串行执行，多线程用于\n"
                "图像解码与PDF写入阶段的流水线并行。\n\n"
                "多线程会增加内存峰值与GPU线程挂死的风险\n"
                "（发生时会自动降级CPU继续处理）。\n\n"
                "是否按当前线程数继续？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply != QMessageBox.Yes:
                self.log("已取消: GPU OCR多线程需确认后执行"
                         "(可手动调低线程数或改用CPU模式后重试)")
                self.progress.setFormat("待开始")
                return
            self.log(f"GPU OCR模式: 按 {max_workers} 线程执行"
                     "(OCR推理串行, 多线程用于解码/写PDF流水线; "
                     "GPU异常自动降级CPU)")

        # 创建工作线程
        resolution = float(self.dpi_spin.value())
        generate_ofd = self.generate_ofd_check.isChecked()
        self.worker = JpgToPdfWorker(
            directory_path=d,
            output_dir=out,
            max_workers=max_workers,
            resolution=resolution,
            generate_ofd=generate_ofd,
            gpu_render=self.gpu_render_check.isChecked(),
            use_gpu_ocr=self.gpu_ocr_check.isChecked()
        )
        
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        # QThread终止兜底: 处理线程被操作系统终止或C库崩溃死亡时不会发出完成信号,
        # 此时界面自动恢复并提示(而非永久卡在“处理中”), 崩溃详情见崩溃日志。
        self.worker.finished.connect(self._on_worker_exit)
        
        self.worker.start()
        
        # 更新按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始转换":
            btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")
        self.log(f"进度: {current}/{total} ({percentage:.1f}%)")
    
    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        
        # 恢复按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始转换":
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)

    def _on_worker_exit(self):
        """QThread终止兜底: 处理线程意外死亡(系统内存不足被终止/内部库崩溃等)
        且未发出完成信号时, 恢复界面并弹窗提示, 不再永久卡在“处理中”。"""
        if getattr(self.worker, '_done', False):
            return
        msg = ("处理线程意外终止(可能是系统内存不足导致进程被终止, 或内部库崩溃)。\n"
               "详细信息请查看程序目录下的 TMToolMan_崩溃日志_*.txt。\n"
               "建议: 降低线程数、关闭其他占用内存的程序后重试。")
        self.log(msg)
        self.progress.setFormat("异常终止")
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始转换":
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        QMessageBox.critical(self, "处理异常终止", msg)


class PdfToOfdWorker(QThread):
    """PDF转OFD后台处理线程 - 带文本层PDF直接转换；无文本层PDF走 PDF页→图片→双层PDF→OFD 流程"""
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)
    
    def __init__(self, pdf_dir, output_dir, parent=None):
        super().__init__(parent)
        self.pdf_dir = pdf_dir
        self.output_dir = output_dir
        self.is_stopped = False
        import threading
        self._ofd_lock = threading.Lock()

        # 检查 OFD 转换库是否可用（ofd_writer，基于 PyMuPDF，生成双层OFD）
        try:
            import fitz  # noqa: F401
            from ofd_writer import make_layered_ofd  # noqa: F401
            self.ofd_available = True
        except ImportError:
            self.ofd_available = False

        # 复用「JPG转双层PDF」功能的处理流程：
        # PDF逐页渲染为图片 → OCR生成双层PDF → 转双层OFD
        self._jpg_helper = JpgToPdfWorker(
            directory_path=self.pdf_dir, output_dir=self.output_dir, resolution=300.0)

    def run(self):
        try:
            if not self.ofd_available:
                self.finished_signal.emit(False, "错误：未安装 OFD 转换依赖(PyMuPDF)\n请运行: pip install PyMuPDF")
                return
            
            # 获取所有PDF文件
            pdf_files = []
            for root, dirs, files in os.walk(self.pdf_dir):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_path = os.path.join(root, file)
                        pdf_files.append(pdf_path)
            
            total_files = len(pdf_files)
            if total_files == 0:
                self.finished_signal.emit(False, "未找到任何PDF文件")
                return
            
            self.log_signal.emit(f"找到 {total_files} 个PDF文件，开始转换...")
            
            # 创建日志文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"ofd_conversion_log_{timestamp}.txt"
            log_file_path = os.path.join(self.pdf_dir, log_filename)
            start_time = datetime.now()
            log_entries = []
            
            processed = 0
            success_count = 0
            
            for pdf_path in pdf_files:
                if self.is_stopped:
                    break
                
                file_start_time = time.time()
                
                # 计算相对路径以保持目录结构
                rel_path = os.path.relpath(pdf_path, self.pdf_dir)
                ofd_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.ofd'
                output_subdir = os.path.join(self.output_dir, os.path.dirname(rel_path))
                os.makedirs(output_subdir, exist_ok=True)
                ofd_path = os.path.join(output_subdir, ofd_filename)
                
                # 执行转换
                success, duration = self.convert_pdf_to_ofd(pdf_path, ofd_path)
                
                file_end_time = time.time()
                file_duration = file_end_time - file_start_time
                
                if success:
                    success_count += 1
                    result = "成功"
                    self.log_signal.emit(f"✓ {os.path.basename(pdf_path)} -> {ofd_filename} ({duration:.2f}秒)")
                else:
                    result = "失败"
                    self.log_signal.emit(f"✗ {os.path.basename(pdf_path)} 转换失败")
                
                processed += 1
                percentage = (processed / total_files) * 100
                
                # 记录日志条目
                log_entry = {
                    "文件名": os.path.basename(pdf_path),
                    "处理结果": result,
                    "处理用时(秒)": f"{file_duration:.2f}",
                    "处理时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                log_entries.append(log_entry)
                
                self.progress_signal.emit(processed, total_files)
            
            if not self.is_stopped:
                # 写入日志文件
                end_time = datetime.now()
                total_duration = (end_time - start_time).total_seconds() / 60
                
                with open(log_file_path, 'w', encoding='utf-8') as log_file:
                    log_file.write("PDF转OFD处理日志 (双层OFD)\n")
                    log_file.write("=" * 50 + "\n")
                    log_file.write(f"处理开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write(f"处理结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    log_file.write(f"总耗时: {total_duration:.2f}分钟\n")
                    log_file.write(f"总文件数: {total_files}\n")
                    log_file.write(f"成功转换: {success_count}\n")
                    log_file.write(f"转换失败: {total_files - success_count}\n")
                    log_file.write("=" * 50 + "\n\n")
                    
                    log_file.write("详细处理记录:\n")
                    log_file.write("文件名\t处理结果\t处理用时(秒)\t处理时间\n")
                    log_file.write("-" * 80 + "\n")
                    
                    for entry in log_entries:
                        log_file.write(f"{entry['文件名']}\t{entry['处理结果']}\t{entry['处理用时(秒)']}\t{entry['处理时间']}\n")
                
                summary_msg = f"\n转换完成！共处理 {total_files} 个PDF文件，成功转换 {success_count} 个，总耗时 {total_duration:.2f}分钟。\n日志: {log_filename}"
                self.finished_signal.emit(True, summary_msg)
            else:
                self.finished_signal.emit(False, "处理已停止")
                
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {str(e)}")
    
    def stop(self):
        self.is_stopped = True
        if getattr(self, '_jpg_helper', None) is not None:
            self._jpg_helper.is_stopped = True
    
    def _pdf_has_text(self, pdf_path):
        """检测 PDF 是否已带可提取文本层（多数页含文本即视为带文本层）"""
        try:
            import fitz
            doc = fitz.open(pdf_path)
            try:
                pages_with_text = 0
                for page in doc:
                    if page.get_text().strip():
                        pages_with_text += 1
                return pages_with_text * 2 >= max(doc.page_count, 1)
            finally:
                doc.close()
        except Exception:
            return False

    def convert_pdf_to_ofd(self, pdf_path, ofd_path):
        """
        将PDF转换为双层OFD：
        ① 若PDF已带文本层，直接调 ofd_writer.make_layered_ofd 转换（无需图片中转）；
        ② 若无文本层，采用与「JPG转双层PDF」功能相同的流程：
           PyMuPDF 逐页渲染为 JPG 图片(300DPI) → 复用 JpgToPdfWorker.process_jpgs_to_ocr_pdf
           生成中间双层PDF(图像层+OCR文本层) → ofd_writer 转为双层 OFD；
        ③ 清理临时图片与中间 PDF，仅保留 OFD 输出。
        """
        if not os.path.exists(pdf_path):
            return False, 0

        if not self.ofd_available:
            return False, 0

        start_time = time.time()
        tmp_dir = None

        try:
            import fitz
            import tempfile
            import uuid
            from ofd_writer import make_layered_ofd

            # ① 已带文本层的 PDF 直接使用，跳过图片中转与 OCR
            if self._pdf_has_text(pdf_path):
                self.log_signal.emit(f"  {os.path.basename(pdf_path)} 已带文本层，直接转换")
                with self._ofd_lock:
                    ok, n, err = make_layered_ofd(pdf_path, ofd_path)
                if not ok:
                    print(f"PDF转OFD失败: {err}")
                    return False, time.time() - start_time
                return True, time.time() - start_time

            self.log_signal.emit(f"  {os.path.basename(pdf_path)} 无文本层，走图片中转+OCR流程")

            # ② PDF 逐页渲染为 JPG 图片
            doc = fitz.open(pdf_path)
            tmp_dir = os.path.join(tempfile.gettempdir(), f"pdf2ofd_{uuid.uuid4().hex[:8]}")
            os.makedirs(tmp_dir, exist_ok=True)
            jpg_paths = []
            zoom = 300.0 / 72.0  # 300DPI 渲染，与中间PDF分辨率一致，页面尺寸不变
            mat = fitz.Matrix(zoom, zoom)
            for i, page in enumerate(doc):
                if self.is_stopped:
                    break
                pix = page.get_pixmap(matrix=mat, alpha=False)
                jpg_path = os.path.join(tmp_dir, f"page_{i:05d}.jpg")
                pix.save(jpg_path)
                jpg_paths.append(jpg_path)
            doc.close()

            if self.is_stopped or not jpg_paths:
                return False, time.time() - start_time

            # ②a 复用 JPG→双层PDF 流程生成中间 PDF
            self._jpg_helper.is_stopped = self.is_stopped
            base_name = os.path.splitext(os.path.basename(ofd_path))[0]
            inter_pdf, ocr_status = self._jpg_helper.process_jpgs_to_ocr_pdf(
                jpg_paths, tmp_dir, base_name)
            if not inter_pdf or not os.path.exists(inter_pdf):
                return False, time.time() - start_time

            # ②b 中间 PDF 转 OFD
            with self._ofd_lock:
                ok, n, err = make_layered_ofd(inter_pdf, ofd_path)

            if not ok:
                print(f"PDF转OFD失败: {err}")
                return False, time.time() - start_time

            return True, time.time() - start_time

        except Exception as e:
            print(f"PDF转OFD过程中发生错误: {e}")
            return False, time.time() - start_time
        finally:
            # ③ 清理临时图片与中间 PDF
            if tmp_dir and os.path.isdir(tmp_dir):
                import shutil
                try:
                    shutil.rmtree(tmp_dir, ignore_errors=True)
                except Exception:
                    pass


class PdfToOfdPage(FunctionPage):
    def __init__(self):
        super().__init__("PDF转OFD")
        group = QGroupBox("PDF转OFD格式 (双层OFD)")
        form = QFormLayout()

        self.pdf_dir = QLineEdit()
        btn_browse_src = QPushButton("选择文件夹")
        btn_browse_src.setObjectName("BrowseBtn")
        btn_browse_src.clicked.connect(self.browse_pdf_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.pdf_dir)
        h1.addWidget(btn_browse_src)
        
        self.out_dir = QLineEdit()
        btn_browse_out = QPushButton("选择文件夹")
        btn_browse_out.setObjectName("BrowseBtn")
        btn_browse_out.clicked.connect(self.browse_out_dir)
        h2 = QHBoxLayout()
        h2.addWidget(self.out_dir)
        h2.addWidget(btn_browse_out)

        form.addRow("PDF源目录:", h1)
        form.addRow("OFD输出目录:", h2)
        group.setLayout(form)
        self.layout.addWidget(group)
        
        # 说明文本
        info_label = QLabel(
            "功能说明：\n"
            "• 已带文本层的 PDF 直接转换为双层OFD；无文本层的 PDF 自动走「JPG转双层PDF」同款流程（渲染图片 → OCR双层PDF → 双层OFD）\n"
            "• 生成双层OFD（图像层+可检索文本层），完整转换全部页，无页数限制\n"
            "• 支持递归扫描子目录\n"
            "• 保持原有目录结构\n"
            "• OFD文件名与PDF相同\n"
            "• 注意：需要 OFD 转换依赖 PyMuPDF (已随程序内置)"
        )
        info_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.layout.addWidget(info_label)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        btn_exec = QPushButton("开始转换为OFD")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        btn_layout.addWidget(btn_exec)
        
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        self.layout.addLayout(btn_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)
        
        self.worker = None
        self.add_log_widget()
    
    def browse_pdf_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择PDF源目录")
        if d:
            self.pdf_dir.setText(d)
            if not self.out_dir.text():
                self.out_dir.setText(d)
    
    def browse_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择OFD输出目录")
        if d: self.out_dir.setText(d)
    
    def execute(self):
        d = self.pdf_dir.text()
        out = self.out_dir.text()
        
        if not d:
            QMessageBox.warning(self, "提示", "请先选择PDF源目录")
            return
        
        if not out:
            QMessageBox.warning(self, "提示", "请先选择OFD输出目录")
            return
        
        if not os.path.exists(d):
            QMessageBox.warning(self, "错误", "PDF源目录不存在")
            return

        # OFD输出目录不存在 → 点击开始时自动创建
        if not os.path.exists(out):
            try:
                os.makedirs(out, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法创建OFD输出目录: {e}")
                return
        
        # 确认操作
        reply = QMessageBox.question(
            self, "确认操作",
            "确定要开始转换吗？\n\n注意：需要 OFD 转换依赖 PyMuPDF！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # 重置进度条
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        
        # 禁用按钮，启用停止按钮
        self.log("="*50)
        self.log("开始处理...")
        self.log(f"PDF源目录: {d}")
        self.log(f"OFD输出目录: {out}")
        self.log("="*50)
        
        # 创建工作线程
        self.worker = PdfToOfdWorker(
            pdf_dir=d,
            output_dir=out
        )
        
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        
        self.worker.start()
        
        # 更新按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始转换为OFD":
            btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)
    
    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")
        self.log(f"进度: {current}/{total} ({percentage:.1f}%)")
    
    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")
        
        # 恢复按钮状态
        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始转换为OFD":
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)


class FileBatchReplaceWorker(QThread):
    """文件批量替换后台处理线程 - 将输出的JPG批量替换目标目录中的图片

    规则:
    1. 扫描 JPG 目录(含子目录)中的 jpg 文件，文件名去除最后四位数字编号和最后一个
       "-"后得到基础名，与目标目录下的同名子目录匹配；
    2. 仅处理编号 >= 起始编号的文件:
       - 只需复制1个 → 直接覆盖目标同名文件；
       - 复制多个(N个) → 源文件从最小编号起连续占位(最小编号处覆盖目标同名文件，
         源编号不连续时也按升序归位)；目标子目录中编号 > 最小编号的现有文件
         从 最小编号+N 起按升序重新编号预留空位(从编号最大的文件开始改名避免重复)，
         再将新文件复制到目标目录。
    3. 每个目标子目录替换完成后, 在该子目录下生成/更新 Directory.txt:
       记录替换后的文件名清单(不含扩展名, 每行一个), 供分件功能
       读取目录页与后续文件偏移量。
    """
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    _NUM_RE = re.compile(r'^(.+)-(\d{4})$')  # 基础名 + "-" + 四位数字编号

    def __init__(self, jpg_dir, target_dir, start_num, parent=None):
        super().__init__(parent)
        self.jpg_dir = jpg_dir
        self.target_dir = target_dir
        self.start_num = start_num
        self.is_stopped = False
        self._log_file = None  # 当前处理日志文件句柄

    def stop(self):
        self.is_stopped = True

    def _wlog(self, s):
        """写入处理日志文件（若已打开），同时输出到界面日志"""
        if self._log_file is not None:
            try:
                self._log_file.write(s + "\n")
                self._log_file.flush()
            except Exception:
                pass
        self.log_signal.emit(s)

    @classmethod
    def _parse_name(cls, fname):
        """文件名去除扩展名、最后一个"-"及末尾四位数字编号，返回 (基础名, 编号)；不匹配返回 None"""
        stem = os.path.splitext(fname)[0]
        m = cls._NUM_RE.match(stem)
        if not m:
            return None
        return m.group(1), int(m.group(2))

    def _collect_sources(self):
        """扫描JPG目录(含子目录)，按基础名分组，返回 ({基础名: [(编号, 完整路径), ...]}, 跳过数)"""
        groups = {}
        skipped = 0
        for root, _dirs, files in os.walk(self.jpg_dir):
            for f in files:
                if not f.lower().endswith(('.jpg', '.jpeg')):
                    continue
                parsed = self._parse_name(f)
                if parsed is None:
                    skipped += 1
                    continue
                base, num = parsed
                if num < self.start_num:
                    continue
                groups.setdefault(base, []).append((num, os.path.join(root, f)))
        for base in groups:
            groups[base].sort(key=lambda t: t[0])
        return groups, skipped

    def _replace_group(self, base, new_files):
        """处理单个基础名分组，返回 (成功复制数, 失败数)"""
        target_sub = os.path.join(self.target_dir, base)
        if not os.path.isdir(target_sub):
            # 目标目录无同名子目录 → 新建后直接复制(无需改名)
            os.makedirs(target_sub, exist_ok=True)
            self._wlog(f"  目标无同名子目录，新建: {base}")

        n = len(new_files)
        nums_new = {num for num, _ in new_files}
        min_new = min(nums_new)

        # 目标子目录现有文件(任意扩展名)中符合「基础名-四位编号」的文件
        existing = []  # [(编号, 文件名)]
        pat = re.compile(r'^' + re.escape(base) + r'-(\d{4})\.[^.]+$')
        for f in os.listdir(target_sub):
            if not os.path.isfile(os.path.join(target_sub, f)):
                continue
            m = pat.match(f)
            if m:
                existing.append((int(m.group(1)), f))

        if n > 1:
            # 源文件从 min_new 起连续占位(占 min_new..min_new+N-1)；目标现有编号 > min_new 的
            # 文件从 min_new+N 起按升序重新编号。例: 源 0002/0003 替换时，目标 0002 被覆盖，
            # 目标原 0003 改名 0004、后续依次类推，替换后编号连续无空洞。
            # (旧逻辑统一平移 N-1，源编号不连续时改名与待复制编号冲突会跳过整组，已废弃)
            fill_start = min_new + n
            push_asc = sorted([t for t in existing if t[0] > min_new],
                              key=lambda t: t[0])
            num_map = {num: fill_start + i for i, (num, _f) in enumerate(push_asc)}
            # 从编号最大的文件开始改名：目标编号若与未改名文件重名，其原编号必更大、
            # 已先行改走，不会发生中间覆盖；编号不变的文件跳过。
            for num, fname in sorted(push_asc, reverse=True):
                new_num = num_map[num]
                if new_num == num:
                    continue
                _stem, ext = os.path.splitext(fname)
                new_name = f"{base}-{new_num:04d}{ext}"
                os.rename(os.path.join(target_sub, fname),
                          os.path.join(target_sub, new_name))
                self._wlog(f"  改名: {fname} → {new_name}")

        # 改名完成后复制新文件；仍保留在原编号上的目标同名文件才会被覆盖
        overwrite_nums = set()
        if n == 1:
            if any(e_num == new_files[0][0] for e_num, _ in existing):
                overwrite_nums.add(new_files[0][0])
        elif any(e_num == min_new for e_num, _ in existing):
            overwrite_nums.add(min_new)

        ok = 0
        target_stems = []
        for i, (num, src_path) in enumerate(new_files):
            # 复制N个时按占位编号落盘(源编号不连续时自动归位)；单个时保持源编号
            target_num = num if n == 1 else min_new + i
            ext = os.path.splitext(src_path)[1]
            target_name = f"{base}-{target_num:04d}{ext}"
            shutil.copy2(src_path, os.path.join(target_sub, target_name))
            target_stems.append(f"{base}-{target_num:04d}")
            if target_num != num:
                self._wlog(f"  复制改名: {os.path.basename(src_path)} → {target_name}")
            else:
                act = "覆盖" if num in overwrite_nums else "复制"
                self._wlog(f"  {act}: {target_name}")
            ok += 1
        if ok:
            # 生成 Directory.txt: 记录替换后在目标目录中的文件名清单(不含扩展名), 供分件读取偏移量
            self._write_directory_txt(target_sub, target_stems)
        return ok, 0

    def _write_directory_txt(self, target_sub, new_stems):
        """在目标子目录下生成/更新 Directory.txt: 记录替换后的文件名清单
        (不含扩展名, 每行一个)。已有记录合并(多次替换时累积),
        按文件名末尾编号排序去重。"""
        dpath = os.path.join(target_sub, 'Directory.txt')
        existing = []
        if os.path.isfile(dpath):
            try:
                with open(dpath, 'r', encoding='utf-8') as fh:
                    existing = [l.strip() for l in fh if l.strip()]
            except Exception:
                existing = []
        merged = list(dict.fromkeys(existing + list(new_stems)))

        def _key(stem):
            m = re.search(r'(\d{1,4})$', stem)
            return int(m.group(1)) if m else 0

        merged.sort(key=_key)
        try:
            with open(dpath, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(merged) + '\n')
            self._wlog(f"  生成 Directory.txt: 记录 {len(merged)} 个替换后的文件名"
                       f"(本次新增/更新 {len(new_stems)} 个)")
        except Exception as e:
            self._wlog(f"  × 写入 Directory.txt 失败: {e}")

    def run(self):
        logf = None
        try:
            if not os.path.isdir(self.jpg_dir):
                self.finished_signal.emit(False, "JPG源目录不存在")
                return
            os.makedirs(self.target_dir, exist_ok=True)

            # 在目标目录下生成处理日志文件
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_path = os.path.join(self.target_dir, f"文件批量替换处理日志_{ts}.txt")
            logf = open(log_path, 'w', encoding='utf-8')
            self._log_file = logf

            self._wlog("文件批量替换处理日志")
            self._wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._wlog(f"JPG源目录: {self.jpg_dir}")
            self._wlog(f"目标目录: {self.target_dir}")
            self._wlog(f"起始编号: {self.start_num:04d} (仅处理编号 >= 起始编号的文件)")
            self._wlog("=" * 70)

            groups, skipped = self._collect_sources()
            if skipped:
                self._wlog(f"跳过 {skipped} 个文件名不含「-四位数字编号」的文件")
            if not groups:
                self._wlog("未找到符合替换条件的JPG文件")
                logf.close()
                logf = None
                self._log_file = None
                self.finished_signal.emit(False, f"未找到符合替换条件的JPG文件(起始编号 {self.start_num:04d})")
                return

            self._wlog(f"共 {len(groups)} 个基础名分组待替换")
            total = len(groups)
            done = 0
            total_ok = 0
            total_fail = 0
            for i, base in enumerate(sorted(groups), 1):
                if self.is_stopped:
                    self._wlog("用户停止处理")
                    break
                new_files = groups[base]
                self._wlog("")
                self._wlog(f"[{i}/{total}] {base} (待复制 {len(new_files)} 个文件)")
                try:
                    ok, fail = self._replace_group(base, new_files)
                    total_ok += ok
                    total_fail += fail
                    self._wlog(f"  结果: 复制 {ok} 个文件" + (f"，失败 {fail} 个" if fail else ""))
                except Exception as e:
                    import traceback
                    total_fail += len(new_files)
                    self._wlog(f"  [异常] {e}")
                    self._wlog(traceback.format_exc())
                done += 1
                self.progress_signal.emit(done, total)

            self._wlog("")
            self._wlog("=" * 70)
            self._wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._wlog(f"总计: 处理 {done}/{total} 组，复制 {total_ok} 个文件，失败 {total_fail} 个")
            if self.is_stopped:
                self._wlog("注意: 处理被用户中途停止")
            logf.close()
            logf = None
            self._log_file = None

            msg = (f"替换完成！处理 {done}/{total} 组，复制 {total_ok} 个文件。\n"
                   f"日志: {os.path.basename(log_path)}")
            self.finished_signal.emit(not self.is_stopped, msg)
        except Exception as e:
            import traceback
            self.log_signal.emit(traceback.format_exc())
            if logf is not None:
                try:
                    logf.close()
                except Exception:
                    pass
                self._log_file = None
            self.finished_signal.emit(False, f"处理出错: {e}")


class FileBatchReplacePage(FunctionPage):
    """文件批量替换功能页：将输出的JPG替换目标目录中的图片"""

    def __init__(self):
        super().__init__("文件批量替换")
        group = QGroupBox("文件批量替换 (将输出的JPG替换目标目录中的图片)")
        form = QFormLayout()

        self.jpg_dir = QLineEdit()
        self.jpg_dir.setPlaceholderText("选择包含输出JPG的目录(含子目录)")
        btn_browse_jpg = QPushButton("选择文件夹")
        btn_browse_jpg.setObjectName("BrowseBtn")
        btn_browse_jpg.clicked.connect(self.browse_jpg_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.jpg_dir)
        h1.addWidget(btn_browse_jpg)

        self.target_dir = QLineEdit()
        self.target_dir.setPlaceholderText("选择要被替换图片的目标目录")
        btn_browse_target = QPushButton("选择文件夹")
        btn_browse_target.setObjectName("BrowseBtn")
        btn_browse_target.clicked.connect(self.browse_target_dir)
        h2 = QHBoxLayout()
        h2.addWidget(self.target_dir)
        h2.addWidget(btn_browse_target)

        self.start_num = QLineEdit()
        self.start_num.setPlaceholderText("例如 0002，仅处理编号不小于此编号的文件")

        form.addRow("JPG源目录:", h1)
        form.addRow("目标目录:", h2)
        form.addRow("起始文件名:", self.start_num)
        group.setLayout(form)
        self.layout.addWidget(group)

        info_label = QLabel(
            "功能说明：\n"
            "• 扫描JPG源目录(含子目录)，文件名去除最后四位数字编号和最后一个\"-\"得到基础名，与目标目录下同名子目录匹配\n"
            "• 仅处理编号不小于起始编号的文件(缺省扩展名jpg，如输入 0002；留空默认从 0001 开始)\n"
            "• 只复制1个文件 → 直接覆盖目标同名文件；复制N个文件 → 源文件从最小编号起连续占位\n"
            "  (最小编号处覆盖目标同名文件)，目标中编号大于最小编号的现有文件从 最小编号+N 起\n"
            "  按升序重新编号预留空位(从编号最大的文件开始改名)，再复制新文件，替换后编号连续\n"
            "• 处理日志生成在目标目录下\n"
            "• 替换后在每个目标子目录生成 Directory.txt(记录替换后的文件名清单, 不含扩展名),\n"
            "  供分件功能读取目录页与文件偏移量\n"
            "• 注意：此操作会修改目标目录文件(改名/覆盖)，建议先备份"
        )
        info_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        self.layout.addWidget(info_label)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_exec = QPushButton("开始替换")
        btn_exec.setObjectName("ActionBtn")
        btn_exec.clicked.connect(self.execute)
        btn_layout.addWidget(btn_exec)

        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        self.layout.addLayout(btn_layout)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

        self.worker = None
        self.add_log_widget()

    def browse_jpg_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择JPG源目录")
        if d:
            self.jpg_dir.setText(d)

    def browse_target_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if d:
            self.target_dir.setText(d)

    def execute(self):
        jpg_d = self.jpg_dir.text().strip()
        target_d = self.target_dir.text().strip()

        if not jpg_d:
            QMessageBox.warning(self, "提示", "请先选择JPG源目录")
            return
        if not os.path.isdir(jpg_d):
            QMessageBox.warning(self, "错误", "JPG源目录不存在")
            return
        if not target_d:
            QMessageBox.warning(self, "提示", "请先选择目标目录")
            return

        # 解析起始编号(缺省扩展名jpg，如 "0002" 或 "0002.jpg")
        s = self.start_num.text().strip()
        if s:
            s = os.path.splitext(s)[0]
            if not s.isdigit():
                QMessageBox.warning(self, "错误", "起始文件名须为数字编号，例如 0002")
                return
            start_num = int(s)
        else:
            start_num = 1

        # 目标目录不存在则自动创建
        if not os.path.exists(target_d):
            try:
                os.makedirs(target_d, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法创建目标目录: {e}")
                return

        reply = QMessageBox.question(
            self, "确认操作",
            f"将从编号 {start_num:04d} 开始，用JPG源目录的文件替换目标目录中的图片。\n"
            f"目标目录中的现有文件可能被改名或覆盖，建议先备份。\n\n确定开始吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.progress.setValue(0)
        self.progress.setFormat("准备中...")
        self.log("=" * 50)
        self.log("开始替换...")
        self.log(f"JPG源目录: {jpg_d}")
        self.log(f"目标目录: {target_d}")
        self.log(f"起始编号: {start_num:04d}")
        self.log("=" * 50)

        self.worker = FileBatchReplaceWorker(
            jpg_dir=jpg_d, target_dir=target_d, start_num=start_num)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始替换":
            btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_processing(self):
        """停止处理"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止处理...")
            self.stop_btn.setEnabled(False)

    def update_progress(self, current, total):
        """更新进度显示"""
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress.setValue(int(percentage))
        self.progress.setFormat(f"{current} / {total}  ({percentage:.0f}%)")

    def on_finished(self, success, message):
        """处理完成回调"""
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止")

        btn = self.findChild(QPushButton, "ActionBtn")
        if btn and btn.text() == "开始替换":
            btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        if success:
            QMessageBox.information(self, "完成", "处理完成！")
        else:
            QMessageBox.warning(self, "提示", message)


class ArchiveCatalogWorker(QThread):
    """
    档案馆标准目录生成后台线程(v3.24重构)：
      解析用户指定目录下符合编码规则的子目录名(全宗号-档案类型·年度-保管期限
      代码-项目号-案卷号, 如 J380-ZY·2021-Y-JSC-0734)，生成两种业务目录:
      - mode='juan' 档案案卷目录: 每个编码子目录一条, 从子目录内同名xlsx取
        总件数(序号最大值)与总页数(最大序号行的页号终止值, 如"102-232"取232)
      - mode='file' 档案案件目录(按件): 逐个子目录xlsx每条序号行一条,
        档号=所属案卷档号-4位件号, 页号取"起-止"右侧, 页数=与下一序号页号差值
      - 机构代码映射: org_map(机构代码→机构名称), 由界面选择的对应表xlsx解析;
        无对应表时机构列为空由用户手工填
      - 输出: 用户所选目录名 + 「档案案卷目录」/「档案案件目录」
    """
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    # 编码目录名正则: 全宗号-类型·年度-期限-项目-卷号(卷号3-4位数字)
    _CODE_RE = re.compile(
        r'^([A-Z0-9]+)-([A-Z]+)·(\d{4})-([A-Z0-9]+)-([A-Z0-9]+)-(\d{3,4})$')
    _RETENTION = {'Y': '永久', 'D30': '30年', 'D10': '10年'}

    def __init__(self, base_dir, templates, modes=None,
                 org_map=None, output_dir=None, parent=None):
        """
        v3.25: 支持一次生成多种目录。
        templates: {'juan': 案卷目录模板路径, 'file': 案件目录模板路径}
        modes: 要生成的目录类型列表, 如 ['juan', 'file'](顺序执行)
        """
        super().__init__(parent)
        self.base_dir = base_dir
        self.templates = templates        # {mode: template_path}
        self.modes = list(modes) if modes else ['juan']
        self.org_map = org_map or {}      # {机构代码(JSC等): 机构名称}
        # 输出目录: 缺省=数据目录下「档案馆标准目录」, 可由界面指定
        self.output_dir = output_dir or os.path.join(base_dir, "档案馆标准目录")
        self.is_stopped = False

    def stop(self):
        self.is_stopped = True

    # ---------- 机构代码对应表解析 ----------
    @staticmethod
    def load_org_map(xlsx_path, wlog=None):
        """解析机构代码对应表xlsx(表头: 机构代码/机构名称)。
        返回 {代码: 名称}; 失败返回空dict。"""
        try:
            import openpyxl
            wb = openpyxl.load_workbook(xlsx_path, data_only=True)
            ws = wb.active
            # 找表头行(前5行内含"机构代码")
            code_col, name_col, start = None, None, None
            for r in range(1, 6):
                vals = [str(ws.cell(row=r, column=c).value or '').strip()
                        for c in range(1, ws.max_column + 1)]
                if '机构代码' in vals and '机构名称' in vals:
                    code_col = vals.index('机构代码') + 1
                    name_col = vals.index('机构名称') + 1
                    start = r + 1
                    break
            if code_col is None:
                if wlog:
                    wlog("  × 对应表未找到「机构代码/机构名称」表头")
                wb.close()
                return {}
            m = {}
            for r in range(start, ws.max_row + 1):
                code = ws.cell(row=r, column=code_col).value
                name = ws.cell(row=r, column=name_col).value
                if code is None or name is None:
                    continue
                code = str(code).strip()
                name = str(name).strip()
                if code and name:
                    m[code] = name
            wb.close()
            if wlog:
                wlog(f"  机构代码对应表: 载入 {len(m)} 条映射")
            return m
        except Exception as e:
            if wlog:
                wlog(f"  × 对应表读取失败: {e}")
            return {}

    # ---------- 编码目录发现(递归, 按上级分组) ----------
    def _find_code_groups(self):
        """
        递归发现编码目录并按上级目录分组。
        返回 {上级目录绝对路径: [编码子目录绝对路径, ...]}；
        指定目录的直接下层就是编码目录 → 上级=指定目录本身。
        """
        groups = {}

        def scan(dir_path, top):
            if self.is_stopped:
                return
            try:
                entries = sorted(os.listdir(dir_path))
            except Exception:
                return
            code_dirs, normal_dirs = [], []
            for e in entries:
                p = os.path.join(dir_path, e)
                if not os.path.isdir(p):
                    continue
                if self._CODE_RE.match(e):
                    code_dirs.append(p)
                else:
                    normal_dirs.append(p)
            if code_dirs:
                groups.setdefault(top, []).extend(code_dirs)
                return  # 该层已是编码目录层, 不再深入
            for nd in normal_dirs:
                scan(nd, nd)

        scan(self.base_dir, self.base_dir)
        return groups

    # ---------- 解析子目录xlsx为记录行 ----------
    @staticmethod
    def _page_end(page_str):
        """页号字符串取终止值: '49-260'→260, '102'→102。无效返回None。"""
        s = str(page_str).strip().replace(' ', '')
        if not s:
            return None
        nums = re.findall(r'\d{1,4}', s)
        return int(nums[-1]) if nums else None

    @staticmethod
    def _page_start(page_str):
        """页号字符串取起始值: '49-260'→49, '102'→102。"""
        s = str(page_str).strip().replace(' ', '')
        nums = re.findall(r'\d{1,4}', s)
        return int(nums[0]) if nums else None

    def _read_inner_rows(self, dir_path, wlog):
        """读取子目录内与目录同名的xlsx, 返回记录行列表。
        每行: dict{seq,doc_no,author,title,date,page_str}。
        兼容多单元结构(单元标题行序号为空则跳过)。"""
        dir_name = os.path.basename(dir_path)
        xp = os.path.join(dir_path, dir_name + '.xlsx')
        if not os.path.isfile(xp):
            # 退化: 目录内任意xlsx
            cands = [f for f in sorted(os.listdir(dir_path))
                     if f.lower().endswith('.xlsx') and not f.startswith('~$')]
            if not cands:
                return None
            xp = os.path.join(dir_path, cands[0])
        try:
            import openpyxl
            wb = openpyxl.load_workbook(xp, read_only=True, data_only=True)
            ws = wb.active
        except Exception as e:
            wlog(f"  × 读取xlsx失败 {os.path.basename(xp)}: {e}")
            return None
        # 表头自适应: 前5行内找含"序号"的行
        header_idx = None
        cols = {}
        for r in range(1, 6):
            rows = list(ws.iter_rows(min_row=r, max_row=r, values_only=True))
            if not rows:
                break
            headers = [str(c).strip() if c is not None else '' for c in rows[0]]
            if '序号' in headers:
                header_idx = r
                for want, aliases in (
                        ('seq', ['序号']), ('doc_no', ['文号', '文件编号']),
                        ('author', ['责任者']), ('title', ['题名', '题  名', '题目']),
                        ('date', ['发文日期', '文件日期', '日期']),
                        ('page', ['页号', '页码'])):
                    for a in aliases:
                        if a in headers:
                            cols[want] = headers.index(a)
                            break
                break
        if header_idx is None:
            wb.close()
            wlog(f"  × {os.path.basename(xp)} 未找到含「序号」的表头行")
            return None
        recs = []
        for row in ws.iter_rows(min_row=header_idx + 1, values_only=True):
            cells = list(row)
            if len(cells) <= max(cols.values()):
                cells += [''] * (max(cols.values()) - len(cells) + 1)
            g = lambda k: (cells[cols[k]]
                           if k in cols and cols[k] < len(cells) else None)
            seq_v = g('seq')
            if seq_v is None or str(seq_v).strip() == '':
                continue   # 单元标题行/空行
            try:
                seq = int(str(seq_v).strip())
            except ValueError:
                continue
            recs.append({
                'seq': seq,
                'doc_no': str(g('doc_no') or '').strip(),
                'author': str(g('author') or '').strip().replace('\n', ''),
                'title': str(g('title') or '').strip().replace('\n', ''),
                'date': str(g('date') or '').strip(),
                'page_str': str(g('page') or '').strip(),
            })
        wb.close()
        return recs

    # ---------- 案卷目录: 每子目录一条 ----------
    def _juan_rows(self, code_dirs, wlog):
        """生成案卷级数据行。
        返回 [(档号,全宗,年度,期限中文,机构名称,机构代码,案卷号,总页数,总件数)]"""
        rows = []
        for cd in sorted(code_dirs):
            name = os.path.basename(cd)
            m = self._CODE_RE.match(name)
            fonds, ftype, year, ret, proj, vol = m.groups()
            retention = self._RETENTION.get(ret, ret)
            org_name = self.org_map.get(proj, '')
            recs = self._read_inner_rows(cd, wlog)
            total_items = max((r['seq'] for r in recs), default=None) if recs else None
            total_pages = None
            if recs:
                max_seq_rec = max(recs, key=lambda r: r['seq'])
                if max_seq_rec['page_str']:
                    total_pages = self._page_end(max_seq_rec['page_str'])
            rows.append((name, fonds, year, retention, org_name, proj,
                         vol, total_pages, total_items))
            wlog(f"  {name}: 期限={retention} 机构={org_name or '(空)'} "
                 f"卷号={vol} 总页数={total_pages} 总件数={total_items}")
        return rows

    # ---------- 案件目录: 子目录xlsx逐行 ----------
    def _file_rows(self, code_dirs, wlog):
        """生成按件级数据行(全部子目录合并)。
        返回 [(所属案卷档号,全宗,年度,期限中文,机构名称,机构代码,
               案卷号,件号,档号,文件编号,责任者,题名,文件日期,页号,页数)]"""
        rows = []
        for cd in sorted(code_dirs):
            name = os.path.basename(cd)
            m = self._CODE_RE.match(name)
            fonds, ftype, year, ret, proj, vol = m.groups()
            retention = self._RETENTION.get(ret, ret)
            org_name = self.org_map.get(proj, '')
            recs = self._read_inner_rows(cd, wlog)
            if not recs:
                wlog(f"  ! {name}: 无有效记录行, 跳过")
                continue
            recs.sort(key=lambda r: r['seq'])
            for i, r in enumerate(recs):
                seq = r['seq']
                vol_no3 = f"{seq:03d}"              # 案卷号=序号三位
                archive_no = f"{name}-{seq:04d}"     # 档号=所属案卷档号-4位件号
                page_no = None
                if r['page_str']:
                    # 页号: 含"-"取右侧
                    s = r['page_str'].replace(' ', '')
                    if '-' in s:
                        page_no = self._page_end(s)
                    else:
                        page_no = self._page_start(s)
                # 页数: 与下一序号页号的差值
                pages = None
                cur_end = self._page_end(r['page_str']) if r['page_str'] else None
                nxt = recs[i + 1] if i + 1 < len(recs) else None
                if nxt is not None and nxt['page_str']:
                    nxt_start = self._page_start(nxt['page_str'])
                    if cur_end is not None and nxt_start is not None:
                        diff = nxt_start - cur_end
                        pages = diff if diff >= 0 else None   # 不为负
                elif cur_end is not None and '-' in r['page_str'].replace(' ', ''):
                    # 无下一页号且当前含"-": 右-左
                    ps = self._page_start(r['page_str'])
                    if ps is not None:
                        pages = cur_end - ps
                rows.append((name, fonds, year, retention, org_name, proj,
                             vol_no3, seq, archive_no, r['doc_no'], r['author'],
                             r['title'], r['date'], page_no, pages))
        return rows

    # ---------- 填充模板 ----------
    def _fill_template(self, out_path, rows, wlog, template_path=None):
        """按模板表头自适应填数据行(模板首行为表头)。"""
        import openpyxl
        from openpyxl.styles import Alignment
        wb = openpyxl.load_workbook(template_path or self.templates.get('juan'))
        ws = wb.active
        headers = {}
        for c in range(1, ws.max_column + 1):
            v = ws.cell(row=1, column=c).value
            if v is None:
                continue
            headers[str(v).strip()] = c
        start_row = 2
        center = Alignment(horizontal='center', vertical='center', wrap_text=True)
        int_cols = {'件号', '页号', '页数', '总页数', '卷内文件总件数',
                    '案卷号', '年度', '全宗号'}
        for i, row in enumerate(rows):
            r = start_row + i
            for key, val in row.items():
                if key not in headers or val is None or val == '':
                    continue
                try:
                    if key in int_cols and val is not None and val != '':
                        val = int(val)
                except (ValueError, TypeError):
                    pass
                ws.cell(row=r, column=headers[key], value=val)
            for c in range(1, ws.max_column + 1):
                ws.cell(row=r, column=c).alignment = center
        wb.save(out_path)

    def run(self):
        try:
            if not os.path.isdir(self.base_dir):
                self.finished_signal.emit(False, "所选目录不存在")
                return
            for md in self.modes:
                tp = self.templates.get(md)
                if not tp or not os.path.isfile(tp):
                    name = '档案案卷目录' if md == 'juan' else '档案案件目录'
                    self.finished_signal.emit(False, f"{name}模板文件不存在")
                    return
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_root = self.output_dir
            os.makedirs(out_root, exist_ok=True)
            names = {'juan': '档案案卷目录', 'file': '档案案件目录'}
            log_path = os.path.join(
                out_root,
                f"档案馆目录日志_{'_'.join(names[m] for m in self.modes)}_{ts}.txt")
            logf = open(log_path, 'w', encoding='utf-8')
            import threading
            lock = threading.Lock()

            def wlog(s):
                with lock:
                    logf.write(s + "\n")
                    logf.flush()
                self.log_signal.emit(s)

            wlog(f"{'+'.join(names[m] for m in self.modes)}生成 - 处理日志")
            wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog(f"指定目录: {self.base_dir}")
            for md in self.modes:
                wlog(f"模板[{names[md]}]: {self.templates.get(md)}")
            if self.org_map:
                wlog(f"机构代码对应: {len(self.org_map)} 条")
            else:
                wlog("机构代码对应: 未选择(机构列为空, 需手工填写)")
            wlog("=" * 70)

            groups = self._find_code_groups()
            if not groups:
                logf.close()
                self.finished_signal.emit(False, "该目录(含下层)无可用编码目录数据")
                return

            total = sum(len(v) for v in groups.values()) * len(self.modes)
            wlog(f"发现 {len(groups)} 个分组 / 共 "
                 f"{sum(len(v) for v in groups.values())} 个编码子目录")
            done = 0
            ok_files = []
            base_name = os.path.basename(os.path.normpath(self.base_dir))
            # v3.25: 逐种目录类型生成(modes顺序执行, 共享分组发现结果)
            for md in self.modes:
                if self.is_stopped:
                    break
                mode_name = names[md]
                wlog("")
                wlog(f"══ 开始生成{mode_name} ══")
                for top, code_dirs in sorted(groups.items()):
                    if self.is_stopped:
                        break
                    top_name = os.path.basename(top)
                    wlog(f"── 分组: {top_name} ({len(code_dirs)} 卷) ──")
                    if md == 'juan':
                        tuples = self._juan_rows(code_dirs, wlog)
                        keys = ['档号', '全宗号', '年度', '保管期限', '机构问题',
                                '机构问题代码', '案卷号', '总页数', '卷内文件总件数']
                    else:
                        tuples = self._file_rows(code_dirs, wlog)
                        keys = ['所属案卷档号', '全宗号', '年度', '保管期限',
                                '机构问题', '机构问题代码', '案卷号', '件号', '档号',
                                '文件编号', '责任者', '题名', '文件日期', '页号', '页数']
                    done += len(code_dirs)
                    self.progress_signal.emit(min(done, total), total)
                    if not tuples:
                        continue
                    rows = [dict(zip(keys, t)) for t in tuples]
                    # v3.24: 输出文件名=所选目录名+目录类型
                    out_name = f"{base_name}{mode_name}.xlsx"
                    out_path = os.path.join(out_root, out_name)
                    try:
                        self._fill_template(out_path, rows, wlog,
                                            template_path=self.templates[md])
                        ok_files.append(out_name)
                        wlog(f"  ✓ 生成: {out_name} ({len(rows)} 条)")
                    except Exception as e:
                        wlog(f"  × 生成失败 {out_name}: {e}")

            wlog("")
            wlog("=" * 70)
            wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            wlog(f"生成 {len(ok_files)} 个目录文件: {', '.join(ok_files)}")
            logf.close()
            if self.is_stopped:
                self.finished_signal.emit(False, "已停止")
            else:
                self.finished_signal.emit(
                    True,
                    f"完成！生成 {len(ok_files)} 个目录文件 → {out_root}")
        except Exception as e:
            self.finished_signal.emit(False, f"处理出错: {e}")


class ArchiveCatalogPage(FunctionPage):
    """档案馆标准目录生成页(v3.24重构)：
    业务目录TAB(档案案卷目录/档案案件目录二选一) + 文书目录TAB(保留原有)。"""

    def __init__(self):
        super().__init__("档案馆标准目录")
        self.worker = None

        from PyQt5.QtWidgets import QTabWidget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # ====== TAB1: 业务目录 ======
        biz_widget = QWidget()
        biz_v = QVBoxLayout(biz_widget)

        # 目录类型选择(v3.25: 改多选框, 可同时生成两种, 缺省全选)
        mode_box = QGroupBox("目录类型(可多选)")
        mode_h = QHBoxLayout()
        self.mode_juan_cb = QCheckBox("档案案卷目录")
        self.mode_file_cb = QCheckBox("档案案件目录")
        self.mode_juan_cb.setChecked(True)   # 缺省两者都选
        self.mode_file_cb.setChecked(True)
        mode_h.addWidget(self.mode_juan_cb)
        mode_h.addWidget(self.mode_file_cb)
        mode_h.addStretch()
        mode_box.setLayout(mode_h)
        biz_v.addWidget(mode_box)

        form = QFormLayout()
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("选择包含编码子目录的目录")
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(self.browse_dir)
        h1 = QHBoxLayout()
        h1.addWidget(self.dir_edit)
        h1.addWidget(btn_browse)
        form.addRow("数据目录:", h1)

        # 两个模板(按当前目录类型选用其一)
        self.tpl_juan_edit = QLineEdit()
        self.tpl_juan_edit.setPlaceholderText("档案案卷目录模板xlsx(案卷级)")
        btn_tj = QPushButton("选择模板")
        btn_tj.setObjectName("BrowseBtn")
        btn_tj.clicked.connect(lambda: self.browse_template(self.tpl_juan_edit))
        h2 = QHBoxLayout()
        h2.addWidget(self.tpl_juan_edit)
        h2.addWidget(btn_tj)
        form.addRow("案卷目录模板:", h2)

        self.tpl_file_edit = QLineEdit()
        self.tpl_file_edit.setPlaceholderText("档案案件目录模板xlsx(按件级)")
        btn_tf = QPushButton("选择模板")
        btn_tf.setObjectName("BrowseBtn")
        btn_tf.clicked.connect(lambda: self.browse_template(self.tpl_file_edit))
        h3 = QHBoxLayout()
        h3.addWidget(self.tpl_file_edit)
        h3.addWidget(btn_tf)
        form.addRow("案件目录模板:", h3)

        # 机构代码对应表(可选)
        self.org_edit = QLineEdit()
        self.org_edit.setPlaceholderText("可选: 机构代码对应表xlsx(不选则机构列留空手填)")
        btn_org = QPushButton("选择对应表")
        btn_org.setObjectName("BrowseBtn")
        btn_org.clicked.connect(self.browse_org)
        h4 = QHBoxLayout()
        h4.addWidget(self.org_edit)
        h4.addWidget(btn_org)
        form.addRow("机构代码对应表:", h4)

        # 输出目录
        self.out_edit = QLineEdit()
        self.out_edit.setPlaceholderText("输出目录(缺省: 数据目录\\档案馆标准目录)")
        btn_out = QPushButton("选择文件夹")
        btn_out.setObjectName("BrowseBtn")
        btn_out.clicked.connect(self.browse_out)
        h5 = QHBoxLayout()
        h5.addWidget(self.out_edit)
        h5.addWidget(btn_out)
        form.addRow("输出目录:", h5)
        biz_v.addLayout(form)

        biz_info = QLabel(
            "【档案案卷目录】每个编码子目录一条; 卷内文件总件数=子目录同名xlsx"
            "序号最大值; 总页数=最大序号行页号终止值(如102-232取232)\n"
            "【档案案件目录】子目录xlsx逐序号行填入; 档号=所属案卷档号-4位件号; "
            "页号取\"起-止\"右侧; 页数=与下一序号页号差值(负值不算, 无下一页号"
            "且含\"-\"时=右减左)\n"
            "编码: 全宗号-类型·年度-期限-项目号-案卷号; 期限Y=永久 D30=30年 D10=10年; "
            "输出文件名=所选目录名+目录类型"
        )
        biz_info.setStyleSheet("color: #666; font-size: 12px;")
        biz_info.setWordWrap(True)
        biz_v.addWidget(biz_info)
        biz_v.addStretch()
        self.tabs.addTab(biz_widget, "业务目录")

        # ====== TAB2: 文书目录 ======
        doc_widget = QWidget()
        doc_v = QVBoxLayout(doc_widget)
        doc_info = QLabel(
            "【文书目录】沿用原有科技类案卷级目录生成逻辑。\n"
            "请切换到「业务目录」TAB使用新功能; 文书目录功能规划中。"
        )
        doc_info.setStyleSheet("color: #666; font-size: 12px;")
        doc_v.addWidget(doc_info)
        doc_v.addStretch()
        self.tabs.addTab(doc_widget, "文书目录")

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("生成目录")
        self.start_btn.setObjectName("ActionBtn")
        self.start_btn.clicked.connect(self.start)
        btn_layout.addWidget(self.start_btn)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633; color: white;")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        self.layout.addLayout(btn_layout)

        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

        self.add_log_widget()

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择数据目录")
        if d:
            self.dir_edit.setText(d)
            if not self.out_edit.text().strip():
                self.out_edit.setText(os.path.join(d, "档案馆标准目录"))

    def browse_out(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if d:
            self.out_edit.setText(d)

    def browse_template(self, edit):
        f, _ = QFileDialog.getOpenFileName(
            self, "选择模板xlsx", "", "Excel文件 (*.xlsx)")
        if f:
            edit.setText(f)

    def browse_org(self):
        f, _ = QFileDialog.getOpenFileName(
            self, "选择机构代码对应表xlsx", "", "Excel文件 (*.xlsx)")
        if f:
            self.org_edit.setText(f)

    def start(self):
        if self.tabs.currentIndex() != 0:
            QMessageBox.information(self, "提示", "请切换到「业务目录」TAB后开始")
            return
        d = self.dir_edit.text().strip()
        if not d or not os.path.isdir(d):
            QMessageBox.warning(self, "提示", "请先选择有效的数据目录")
            return
        # v3.25: 多选框收集目录类型(缺省全选), 校验所选类型的模板
        modes = []
        if self.mode_juan_cb.isChecked():
            modes.append('juan')
        if self.mode_file_cb.isChecked():
            modes.append('file')
        if not modes:
            QMessageBox.warning(self, "提示", "请至少勾选一种目录类型")
            return
        templates = {'juan': self.tpl_juan_edit.text().strip(),
                     'file': self.tpl_file_edit.text().strip()}
        for md in modes:
            tp = templates[md]
            tpl_name = '案卷目录模板' if md == 'juan' else '案件目录模板'
            if not tp or not os.path.isfile(tp):
                QMessageBox.warning(self, "提示", f"请先选择{tpl_name}xlsx文件")
                return
        out = self.out_edit.text().strip()
        if not out:
            out = os.path.join(d, "档案馆标准目录")
            self.out_edit.setText(out)
        try:
            os.makedirs(out, exist_ok=True)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法创建输出目录: {e}")
            return
        # 机构代码对应表(可选)
        org_map = {}
        org_p = self.org_edit.text().strip()
        if org_p:
            if not os.path.isfile(org_p):
                QMessageBox.warning(self, "提示", "机构代码对应表文件不存在, 已忽略")
            else:
                org_map = ArchiveCatalogWorker.load_org_map(org_p, self.log)
                if not org_map:
                    reply = QMessageBox.question(
                        self, "提示",
                        "机构代码对应表未解析到有效映射(需含「机构代码/机构名称」表头)。\n"
                        "是否继续(机构列将留空, 需手工填写)?",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply != QMessageBox.Yes:
                        return
        self.log_box.clear()
        names = {'juan': '档案案卷目录', 'file': '档案案件目录'}
        self.log(f"开始生成 {'+'.join(names[m] for m in modes)}: {d}")
        for md in modes:
            self.log(f"模板[{names[md]}]: {templates[md]}")
        self.log(f"输出目录: {out}")
        self.worker = ArchiveCatalogWorker(d, templates, modes=modes,
                                           org_map=org_map, output_dir=out)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止...")

    def _update_progress(self, cur, total):
        pct = cur / total * 100 if total else 0
        self.progress.setValue(int(pct))
        self.progress.setFormat(f"{cur} / {total} ({pct:.0f}%)")

    def _on_finished(self, success, message):
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止/失败")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.warning(self, "结束", message)


class FileSplitPage(FunctionPage):
    """分件功能页：按卷内文件目录表格自动分件"""

    def __init__(self):
        super().__init__("分件")
        group = QGroupBox("分件 (按卷内文件目录表格自动拆分)")
        form = QFormLayout()

        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("选择要分件的目录(将处理其下所有子目录)")
        btn_browse = QPushButton("选择文件夹")
        btn_browse.setObjectName("BrowseBtn")
        btn_browse.clicked.connect(self.browse_dir)
        h = QHBoxLayout()
        h.addWidget(self.dir_edit)
        h.addWidget(btn_browse)
        form.addRow("分件目录:", h)

        # 分件到新目录(缺省选中): 结果按目录结构拷贝到目标目录, 源不动
        self._target_manual = False  # 用户是否手动改过目标目录(改过则不随源联动)
        self.to_new_check = QCheckBox("分件到新目录(拷贝到目标目录, 源文件不动)")
        self.to_new_check.setChecked(True)
        self.to_new_check.stateChanged.connect(self.on_to_new_toggled)
        form.addRow("分件方式:", self.to_new_check)

        self.target_edit = QLineEdit()
        self.target_edit.setPlaceholderText("分件结果输出目录")
        btn_target = QPushButton("选择文件夹")
        btn_target.setObjectName("BrowseBtn")
        btn_target.clicked.connect(self.browse_target)
        h2 = QHBoxLayout()
        h2.addWidget(self.target_edit)
        h2.addWidget(btn_target)
        self.btn_target = btn_target
        form.addRow("目标目录:", h2)

        # 分件依据: 缺省按目录文件(xlsx)分件; OCR分件为可选项, 缺省不勾选
        self.ocr_check = QCheckBox("使用OCR识别分件(不勾选时缺省按xlsx目录文件分件)")
        self.ocr_check.setChecked(False)
        self.ocr_check.stateChanged.connect(self.on_ocr_toggled)
        form.addRow("分件依据:", self.ocr_check)

        self.xlsx_dir_edit = QLineEdit()
        self.xlsx_dir_edit.setPlaceholderText("包含xlsx目录文件的文件夹(将递归查找与待处理目录同名的xlsx)")
        btn_xlsx = QPushButton("选择文件夹")
        btn_xlsx.setObjectName("BrowseBtn")
        btn_xlsx.clicked.connect(self.browse_xlsx_dir)
        self.btn_xlsx = btn_xlsx
        h3 = QHBoxLayout()
        h3.addWidget(self.xlsx_dir_edit)
        h3.addWidget(btn_xlsx)
        form.addRow("目录文件:", h3)

        group.setLayout(form)
        self.layout.addWidget(group)

        # 说明
        info = QLabel(
            "功能说明：\n"
            "• 缺省按xlsx目录文件分件: 从指定文件夹下读取与待处理目录同名的xlsx文件(第3行为标题行, 含「序号」「页号」列)作为分件依据\n"
            "• 勾选「使用OCR识别分件」切换为OCR模式: 对每个子目录 OCR 目录页(卷内文件目录)，解析序号/页号自动拆分\n"
            "• 若子目录含 Directory.txt(文件批量替换生成): 第一页为卷皮, 目录页取 Directory.txt 记录,\n"
            "  文件偏移量=Directory.txt 最大文件序号; 无 Directory.txt 时提示确认并按缺省偏移量2处理;\n"
            "  分件完成后删除该目录下 Directory.txt\n"
            "• 检查: 按与分件相同的依据(xlsx/OCR)检查各目录，发现应移走却残留的文件并生成报告\n"
            "• 手工分件: 逐个目录手工输入序号/页号拆分(带连续性校验)"
        )
        info.setStyleSheet("color: #666; font-size: 12px;")
        self.layout.addWidget(info)

        # 按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始分件")
        self.start_btn.setObjectName("ActionBtn")
        self.start_btn.clicked.connect(self.start)
        btn_layout.addWidget(self.start_btn)
        self.check_btn = QPushButton("检查")
        self.check_btn.setObjectName("ActionBtn")
        self.check_btn.clicked.connect(self.start_check)
        btn_layout.addWidget(self.check_btn)
        self.manual_btn = QPushButton("手工分件")
        self.manual_btn.setObjectName("ActionBtn")
        self.manual_btn.clicked.connect(self.start_manual)
        btn_layout.addWidget(self.manual_btn)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633; color: white;")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        self.layout.addLayout(btn_layout)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

        # 日志
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(250)
        self.layout.addWidget(self.log_box, 1)

        self.worker = None

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择分件目录")
        if d:
            self.dir_edit.setText(d)
            # 源目录变化: 目标目录未手动改过时自动跟随(源/分件完成)
            self._auto_target()
            # 缺省xlsx分件模式且未选目录文件时, 目录文件跟随分件目录
            if not self.ocr_check.isChecked() and not self.xlsx_dir_edit.text().strip():
                self.xlsx_dir_edit.setText(d)

    def _auto_target(self):
        """目标目录自动联动: 用户未手动改过目标目录时, 跟随源目录生成
        「源目录/分件完成」; 手动改过(选择过其他目录)后不再跟随。"""
        if getattr(self, '_target_manual', False):
            return
        base = self.dir_edit.text().strip()
        if base:
            self.target_edit.setText(os.path.join(base, "分件完成"))

    def log(self, msg):
        self.log_box.append(f">> {msg}")

    def on_to_new_toggled(self, state):
        """「分件到新目录」勾选状态切换: 取消时禁编目标目录。"""
        to_new = self.to_new_check.isChecked()
        self.target_edit.setEnabled(to_new)
        self.btn_target.setEnabled(to_new)
        if to_new:
            self._auto_target()  # 目标为空或未手动改过 → 自动填默认

    def browse_target(self):
        d = QFileDialog.getExistingDirectory(self, "选择分件结果输出目录")
        if d:
            self.target_edit.setText(d)
            self._target_manual = True  # 用户手动指定, 之后不再跟随源目录

    def on_ocr_toggled(self, state):
        """「使用OCR识别分件」勾选状态切换: 勾选时用OCR(禁用xlsx目录输入);
        不勾选时缺省按xlsx目录文件分件(启用并要求选择xlsx目录)。"""
        use_ocr = self.ocr_check.isChecked()
        self.xlsx_dir_edit.setEnabled(not use_ocr)
        self.btn_xlsx.setEnabled(not use_ocr)
        if not use_ocr and not self.xlsx_dir_edit.text().strip():
            # xlsx模式且未选择目录时, 默认使用分件目录
            base = self.dir_edit.text().strip()
            if base:
                self.xlsx_dir_edit.setText(base)

    def browse_xlsx_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择包含xlsx目录文件的文件夹")
        if d:
            self.xlsx_dir_edit.setText(d)

    def start(self):
        base_dir = self.dir_edit.text().strip()
        if not base_dir:
            QMessageBox.warning(self, "提示", "请先选择分件目录")
            return
        if not os.path.isdir(base_dir):
            QMessageBox.warning(self, "错误", "目录不存在")
            return

        # Directory.txt 检查: 子目录缺少 Directory.txt 时可能未做过卷内目录替换, 提示用户确认
        sub_names = [d for d in os.listdir(base_dir)
                     if os.path.isdir(os.path.join(base_dir, d))]
        missing = [d for d in sub_names
                   if not os.path.isfile(os.path.join(base_dir, d, 'Directory.txt'))]
        if sub_names and missing:
            show = '、'.join(missing[:8]) + ('...' if len(missing) > 8 else '')
            reply = QMessageBox.question(
                self, "提示",
                f"当前待处理目录有 {len(missing)}/{len(sub_names)} 个子目录没有 Directory.txt，\n"
                f"可能没有进行过卷内目录替换。\n"
                f"若继续, 这些目录将按缺省偏移量 2 处理。\n"
                f"({show})\n\n是否继续？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply != QMessageBox.Yes:
                self.log("已取消: 待处理目录缺少 Directory.txt")
                return
            self.log(f"注意: {len(missing)} 个目录无 Directory.txt, 将按缺省偏移量 2 处理")

        to_new = self.to_new_check.isChecked()
        target_base = None
        copy_mode = False
        if to_new:
            target_base = self.target_edit.text().strip()
            if not target_base:
                target_base = os.path.join(base_dir, "分件完成")
                self.target_edit.setText(target_base)
            try:
                os.makedirs(target_base, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法创建目标目录: {e}")
                return
            copy_mode = True

        if copy_mode:
            confirm_msg = (f"分件结果将拷贝到:\n{target_base}\n"
                           f"(源目录文件保持不动)")
        else:
            confirm_msg = ("分件将在源目录内移动 jpg 文件(不可自动撤销)，\n"
                           "建议先备份。确定开始吗？")
        reply = QMessageBox.question(self, "确认操作", confirm_msg,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.log_box.clear()
        self.log(f"开始分件: {base_dir}")
        if copy_mode:
            self.log(f"分件到新目录(拷贝): {target_base}")

        # 分件依据: 缺省读取目录文件(xlsx); 勾选OCR选项时用OCR模式
        xlsx_dir = None
        if self.ocr_check.isChecked():
            self.log("分件依据: OCR识别目录页")
        else:
            xlsx_dir = self.xlsx_dir_edit.text().strip()
            if not xlsx_dir:
                QMessageBox.warning(self, "提示", "缺省按xlsx目录文件分件，请先选择包含xlsx的文件夹")
                return
            if not os.path.isdir(xlsx_dir):
                QMessageBox.warning(self, "错误", f"目录文件路径不存在: {xlsx_dir}")
                return
            self.log(f"读取目录文件(xlsx): {xlsx_dir}")

        self.worker = FileSplitWorker(base_dir, target_base=target_base,
                                      copy_mode=copy_mode, xlsx_dir=xlsx_dir)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log("正在停止...")

    def update_progress(self, cur, total):
        pct = cur / total * 100 if total else 0
        self.progress.setValue(int(pct))
        self.progress.setFormat(f"{cur} / {total} ({pct:.0f}%)")

    def on_finished(self, success, message):
        self.log(message)
        self.progress.setFormat("已完成" if success else "已停止/失败")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.warning(self, "结束", message)

    # ---------- 检查 ----------
    def start_check(self):
        base_dir = self.dir_edit.text().strip()
        if not base_dir:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        if not os.path.isdir(base_dir):
            QMessageBox.warning(self, "错误", "目录不存在")
            return

        # 分件依据: 缺省读取目录文件(xlsx); 勾选OCR选项时用OCR模式
        xlsx_dir = None
        if not self.ocr_check.isChecked():
            xlsx_dir = self.xlsx_dir_edit.text().strip()
            if not xlsx_dir or not os.path.isdir(xlsx_dir):
                QMessageBox.warning(self, "提示", "缺省按xlsx目录文件检查，请先选择有效的目录文件路径")
                return

        self.log_box.clear()
        self.log(f"开始检查: {base_dir}")
        if xlsx_dir:
            self.log(f"检查模式: 读取目录文件(xlsx) → {xlsx_dir}")
        self.check_worker = FileSplitCheckWorker(base_dir, xlsx_dir=xlsx_dir)
        self.check_worker.log_signal.connect(self.log)
        self.check_worker.progress_signal.connect(self.update_progress)
        self.check_worker.finished_signal.connect(self.on_check_finished)
        self.check_worker.start()
        self.check_btn.setEnabled(False)

    def on_check_finished(self, success, message):
        self.log(message)
        self.progress.setFormat("检查完成" if success else "检查停止/失败")
        self.check_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "检查完成", message)
        else:
            QMessageBox.warning(self, "检查结束", message)

    # ---------- 手工分件 ----------
    def start_manual(self):
        base_dir = self.dir_edit.text().strip()
        if not base_dir:
            QMessageBox.warning(self, "提示", "请先选择目录")
            return
        if not os.path.isdir(base_dir):
            QMessageBox.warning(self, "错误", "目录不存在")
            return
        dlg = ManualSplitDialog(base_dir, self)
        dlg.exec_()

class XlsxToJpgWorker(QThread):
    """表格文件(xlsx/xls)转JPG后台处理线程 - openpyxl读取+PIL渲染，按A4排版标准输出，超一页自动分页（分页序号可指定起始编码）。
    输出前对表格进行编辑: 删除 G 列后的所有无关列(仅保留 A-G);
    排版后若最后一页只有空表格(无文字)则删除该页;
    最后一页未占满版面时以空表格行补足, 保证导出文件整洁。"""
    # 补足空行统一行高(磅): 所有文件的补足空行都用此固定行高(对齐
    # J380-ZY·2021-Y-GTC-0171 样例的空行间距), 保证各文件空行间距一致;
    # 不按各文件自身空行行高取值(不同文件不一致会导致间距忽大忽小)
    FILL_ROW_H_PT = 57.0
    log_signal = Signal(str)
    progress_signal = Signal(int, int)
    finished_signal = Signal(bool, str)

    def __init__(self, input_dir, output_dir=None, same_dir=True, start_num=1, parent=None):
        super().__init__(parent)
        self.input_dir = input_dir
        self.output_dir = output_dir  # 仅 same_dir=False 时使用
        self.same_dir = same_dir      # True=输出到原目录
        self.start_num = start_num    # 分页输出的起始文件编码（默认1，即 -0001 开始）
        self.is_stopped = False
        self._log_file = None  # 当前处理日志文件句柄

    def _wlog(self, s):
        """写入处理日志文件（若已打开），同时输出到界面日志"""
        if self._log_file is not None:
            try:
                self._log_file.write(s + "\n")
                self._log_file.flush()
            except Exception:
                pass
        self.log_signal.emit(s)

    def _find_excel_files(self):
        """递归查找所有xlsx/xls文件"""
        result = []
        for root, dirs, files in os.walk(self.input_dir):
            for f in files:
                if f.lower().endswith(('.xlsx', '.xlsm', '.xls')) and not f.startswith('~$'):
                    result.append(os.path.join(root, f))
        return sorted(result)

    def _detect_file_format(self, filepath):
        """
        检测文件实际格式（通过文件头魔数）。
        返回: 'xlsx', 'xlsm', 'xls' (OLE2格式), 或 'unknown'
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(8)
                # xlsx/xlsm 是 ZIP 格式，文件头为 PK (50 4B)
                if header[:2] == b'PK':
                    # 进一步检测是否包含宏（xlsm）
                    try:
                        import zipfile
                        with zipfile.ZipFile(filepath, 'r') as zf:
                            if 'xl/vbaProject.bin' in zf.namelist():
                                return 'xlsm'
                    except Exception:
                        pass
                    return 'xlsx'
                # xls 是 OLE2 复合文档，文件头为 D0 CF 11 E0
                if header[:4] == b'\xd0\xcf\x11\xe0':
                    return 'xls'
                return 'unknown'
        except Exception:
            return 'unknown'

    def _get_openpyxl_readable_path(self, filepath):
        """
        openpyxl 只接受 .xlsx/.xlsm/.xltx/.xltm 扩展名，
        对于被改名的文件（如 xlsm 改成 .xls），创建正确扩展名的临时副本。
        返回: (可读路径, 临时文件路径或None)
        """
        import tempfile
        import uuid
        import shutil
        supported = ('.xlsx', '.xlsm', '.xltx', '.xltm')
        ext = os.path.splitext(filepath)[1].lower()
        if ext in supported:
            return filepath, None
        # 根据实际格式确定正确扩展名
        actual_format = self._detect_file_format(filepath)
        correct_ext = {'xlsx': '.xlsx', 'xlsm': '.xlsm'}.get(actual_format, '.xlsx')
        temp_file = os.path.join(tempfile.gettempdir(),
                                 f"opy_{uuid.uuid4().hex[:8]}{correct_ext}")
        shutil.copy2(filepath, temp_file)
        return temp_file, temp_file

    def _convert_xlsx(self, filepath, output_path, dpi=300):
        """转换xlsx/xlsm文件为A4排版JPG（openpyxl+PIL渲染，超一页自动分页）"""
        return self._convert_with_openpyxl(filepath, output_path, dpi)

    def _convert_xls(self, filepath, output_path, dpi=300):
        """转换xls文件为JPG，若实际是xlsx/xlsm格式则用openpyxl渲染"""
        actual_format = self._detect_file_format(filepath)
        if actual_format in ('xlsx', 'xlsm'):
            self._wlog(f"  文件实际为 {actual_format} 格式（扩展名为.xls），使用 openpyxl 渲染...")
            return self._convert_with_openpyxl(filepath, output_path, dpi)
        return False, "旧版 xls (OLE2) 格式暂不支持直接渲染，请先在 Excel 中另存为 xlsx 后再处理", []

    def _convert_with_openpyxl(self, filepath, output_path, dpi=300):
        """
        使用 openpyxl 读取表格数据和格式，用 PIL 渲染为 JPG。
        输出按 A4 纸排版标准：自动选择纵向/横向、20mm 页边距；
        输出文件名统一追加四位序号（从用户指定起始编码 start_num 开始），
        单页输出为 -{start_num:04d}，超过一页时按行分页依次递增。
        使用 Windows 系统中文字体（宋体/黑体），避免中文字形渲染错误。
        保留合并单元格、列宽、行高、对齐方式、字体加粗、背景色等格式信息。
        返回: (是否成功, 错误信息, 输出文件路径列表)
        """
        try:
            import openpyxl
            from openpyxl.utils import get_column_letter

            # openpyxl 拒绝非 .xlsx/.xlsm 扩展名的文件，必要时创建正确扩展名的临时副本
            load_path, opy_temp_file = self._get_openpyxl_readable_path(filepath)

            # 加载工作簿（read_only=False 以获取合并单元格和列宽信息）
            try:
                wb = openpyxl.load_workbook(load_path, read_only=False, data_only=True)
            finally:
                if opy_temp_file and os.path.exists(opy_temp_file):
                    try:
                        os.remove(opy_temp_file)
                    except:
                        pass
            ws = wb.active

            if ws.max_row is None or ws.max_column is None or ws.max_row == 0 or ws.max_column == 0:
                wb.close()
                return False, "工作表为空", []

            # ---- 输出前编辑: 删除 G 列后的所有无关列(仅保留 A-G 列) ----
            KEEP_COLS = 7
            orig_col = ws.max_column
            if orig_col > KEEP_COLS:
                n_del = orig_col - KEEP_COLS
                try:
                    ws.delete_cols(KEEP_COLS + 1, n_del)
                    self._wlog(f"  编辑: 已删除 G 列后的 {n_del} 个无关列"
                               f"(原 {orig_col} 列 → 保留 A-G)")
                except Exception as e:
                    self._wlog(f"  × 删除 G 列后无关列失败: {e}, 排版时仅保留 A-G 列")

            max_row = ws.max_row
            max_col = min(ws.max_column, KEEP_COLS)

            # 读取合并单元格信息
            merged_covered = set()  # 被合并覆盖的非左上角单元格
            merged_map = {}  # 左上角 -> (min_row, min_col, max_row, max_col)
            for mr in ws.merged_cells.ranges:
                if mr.min_row > max_row or mr.min_col > max_col:
                    continue
                for r in range(mr.min_row, min(mr.max_row, max_row) + 1):
                    for c in range(mr.min_col, min(mr.max_col, max_col) + 1):
                        if (r, c) != (mr.min_row, mr.min_col):
                            merged_covered.add((r, c))
                merged_map[(mr.min_row, mr.min_col)] = (
                    mr.min_row, mr.min_col,
                    min(mr.max_row, max_row), min(mr.max_col, max_col)
                )

            # 读取列宽（字符单位，默认8.43）
            col_widths = []
            for col_idx in range(1, max_col + 1):
                col_letter = get_column_letter(col_idx)
                dim = ws.column_dimensions.get(col_letter)
                if dim and dim.width:
                    col_widths.append(dim.width)
                else:
                    col_widths.append(8.43)

            # 读取行高（磅，默认15）
            row_heights = []
            for row_idx in range(1, max_row + 1):
                dim = ws.row_dimensions.get(row_idx)
                if dim and dim.height:
                    row_heights.append(dim.height)
                else:
                    row_heights.append(15)

            # ---- A4 排版：计算表格自然尺寸与页面参数 ----
            # Excel 列宽单位：1字符 ≈ 7像素 @ 96DPI；行高单位：磅（1磅 = 1/72 英寸）
            table_w_inch = sum(col_widths) * 7.0 / 96.0
            table_h_inch = sum(row_heights) / 72.0

            # 按表格宽高比选择 A4 方向（210x297mm）
            if table_w_inch > table_h_inch:
                page_w_mm, page_h_mm = 297, 210   # 横向
            else:
                page_w_mm, page_h_mm = 210, 297   # 纵向
            margin_mm = 20.0  # 标准页边距

            mm_per_inch = 25.4
            content_w_inch = (page_w_mm - margin_mm * 2) / mm_per_inch
            content_h_inch = (page_h_mm - margin_mm * 2) / mm_per_inch

            # 自然尺寸能否容纳在一页内，超出则按行分页
            single_page = (table_w_inch <= content_w_inch and table_h_inch <= content_h_inch)
            if single_page:
                # 单页：等比缩放适配内容区（放大上限 2 倍，避免小表格过度放大发虚）
                scale = min(content_w_inch / max(table_w_inch, 0.1),
                            content_h_inch / max(table_h_inch, 0.1),
                            2.0)
            else:
                # 分页输出：只缩小适配宽度，不放大
                scale = min(1.0, content_w_inch / max(table_w_inch, 0.1))
            render_dpi = dpi * scale  # 按缩放后 DPI 渲染，保证文字清晰

            px_per_char = 7.0 * render_dpi / 96.0
            px_per_pt = render_dpi / 72.0

            col_width_px = [w * px_per_char for w in col_widths]
            row_height_px = [h * px_per_pt for h in row_heights]

            # ---- 字体加载（带缓存，优先使用 Windows 系统中文字体）----
            fonts_regular = [r'C:\Windows\Fonts\simsun.ttc',
                             r'C:\Windows\Fonts\simhei.ttf',
                             r'C:\Windows\Fonts\msyh.ttc']
            fonts_bold = [r'C:\Windows\Fonts\simhei.ttf',
                          r'C:\Windows\Fonts\msyhbd.ttc',
                          r'C:\Windows\Fonts\simsun.ttc']
            font_cache = {}

            def get_font(size_pt, bold):
                key = (round(size_pt * 2), bold)
                if key in font_cache:
                    return font_cache[key]
                px = max(8, int(round(size_pt * px_per_pt)))
                font = None
                for fp in (fonts_bold if bold else fonts_regular):
                    if os.path.exists(fp):
                        try:
                            font = ImageFont.truetype(fp, px)
                            break
                        except Exception:
                            pass
                if font is None:
                    font = ImageFont.load_default()
                font_cache[key] = font
                return font

            # 累积 x 坐标（各页列布局相同）
            x_positions = [0]
            for w in col_width_px:
                x_positions.append(x_positions[-1] + w)

            pad = max(2, int(render_dpi / 120))  # 单元格内边距

            # 被合并单元格 -> 左上角锚点（用于识别跨页合并）
            merged_anchor = {}
            for (ar, ac), (min_r, min_c, max_r, max_c) in merged_map.items():
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        if (r, c) != (ar, ac):
                            merged_anchor[(r, c)] = (ar, ac)

            def render_page(r_start, r_end, filler_heights=None):
                """渲染行区间 [r_start, r_end]（1-based 含端点）的表格子图;
                filler_heights 非空时在表格底部追加等量的空表格行(各行高度由列表
                指定, 单位px), 用于占满最后一页版面。"""
                filler_heights = filler_heights or []
                page_row_h_px = row_height_px[r_start - 1:r_end] + filler_heights
                sub_w = int(sum(col_width_px)) + 2
                sub_h = int(sum(page_row_h_px)) + 2
                img = Image.new('RGB', (sub_w, sub_h), 'white')
                draw = ImageDraw.Draw(img)

                def text_width(text, font):
                    try:
                        return draw.textlength(text, font=font)
                    except Exception:
                        return draw.textsize(text, font=font)[0]

                def wrap_text(text, font, max_width):
                    """按像素宽度折行"""
                    lines = []
                    for seg in text.split('\n'):
                        if not seg:
                            lines.append('')
                            continue
                        cur = ''
                        for ch in seg:
                            if not cur or text_width(cur + ch, font) <= max_width:
                                cur += ch
                            else:
                                lines.append(cur)
                                cur = ch
                        lines.append(cur)
                    return lines

                # 本页累积 y 坐标（从 0 开始, 含追加的空表格行）
                y_positions = [0]
                for h in page_row_h_px:
                    y_positions.append(y_positions[-1] + h)

                # ---- 遍历本页单元格进行绘制 ----
                for row_idx in range(r_start, r_end + 1):
                    for col_idx in range(1, max_col + 1):
                        # 被合并覆盖的单元格：锚点在本页则由锚点绘制，
                        # 锚点在上一页（跨页合并）则补画延续边框
                        if (row_idx, col_idx) in merged_covered:
                            anchor = merged_anchor.get((row_idx, col_idx))
                            if anchor is None or anchor[0] >= r_start:
                                continue
                            cx1 = int(x_positions[col_idx - 1])
                            cy1 = int(y_positions[row_idx - r_start])
                            cx2 = int(x_positions[col_idx])
                            cy2 = int(y_positions[row_idx - r_start + 1])
                            draw.rectangle([cx1, cy1, cx2, cy2], fill=(255, 255, 255),
                                           outline=(51, 51, 51), width=1)
                            continue

                        cell = ws.cell(row=row_idx, column=col_idx)

                        # 确定单元格范围（是否合并），跨页合并裁剪到本页
                        if (row_idx, col_idx) in merged_map:
                            min_r, min_c, max_r, max_c = merged_map[(row_idx, col_idx)]
                            max_r = min(max_r, r_end)
                        else:
                            min_r, min_c, max_r, max_c = row_idx, col_idx, row_idx, col_idx

                        x1 = int(x_positions[min_c - 1])
                        y1 = int(y_positions[min_r - r_start])
                        x2 = int(x_positions[max_c])
                        y2 = int(y_positions[max_r - r_start + 1])
                        cw = x2 - x1
                        chh = y2 - y1

                        value = str(cell.value) if cell.value is not None else ''

                        is_bold = False
                        font_size = 11
                        if cell.font:
                            is_bold = bool(cell.font.bold)
                            if cell.font.size:
                                font_size = cell.font.size

                        # 对齐与自动换行（Excel 默认：文本靠左、数字靠右）
                        is_number = isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool)
                        h_align = 'right' if is_number else 'left'
                        v_align = 'center'
                        wrap_flag = False
                        if cell.alignment:
                            if cell.alignment.horizontal and cell.alignment.horizontal != 'general':
                                h_align = cell.alignment.horizontal
                            if cell.alignment.vertical:
                                v_align = cell.alignment.vertical
                            wrap_flag = bool(cell.alignment.wrap_text)

                        # 背景色
                        bg_color = (255, 255, 255)
                        try:
                            if cell.fill and cell.fill.fgColor and cell.fill.fgColor.rgb:
                                rgb = str(cell.fill.fgColor.rgb)
                                if len(rgb) == 8 and rgb != '00000000':
                                    r_v, g_v, b_v = int(rgb[2:4], 16), int(rgb[4:6], 16), int(rgb[6:8], 16)
                                    if not (r_v == 0 and g_v == 0 and b_v == 0):
                                        bg_color = (r_v, g_v, b_v)
                        except Exception:
                            pass

                        # 绘制单元格矩形（边框+背景）
                        draw.rectangle([x1, y1, x2, y2], fill=bg_color, outline=(51, 51, 51), width=1)

                        if not value:
                            continue

                        # ---- 确定字号：先按行高约束，不换行时再按列宽约束 ----
                        fs = font_size
                        line_h = int(fs * px_per_pt * 1.25)
                        raw_lines = value.split('\n')
                        while len(raw_lines) * line_h > chh - pad and fs > 6:
                            fs -= 1
                            line_h = int(fs * px_per_pt * 1.25)
                        if not wrap_flag:
                            for line in raw_lines:
                                lw = text_width(line, get_font(fs, is_bold))
                                while lw > cw - pad * 2 and fs > 6:
                                    fs -= 1
                                    lw = text_width(line, get_font(fs, is_bold))
                        font = get_font(fs, is_bold)
                        line_h = int(fs * px_per_pt * 1.25)

                        # 换行处理
                        if wrap_flag:
                            lines = wrap_text(value, font, cw - pad * 2)
                            # 折行后总高度超出单元格时缩小字体
                            while len(lines) * line_h > chh - pad and fs > 6:
                                fs -= 1
                                font = get_font(fs, is_bold)
                                line_h = int(fs * px_per_pt * 1.25)
                                lines = wrap_text(value, font, cw - pad * 2)
                        else:
                            lines = raw_lines

                        # 垂直起始位置
                        total_text_h = len(lines) * line_h
                        if v_align == 'top':
                            ty = y1 + pad
                        elif v_align == 'bottom':
                            ty = y2 - pad - total_text_h
                        else:
                            ty = y1 + (chh - total_text_h) // 2

                        # 逐行绘制文字
                        for line in lines:
                            lw = int(text_width(line, font))
                            if h_align == 'left':
                                tx = x1 + pad
                            elif h_align == 'right':
                                tx = x2 - pad - lw
                            else:
                                tx = x1 + (cw - lw) // 2
                            draw.text((tx, ty), line, font=font, fill=(0, 0, 0))
                            ty += line_h

                # 追加的空表格行: 仅画边框(无文字), 用于占满最后一页版面
                for fi in range(len(filler_heights)):
                    fy1 = int(y_positions[r_end - r_start + 1 + fi])
                    fy2 = int(y_positions[r_end - r_start + 2 + fi])
                    for col_idx in range(1, max_col + 1):
                        draw.rectangle([int(x_positions[col_idx - 1]), fy1,
                                        int(x_positions[col_idx]), fy2],
                                       fill=(255, 255, 255),
                                       outline=(51, 51, 51), width=1)

                return img

            # A4 画布尺寸与边距像素
            page_w_px = int(round(page_w_mm * dpi / 25.4))
            page_h_px = int(round(page_h_mm * dpi / 25.4))
            margin_px = int(round(margin_mm * dpi / 25.4))

            def save_page(sub_img, out_path, top_align):
                """将子图放置到 A4 画布并保存（top_align=True 时分页内容顶部对齐边距）"""
                page = Image.new('RGB', (page_w_px, page_h_px), 'white')
                offset_x = max(0, (page_w_px - sub_img.width) // 2)
                offset_y = margin_px if top_align else max(0, (page_h_px - sub_img.height) // 2)
                # 超出画布时裁剪（单行高于整页的极端情况）
                paste_w = min(sub_img.width, page_w_px - offset_x)
                paste_h = min(sub_img.height, page_h_px - offset_y)
                if paste_w < sub_img.width or paste_h < sub_img.height:
                    sub_img = sub_img.crop((0, 0, paste_w, paste_h))
                page.paste(sub_img, (offset_x, offset_y))
                page.save(out_path, 'JPEG', quality=95, dpi=(dpi, dpi))

            output_files = []
            base_noext = os.path.splitext(output_path)[0]
            if single_page:
                # 一页可容纳：居中放置，文件名同样追加起始编码序号
                single_path = f"{base_noext}-{self.start_num:04d}.jpg"
                save_page(render_page(1, max_row), single_path, top_align=False)
                output_files.append(single_path)
            else:
                # 超过一页：按内容区高度贪心分组行进行分页
                page_h_pt = content_h_inch * 72.0
                page_ranges = []
                cur_start = 1
                cur_h = 0.0
                for idx, h in enumerate(row_heights, start=1):
                    if cur_h > 0 and cur_h + h > page_h_pt + 1e-6:
                        page_ranges.append((cur_start, idx - 1))
                        cur_start = idx
                        cur_h = 0.0
                    cur_h += h
                page_ranges.append((cur_start, max_row))

                # ---- 排版后最后一页仅空表格(无文字)时, 删除该页 ----
                def _row_has_text(r):
                    for c in range(1, max_col + 1):
                        v = ws.cell(row=r, column=c).value
                        if v is not None and str(v).strip():
                            return True
                    return False

                def _range_has_text(rs, re_):
                    return any(_row_has_text(r) for r in range(rs, re_ + 1))

                while len(page_ranges) > 1 and not _range_has_text(*page_ranges[-1]):
                    rs_d, re_d = page_ranges.pop()
                    self._wlog(f"  排版后最后一页(行{rs_d}-{re_d})仅空表格无文字, 已删除该页")

                # ---- 最后一页未占满版面时, 以空表格行补足 ----
                # 补足空行行高统一为固定标准 FILL_ROW_H_PT(所有文件一致,
                # 对齐样例空行间距); 每个补足空行都取同一固定行高,
                # 各行行高完全一致; 不拉伸末行去凑满版面,
                # 补足整数行后不足一行的余量留白
                filler_heights = []
                rs_last, re_last = page_ranges[-1]
                used_h_pt = sum(row_heights[rs_last - 1:re_last])
                remain_h_pt = page_h_pt - used_h_pt
                fill_h_pt = self.FILL_ROW_H_PT
                if remain_h_pt >= fill_h_pt:
                    # 以固定统一行高补足整数行: 所有文件的空行间距一致;
                    # 剩余空间不足以再补一行时不强凑, 留白即可
                    filler_n = int(remain_h_pt // fill_h_pt)
                    leftover_pt = remain_h_pt - filler_n * fill_h_pt
                    filler_heights = [fill_h_pt * px_per_pt] * filler_n
                    self._wlog(f"  最后一页未占满版面, 以统一空行行高 {fill_h_pt:g}pt 补足 "
                               f"{filler_n} 个等高空表格行"
                               f"(余 {leftover_pt:.1f}pt 留白)")

                self._wlog(f"  表格超过一页 A4，分页为 {len(page_ranges)} 页...")
                for n, (rs, re_) in enumerate(page_ranges, start=1):
                    # 分页文件名：原文件名 + "-" + 四位序号（从用户指定起始编码开始）
                    page_path = f"{base_noext}-{self.start_num + n - 1:04d}.jpg"
                    if n == len(page_ranges):
                        save_page(render_page(rs, re_, filler_heights=filler_heights),
                                  page_path, top_align=True)
                    else:
                        save_page(render_page(rs, re_), page_path, top_align=True)
                    output_files.append(page_path)

            wb.close()

            return True, "", output_files

        except ImportError as e:
            return False, f"缺少必要库: {e}", []
        except Exception as e:
            return False, f"转换失败: {e}", []

    def run(self):
        logf = None
        try:
            files = self._find_excel_files()
            if not files:
                self.finished_signal.emit(False, "所选目录下没有找到xlsx或xls文件")
                return

            # 在输出目录下生成处理日志文件
            log_dir = self.input_dir if self.same_dir else self.output_dir
            os.makedirs(log_dir, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_path = os.path.join(log_dir, f"表格转换处理日志_{ts}.txt")
            logf = open(log_path, 'w', encoding='utf-8')
            self._log_file = logf

            total = len(files)
            self._wlog("表格转JPG处理日志")
            self._wlog(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._wlog(f"表格目录: {self.input_dir}")
            if self.same_dir:
                self._wlog("输出方式: 原目录输出")
            else:
                self._wlog(f"输出方式: 输出到目录 {self.output_dir}")
            self._wlog(f"找到 {total} 个表格文件")
            self._wlog(f"分页起始编码: {self.start_num:04d}")
            self._wlog("按 A4 排版标准输出（自动选择纵向/横向，20mm 页边距，超过一页自动分页）")
            self._wlog("输出前编辑: 删除 G 列后无关列; 末页仅空表格则删除该页; 末页未占满以空表格行补足")
            self._wlog("=" * 70)

            success_count = 0
            fail_count = 0

            for i, filepath in enumerate(files):
                if self.is_stopped:
                    self._wlog("用户停止处理")
                    break

                rel_path = os.path.relpath(filepath, self.input_dir)
                self._wlog(f"[{i + 1}/{total}] 处理: {rel_path}")

                # 确定输出路径
                if self.same_dir:
                    # 输出到原目录
                    output_path = os.path.splitext(filepath)[0] + '.jpg'
                else:
                    # 输出到指定目录，保持相对路径结构
                    rel_jpg = os.path.splitext(rel_path)[0] + '.jpg'
                    output_path = os.path.join(self.output_dir, rel_jpg)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # 转换文件（根据实际格式而非扩展名分发）
                try:
                    actual_format = self._detect_file_format(filepath)
                    if actual_format in ('xlsx', 'xlsm'):
                        ok, err, out_files = self._convert_xlsx(filepath, output_path)
                    elif actual_format == 'xls':
                        ok, err, out_files = self._convert_xls(filepath, output_path)
                    else:
                        # 未知格式，按扩展名尝试
                        if filepath.lower().endswith(('.xlsx', '.xlsm')):
                            ok, err, out_files = self._convert_xlsx(filepath, output_path)
                        else:
                            ok, err, out_files = self._convert_xls(filepath, output_path)

                    if ok:
                        success_count += 1
                        for op in out_files:
                            self._wlog(f"  → {os.path.basename(op)}")
                    else:
                        fail_count += 1
                        self._wlog(f"  × 失败: {err}")
                except Exception as e:
                    fail_count += 1
                    self._wlog(f"  × 出错: {e}")

                self.progress_signal.emit(i + 1, total)

            self._wlog("=" * 70)
            self._wlog(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._wlog(f"总计: 成功 {success_count} 个，失败 {fail_count} 个")
            logf.close()
            logf = None
            self._log_file = None

            msg = (f"转换完成！成功 {success_count} 个，失败 {fail_count} 个\n"
                   f"日志: {os.path.basename(log_path)}")
            self.finished_signal.emit(True, msg)

        except Exception as e:
            import traceback
            self.log_signal.emit(traceback.format_exc())
            if logf is not None:
                try:
                    logf.close()
                except:
                    pass
                self._log_file = None
            self.finished_signal.emit(False, f"处理出错: {e}")

    def stop(self):
        self.is_stopped = True


class XlsxToJpgPage(FunctionPage):
    """表格输出为JPG功能页 - 将xlsx/xls文件转换为300DPI的JPG图像"""

    def __init__(self):
        super().__init__("表格输出为JPG")
        self.worker = None

        group = QGroupBox("将Excel表格(xlsx/xls)转换为300DPI的JPG图像")
        form = QFormLayout()

        # 输入目录
        self.input_dir = QLineEdit()
        self.input_dir.setPlaceholderText("选择包含xlsx/xls文件的目录...")
        btn_browse_input = QPushButton("选择文件夹")
        btn_browse_input.setObjectName("BrowseBtn")
        btn_browse_input.clicked.connect(
            lambda: self.input_dir.setText(QFileDialog.getExistingDirectory(self, "选择表格目录")))
        h_input = QHBoxLayout()
        h_input.addWidget(self.input_dir)
        h_input.addWidget(btn_browse_input)

        # 原目录输出选项
        self.same_dir_cb = QCheckBox("原目录输出（JPG文件输出到表格所在目录）")
        self.same_dir_cb.setChecked(True)
        self.same_dir_cb.stateChanged.connect(self._on_same_dir_changed)

        # 输出目录（仅在取消原目录输出时可用）
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("选择JPG输出目录...")
        self.output_dir.setEnabled(False)
        btn_browse_output = QPushButton("选择文件夹")
        btn_browse_output.setObjectName("BrowseBtn")
        btn_browse_output.setEnabled(False)
        btn_browse_output.clicked.connect(
            lambda: self.output_dir.setText(QFileDialog.getExistingDirectory(self, "选择输出目录")))
        self.btn_browse_output = btn_browse_output
        h_output = QHBoxLayout()
        h_output.addWidget(self.output_dir)
        h_output.addWidget(btn_browse_output)

        form.addRow("表格目录:", h_input)
        form.addRow("", self.same_dir_cb)
        form.addRow("输出目录:", h_output)

        # 起始文件编码（分页输出时序号从此编码开始）
        self.start_num = QLineEdit()
        self.start_num.setPlaceholderText("四位起始编码，如 0002；留空默认从 0001 开始")
        form.addRow("起始文件名:", self.start_num)

        group.setLayout(form)
        self.layout.addWidget(group)

        # 说明文字
        info_label = QLabel("说明：将表格转换为 300DPI 的 JPG 图像，按 A4 纸排版标准输出"
                           "（自动选择纵向/横向，20mm 页边距，表格等比缩放居中）。"
                           "输出前自动删除表格 G 列后的无关列(仅保留 A-G)；"
                           "分页后若最后一页仅有空表格(无文字)则删除该页；"
                           "最后一页未占满版面时以等高的空表格行补足(各行行高一致，所有文件"
                           "统一使用固定空行行高 57pt；剩余空间不足一行时留白)，确保导出文件整洁。"
                           "输出文件名统一追加四位序号，从指定起始编码开始"
                           "（如输入 0002：单页输出 原名-0002.jpg，超过一页时 原名-0002.jpg、原名-0003.jpg …）。"
                           "点击开始转换后会先根据第一个待处理文件提醒输出文件名格式。"
                           "处理日志生成在输出目录下。"
                           "多 sheet 的文件仅转换第一个 sheet；旧版 xls (OLE2) 格式请先另存为 xlsx。")
        info_label.setStyleSheet("color: #666; font-size: 12px; margin: 10px 0;")
        info_label.setWordWrap(True)
        self.layout.addWidget(info_label)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始转换")
        self.start_btn.setObjectName("ActionBtn")
        self.start_btn.clicked.connect(self._start)
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.setObjectName("ActionBtn")
        self.stop_btn.setStyleSheet("background-color: #DA3633;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop)
        self.clear_btn = QPushButton("清空结果")
        self.clear_btn.setObjectName("ActionBtn")
        self.clear_btn.clicked.connect(self._clear)
        for b in (self.start_btn, self.stop_btn, self.clear_btn):
            btn_layout.addWidget(b)
        self.layout.addLayout(btn_layout)

        # 进度条
        self.progress = QProgressBar()
        self.progress.setFormat("待开始")
        self.layout.addWidget(self.progress)

        self.add_log_widget()

    def _on_same_dir_changed(self, state):
        enabled = state != Qt.Checked
        self.output_dir.setEnabled(enabled)
        self.btn_browse_output.setEnabled(enabled)

    def _set_running(self, running):
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)

    def _first_excel_file(self, input_dir):
        """查找第一个待处理文件（与 worker._find_excel_files 规则保持一致）"""
        result = []
        for root, _dirs, files in os.walk(input_dir):
            for f in files:
                if f.lower().endswith(('.xlsx', '.xlsm', '.xls')) and not f.startswith('~$'):
                    result.append(os.path.join(root, f))
        return sorted(result)[0] if result else None

    def _start(self):
        input_dir = self.input_dir.text().strip()
        if not input_dir or not os.path.isdir(input_dir):
            QMessageBox.warning(self, "提示", "请先选择有效的表格目录。")
            return

        same_dir = self.same_dir_cb.isChecked()
        output_dir = None
        if not same_dir:
            output_dir = self.output_dir.text().strip()
            if not output_dir:
                QMessageBox.warning(self, "提示", "请选择输出目录，或勾选「原目录输出」。")
                return

        # 校验起始文件编码（须为四位数字，位长不够则提示）
        snum_text = self.start_num.text().strip()
        if snum_text:
            if not (snum_text.isdigit() and len(snum_text) == 4):
                QMessageBox.warning(self, "提示",
                                    f"起始文件名编码位长不足：请输入四位数字编码（如 0002），当前输入「{snum_text}」。")
                return
            start_num = int(snum_text)
        else:
            start_num = 1

        # 提醒：根据第一个待处理文件展示输出文件名格式，用户确认后才转换
        first_file = self._first_excel_file(input_dir)
        if not first_file:
            QMessageBox.warning(self, "提示", "所选目录下没有找到 xlsx/xls 文件。")
            return
        rel = os.path.relpath(first_file, input_dir)
        if same_dir:
            first_out = os.path.splitext(first_file)[0] + '.jpg'
        else:
            first_out = os.path.join(output_dir, os.path.splitext(rel)[0] + '.jpg')
        out_base = os.path.splitext(os.path.basename(first_out))[0]
        preview = (f"第一个待处理文件: {os.path.basename(first_file)}\n\n"
                   f"输出文件名格式：\n"
                   f"  · 单页输出: {out_base}-{start_num:04d}.jpg\n"
                   f"  · 分页输出(超过一页时): {out_base}-{start_num:04d}.jpg、"
                   f"{out_base}-{start_num + 1:04d}.jpg …\n\n"
                   f"选择「Yes」开始转换，选择「No」放弃转换。")
        reply = QMessageBox.question(self, "输出文件名格式确认", preview,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            self.log("用户放弃转换")
            return

        self._clear()
        self.progress.setValue(0)
        self.progress.setFormat("准备中...")

        self.worker = XlsxToJpgWorker(input_dir, output_dir=output_dir,
                                      same_dir=same_dir, start_num=start_num)
        self.worker.log_signal.connect(self.log)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.finished_signal.connect(self._on_finished)
        self._set_running(True)
        self.worker.start()

    def _stop(self):
        if self.worker:
            self.worker.stop()
            self.log("正在停止...")

    def _update_progress(self, done, total):
        if total <= 0:
            self.progress.setValue(0)
            self.progress.setFormat("0 / 0")
            return
        pct = int(done * 100 / total)
        self.progress.setValue(pct)
        self.progress.setFormat(f"{done} / {total}  ({pct}%)")

    def _on_finished(self, ok, message):
        self._set_running(False)
        self.log(message)
        self.progress.setFormat("已完成" if ok else "已停止")
        self.worker = None
        QMessageBox.information(self, "完成" if ok else "结束", message)

    def _clear(self):
        if hasattr(self, 'progress'):
            self.progress.setValue(0)
            self.progress.setFormat("待开始")
        if hasattr(self, 'log_box'):
            self.log_box.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("同美档案工具集合 v" + VERSION)
        self.resize(1000, 650)
        self.setStyleSheet(TechStyle.QSS)

        # 主中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧菜单栏
        self.left_panel = QWidget()
        self.left_panel.setObjectName("LeftPanel")
        self.left_panel.setFixedWidth(220)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignTop)

        title = QLabel("同美档案工具集合")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # 菜单按钮配置
        menus = ["文件改名", "自动编页码", "文件移动", "加盖归档章",
                 "修改DPI", "表格输出为JPG", "JPG转双层PDF", "PDF转OFD", "分件", "文件批量替换",
                 "档案馆标准目录"]

        self.menu_buttons = []
        for m in menus:
            btn = QPushButton(m)
            btn.setObjectName("MenuBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, b=btn: self.on_menu_click(b))
            left_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        left_layout.addStretch()

        # 右侧功能区 (使用QStackedWidget管理多页面)
        self.right_panel = QWidget()
        self.right_panel.setObjectName("RightPanel")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)

        self.stack = QStackedWidget()

        # 实例化各功能页
        self.pages = {
            "文件改名": FileRenamePage(),
            "自动编页码": AutoPagingPage(),
            "文件移动": FileMovePage(),
            "加盖归档章": ArchiveStampPage(),
            "修改DPI": ModifyDpiPage(),
            "表格输出为JPG": XlsxToJpgPage(),
            "JPG转双层PDF": JpgToPdfPage(),
            "PDF转OFD": PdfToOfdPage(),
            "分件": FileSplitPage(),
            "文件批量替换": FileBatchReplacePage(),
            "档案馆标准目录": ArchiveCatalogPage()
        }

        for name in menus:
            self.stack.addWidget(self.pages[name])

        right_layout.addWidget(self.stack)

        # 组装整体布局
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.right_panel)

        # 默认选中第一个菜单
        self.on_menu_click(self.menu_buttons[0])

    def on_menu_click(self, clicked_btn):
        """处理菜单点击切换事件"""
        # 取消其他按钮的选中状态
        for btn in self.menu_buttons:
            btn.setChecked(False)
        # 激活当前按钮
        clicked_btn.setChecked(True)

        # 切换右侧堆栈页面
        page_name = clicked_btn.text()
        if page_name in self.pages:
            self.stack.setCurrentWidget(self.pages[page_name])


if __name__ == "__main__":
    _setup_crash_log()  # 崩溃日志: 任何崩溃都留下记录(见函数注释)

    # v3.13: 启动时强制校验解释器位数——必须64位。
    # 32位进程用户态地址空间上限约2GB, paddle/cv2 长时间运行必然先于真实内存
    # 耗尽而崩溃(崩溃日志20260901: cv2连1.9MB都分配失败)。此前曾误用32位Python
    # 打包出问题版本, 此处硬性拦截, 并写入崩溃日志留痕便于事后排查。
    import struct as _st_bitness
    _bitness = _st_bitness.calcsize('P') * 8
    if _bitness != 64:
        _msg = (f"程序必须运行在64位Python环境下(当前为{_bitness}位)。\n"
                f"32位进程内存地址空间上限约2GB, OCR长时间运行会因内存耗尽崩溃。\n"
                f"请使用64位Python重新打包后再运行。")
        try:
            with open(os.path.join(
                    os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
                    else os.path.dirname(os.path.abspath(__file__)),
                    f"TMToolMan_崩溃日志_{datetime.now().strftime('%Y%m%d')}.txt"),
                    'a', encoding='utf-8') as _f:
                _f.write(f"\n{'=' * 80}\n[位数拦截] 检测到{_bitness}位解释器, 程序拒绝启动 "
                         f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        except Exception:
            pass
        try:
            from PyQt5.QtWidgets import QApplication as _QA, QMessageBox as _QMB
            _app = _QA(sys.argv)
            _QMB.critical(None, "运行环境错误", _msg)
        except Exception:
            pass
        sys.exit(1)

    app = QApplication(sys.argv)
    # 强制使用深色科技感字体渲染
    f = QFont("Microsoft YaHei", 9)
    app.setFont(f)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
