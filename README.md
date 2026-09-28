# TMTool — 同美档案工具集

面向档案数字化加工与法院档案整理的一组 Windows 桌面工具（PyQt5 为主），覆盖图像质检、扫描件处理、双层 PDF/OFD 生成、文件整理改名、目录报表生成等日常批量作业。全部工具均针对 **Windows 7 SP1 及以上** 环境开发与打包，批量处理均不修改原始文件（结果写入独立输出目录）。

## 工具一览

| 工具 | 入口文件 | 当前版本 | 说明 |
|------|----------|----------|------|
| 同美档案工具集合 | `TMToolMan.py` | v3.26 | 主程序，11 个功能页的集成工具箱（见下） |
| 同美图像质检工具 | `BlackCircleRemover.py`（打包名 `ImageCheckTool`） | v3.4 | 扫描图像黑圈检测裁剪、去黑边、纠偏、订书钉散点清理 |
| DPI 扫描工具 | `CheckDPI.py` | - | 递归扫描 DPI 低于阈值的 JPG 文件（已集成进主程序「修改DPI」页） |
| 日报编写程序 | `DailyReport.py` | - | 电子卷宗随案生成中心日报：日历填报、日/周/月合计、导出 Excel |
| 错别字检查工具 | `TypoChecker.py` | - | 基于 pycorrector 数据检查 Excel 指定列错别字并修改 |
| 分件处理工具（独立版） | `split_processing_tool.py` | - | 法院一张网案卷分件：按页码范围分件并生成 PDF（tkinter 版，主程序「分件」页为集成版） |
| Umi-OCR 接口模块 | `pdf_ocr_processor.py` | - | 调用本地 Umi-OCR HTTP 接口对 PDF 做 OCR 的封装模块 |

## 同美档案工具集合（TMToolMan）

主程序为深色科技感界面：左侧菜单、右侧功能页。窗口标题实时显示版本号。

| 功能页 | 说明 |
|--------|------|
| 文件改名 | 三个 TAB：按目录名批量重命名 / 文件夹命名标准化（目标格式 `全宗号-专业·专业类型·年限-保管期限-件号`，支持直接填写或引用现有目录、预览、改名记录 Excel）/ 修改文件扩展名 |
| 自动编页码 | 在 JPG 文件右上角批量添加序号 |
| 文件移动 | 按扩展名 / 修改日期 / 全部，在源目录与目标目录之间批量移动 |
| 加盖归档章 | 从目录名提取全宗号、年份、档号自动生成归档章（45mm×16mm），JPG 顶部加 18mm 白边后居中加盖 |
| 修改DPI | 递归批量修改 JPG/JPEG 的 DPI（仅改 DPI，不影响像素尺寸） |
| 表格输出为JPG | 将 Excel 表格批量输出为 JPG 图片 |
| JPG转双层PDF | 目录内 JPG 合并为同名可搜索双层 PDF，内置本地 OCR（PaddleOCR，支持 CPU/GPU 模式），可同时生成同名 OFD；含 GPU 崩溃降级、内存看门狗、周期复探等稳定性机制 |
| PDF转OFD | 已带文本层的 PDF 直接转双层 OFD；无文本层的自动走「渲染 → OCR → 双层 OFD」全流程 |
| 分件 | 法院一张网案卷分件：按 29 个固定项目/自定义项目与页码范围拆分 JPG 并生成 PDF，支持合并 0000 编号目录（卷底备考表与卷皮目录） |
| 文件批量替换 | 将处理输出的 JPG 按目录结构替换目标目录中的同名图片 |
| 档案馆标准目录 | 业务/文书双 TAB；解析编码子目录名（如 `J380-ZY·2021-Y-FGC-0001`），配合机构代码对应表，按模板 xlsx 批量生成「档案案卷目录」「档案案件目录」，支持一次勾选同时生成两种 |

各功能的详细变更见 `TMToolMan.py` 文件头部的 `CHANGELOG`。

## 同美图像质检工具（ImageCheckTool）

原黑圈检测工具的升级版，打包产物更名为 `ImageCheckTool`。面向扫描档案图像的一键清理：

- **黑圈检测裁剪**：识别图像左右两侧边距内的黑色不规则圆圈（打号机标记等）并白色填充；
- **去黑边、纠偏**：扫描仪黑边清除 + 小角度倾斜自动纠偏（投影法 + Hough 双重印证）；
- **订书钉/散点清理**：空白区订书钉孔、散点杂质清理；
- **内容保护**：印章、手写签批、带底色图像与文字行保护带，避免误清理笔画（v3.4 修复了页首标题行文字被掏空的问题）；
- **多线程并行**：默认 4 线程，可调 1–16 线程，批量处理提速 2–4 倍；
- 处理前后并排预览、逐文件日志与统计。

详细使用说明见 [README_黑圈处理.md](./README_黑圈处理.md) 与 [README_黑圈工具_v2.2.md](./README_黑圈工具_v2.2.md)。

## 目录结构

```
TMTool/
├── TMToolMan.py                 # 主程序：同美档案工具集合
├── BlackCircleRemover.py        # 图像质检工具源码（打包名 ImageCheckTool）
├── CheckDPI.py                  # DPI 扫描工具
├── DailyReport.py               # 日报编写程序
├── daily_report_data.py         # 日报数据管理模块
├── daily_reports.db             # 日报本地数据（SQLite）
├── TypoChecker.py               # 错别字检查工具
├── split_processing_tool.py     # 分件处理工具（tkinter 独立版）
├── pdf_ocr_processor.py         # Umi-OCR 接口封装模块
├── 业务档案按件目录模板.xlsx      # 档案馆标准目录模板
├── 业务档案案卷目录模板.xlsx      # 档案馆标准目录模板
├── 机构代码对应模板.xlsx          # 机构代码 → 机构名称对应表模板
├── build_blackcircle.bat        # ImageCheckTool 打包脚本（Win7 兼容）
├── build_daily_report.bat       # DailyReport 打包脚本（Win7 兼容）
├── build_win7.bat               # CheckDPI 打包脚本（Win7 兼容）
├── ImageCheckTool.spec          # PyInstaller spec（入口 BlackCircleRemover.py）
└── CheckDPI.spec                # PyInstaller spec
```

## 环境要求与依赖

- Windows 7 SP1 及以上（打包产物无需 Python 环境，需 Visual C++ 运行库）
- Python 3.8+（64 位。JPG转双层PDF 功能在 32 位环境下会被启动校验直接拦截）

```bash
pip install PyQt5 Pillow numpy openpyxl
# JPG转双层PDF / PDF转OFD 功能额外依赖
pip install paddleocr paddlepaddle  # GPU 模式安装 paddlepaddle-gpu
pip install PyMuPDF
```

## 快速开始

```bash
# 主程序
python TMToolMan.py

# 图像质检工具
python BlackCircleRemover.py

# DPI 扫描
python CheckDPI.py

# 日报编写
python DailyReport.py

# 错别字检查
python TypoChecker.py

# 分件处理（独立版）
python split_processing_tool.py
```

## 打包发布

各 `.bat` 脚本均固定使用 PyInstaller 4.10（最后一个兼容 Windows 7 的版本）：

| 脚本 | 产物 |
|------|------|
| `build_blackcircle.bat` / `pyinstaller ImageCheckTool.spec` | `dist\ImageCheckTool\`（多文件模式） |
| `build_daily_report.bat` | `dist\DailyReport.exe`（单文件） |
| `build_win7.bat` | `dist\CheckDPI.exe`（单文件） |

## 版本记录

- `TMToolMan.py`、`BlackCircleRemover.py` 文件头部维护各自的 `VERSION` 与 `CHANGELOG`（每次修改递增版本号并追加记录），主程序窗口标题会显示当前版本号；
- 历史版本详情见 [Releases](https://github.com/TongMei-Tech/TMTool/releases)。
