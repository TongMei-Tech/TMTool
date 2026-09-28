# TMTool 修改说明（CHANGELOG）

每次代码修改必须：①递增对应程序文件头部的 `VERSION` 并在其 `CHANGELOG` 追加记录；②在本文件追加对应条目；③提交并为该版本创建 GitHub Release。

各程序内部完整变更记录见 `TMToolMan.py` / `BlackCircleRemover.py` 文件头部 `CHANGELOG`（本文件为仓库级汇总）。

## TMToolMan v3.28（2026-09-28）

用户确认 20260928 场景中成串『Windows fatal exception: access violation』**伴随程序异常退出**（系统级崩溃）——修正 v3.27 的绝对化表述并加固：

- **修正误导文案**：崩溃日志备注与 GPU 模式界面提示改为分级表述——偶发单行 = 显卡驱动内部已自行处理的异常探测，程序未受影响；**成串出现 = GPU 驱动/显存状态恶化征兆，程序可能在此时点前后 access violation 崩溃退出**，建议停止本批改用 CPU 模式完成并反馈崩溃日志与 run_monitor 采样。
- **新增 `_drop_ocr_safe()`（跨线程析构加固）**：`_rebuild_ocr_cpu` / `_reprobe_ocr` 原先在工作线程直接 `self._ocr = None`，GPU predictor 的 C++ 析构（含 CUDA 上下文 teardown）可能在非创建线程执行——跨线程 teardown 是 access violation 的已知诱因。现一律提交到 OCR 服务线程（= 创建线程）内 GC 析构；服务线程挂死/超时时把实例钉入 `_ocr_orphans` 孤儿列表永不在其他线程析构（按次泄漏，每轮运行至多数个实例，以可承受泄漏换取不崩溃）。
- 待证：需完整崩溃日志（成串提示行后若有 `Current thread` 堆栈即崩溃点）与该批次 `run_monitor_时间戳.txt` 精确定位；若 GPU 路径仍崩，下一步实施 **OCR 子进程隔离**（推理崩溃只损失子进程，父进程自动重启/降级）。

## TMToolMan v3.27（2026-09-28）

GPU 模式 JPG 转双层 PDF 长时间处理大文件（单线程 + 单文件 100+ 页）生成十几个 PDF 后出现成串『Windows fatal exception: access violation』单行提示的排查与削减：

- **分段边界 GPU 缓存释放（empty_cache）由每分段一次改为每 6 分段一次**——大文件时自适应 CHUNK=8 页，原逻辑单个百页文件要空转十余次「全量归还驱动 → 重新申请」循环，十几个文件后驱动侧显存碎片化；auto_growth 分配器复用自留池空闲块本就是抗碎片行为。目录结束处仍无条件释放，200 页引擎例行重建也会释放。
- **GPU 模式新增每 5 个目录整实例重建 OCR 引擎**（`_svc_recycle_engine`，服务线程内丢弃 + GC + empty_cache，下次 OCR 懒重建）——与 200 页页数阈值互补（大文件目录凑满 200 页前碎片已累积），实例级销毁重建是唯一能彻底归还驱动侧资源的显存整理方式。
- **运行监控采样改用 NVML 读全卡显存**（nvml.dll 句柄模块级缓存），不再从监控线程并发调用 paddle CUDA API（`memory_allocated` 等），消除与 OCR 服务线程推理的并发驱动入口。
- **顺带修复 NVML 路径栈越界隐患**：原给 `nvmlDeviceGetMemoryInfo` 传两个独立 `c_ulonglong`（共 16 字节且不保证相邻），而驱动要写整个 `nvmlMemory_t`（≥24 字节）结构体——改为分配带余量的结构体缓冲。
- 启动时崩溃日志写入说明性备注、GPU 模式启动时界面日志提示。

## TMToolMan v3.26（2026-09-10）

修复 GPU 模式 JPG 转双层 PDF 段错误崩溃（崩溃日志 20260910：OCR 服务线程在 paddleocr `img_decode` 内部 `np.frombuffer → cv2.imdecode` 发生 access violation，GPU 模式 4 工作线程运行中）：各工作线程调用 OCR 前用 PIL 预解码图像为 BGR 连续 ndarray（`np.array` 拷贝 + `ascontiguousarray`，非 `np.asarray` 共享内存），服务线程内完全不再执行文件读取与 `cv2.imdecode`（崩溃点移出）；首次探测 / 复探 / CPU 重探测三处探测图同样预解码；预解码失败回退原路径模式。

## 仓库变更（2026-09-28）

- 新增项目 `README.md`：工具一览、主程序 11 功能页说明、图像质检工具介绍、目录结构、依赖与打包说明（fa060e3）。
- 新增本 `CHANGELOG.md` 作为仓库级修改说明汇总。
