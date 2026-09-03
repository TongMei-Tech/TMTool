"""
日报数据管理模块
负责数据的存储、加载、合计计算
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# 部门配置：(序号, 部门名, 归档类别)
DEPARTMENTS = [
    (1, '民一', '民事'),
    (2, '民二', ''),
    (3, '速裁', ''),
    (4, '综合', ''),
    (5, '沣东', '执行'),
    (6, '沣西', ''),
    (7, '秦汉', ''),
    (8, '空港', ''),
    (9, '泾河', ''),
    (10, '执行', '刑事'),
    (11, '刑事', ''),
    (12, '院领导', ''),
    (13, '立案庭', ''),
    (14, '审管办', ''),
    (15, '上诉', ''),
    (16, '鉴定', ''),
]

# 归档分组定义：(类别名, 起始行索引0-based, 行数)
# 民事: rows 0-3 (民一、民二、速裁、综合) = 4行
# 执行: rows 4-8 (沣东、沣西、秦汉、空港、泾河) = 5行
# 刑事: rows 9-15 (执行、刑事、院领导、立案庭、审管办、上诉、鉴定) = 7行
ARCHIVE_GROUPS = [
    ('民事', 0, 4),
    ('执行', 4, 5),
    ('刑事', 9, 7),
]

# 数据列（每行9列可编辑数据）
# 索引: 0=D(立案接收/案), 1=E(立案扫描质检/页), 2=F(立案上传/册),
#        3=G(结案接收/案), 4=H(结案扫描质检/页), 5=I(结案上传/册),
#        6=J(卷宗整理/册), 7=K(装订/册), 8=M(归档/案)
COL_COUNT = 9
COL_NAMES = [
    '立案接收/案', '立案扫描质检/页', '立案上传/册',
    '结案接收/案', '结案扫描质检/页', '结案上传/册',
    '卷宗整理/册', '装订/册',
    '归档/案',
]


def _app_dir():
    """获取应用程序所在目录（兼容PyInstaller打包后的路径）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，sys.executable 指向 exe 文件
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _data_file():
    """旧版json数据文件路径(用于自动迁移)"""
    return os.path.join(_app_dir(), 'daily_reports.json')


def _db_file():
    """sqlite数据库路径：与程序同目录下的 daily_reports.db"""
    return os.path.join(_app_dir(), 'daily_reports.db')


def _db_conn():
    """打开数据库并确保表结构。失败返回None(降级json)。"""
    try:
        import sqlite3
        conn = sqlite3.connect(_db_file())
        conn.execute("""CREATE TABLE IF NOT EXISTS daily_reports (
            date_str TEXT PRIMARY KEY,
            data_json TEXT NOT NULL,
            updated_at TEXT)""")
        conn.commit()
        return conn
    except Exception:
        return None


def _migrate_json_if_any(conn):
    """旧json数据自动迁移进sqlite(仅当库为空且json存在)。迁移后json改名为.bak。"""
    try:
        n = conn.execute("SELECT COUNT(*) FROM daily_reports").fetchone()[0]
        if n > 0:
            return
        jp = _data_file()
        if not os.path.exists(jp):
            return
        with open(jp, 'r', encoding='utf-8') as f:
            old = json.load(f)
        if not isinstance(old, dict):
            return
        conn.executemany(
            "INSERT OR REPLACE INTO daily_reports VALUES (?,?,?)",
            [(d, json.dumps(rows, ensure_ascii=False),
              datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
             for d, rows in old.items()])
        conn.commit()
        os.replace(jp, jp + '.bak')   # 保留备份, 防误删
    except Exception:
        pass


def load_all_data():
    """加载所有日报数据，返回 {date_str: [[row0 data], [row1 data], ...], ...}
    存储: sqlite(daily_reports.db); 库不可用时降级读旧json。"""
    conn = _db_conn()
    if conn is not None:
        try:
            _migrate_json_if_any(conn)
            rows = conn.execute("SELECT date_str, data_json FROM daily_reports").fetchall()
            return {d: json.loads(j) for d, j in rows}
        except Exception:
            return {}
        finally:
            conn.close()
    # 降级: sqlite不可用 → 读旧json
    path = _data_file()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_all_data(data):
    """保存所有日报数据(sqlite整表重写, 接口与旧json版一致)"""
    conn = _db_conn()
    if conn is not None:
        try:
            conn.execute("DELETE FROM daily_reports")
            conn.executemany(
                "INSERT INTO daily_reports VALUES (?,?,?)",
                [(d, json.dumps(rows, ensure_ascii=False),
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                 for d, rows in data.items()])
            conn.commit()
        finally:
            conn.close()
        return
    # 降级: sqlite不可用 → 写json
    path = _data_file()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_day_data(data, date_str):
    """获取某天的数据，返回 16行x9列 的二维列表（None表示未填）"""
    if date_str in data:
        stored = data[date_str]
        # 兼容旧数据：如果是10列，去掉index 8
        result = []
        for row in stored:
            if len(row) == 10:
                result.append(row[:8] + [row[9]])
            elif len(row) == COL_COUNT:
                result.append(row)
            else:
                r = list(row) + [None] * (COL_COUNT - len(row))
                result.append(r[:COL_COUNT])
        return result
    return [[None] * COL_COUNT for _ in range(len(DEPARTMENTS))]


def set_day_data(data, date_str, day_data):
    """设置某天的数据"""
    data[date_str] = day_data
    save_all_data(data)


def calc_daily_total(day_data):
    """计算日合计：按列求和，返回长度为COL_COUNT的列表"""
    totals = [0] * COL_COUNT
    for row in day_data:
        for c in range(COL_COUNT):
            v = row[c]
            if v is not None:
                try:
                    totals[c] += int(v)
                except (ValueError, TypeError):
                    pass
    return totals


def get_week_dates(date_str):
    """获取某日期所在周的周一到周日的所有日期字符串列表"""
    dt = datetime.strptime(date_str, '%Y%m%d')
    monday = dt - timedelta(days=dt.weekday())
    return [(monday + timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]


def get_month_dates(date_str):
    """获取某日期所在月的所有日期字符串列表"""
    dt = datetime.strptime(date_str, '%Y%m%d')
    year, month = dt.year, dt.month
    import calendar
    days_in_month = calendar.monthrange(year, month)[1]
    return [f"{year:04d}{month:02d}{d:02d}" for d in range(1, days_in_month + 1)]


def get_week_number(date_str):
    """获取日期在当月中的周数（第几周），周一为一周开始"""
    dt = datetime.strptime(date_str, '%Y%m%d')
    first_day = dt.replace(day=1)
    first_monday = first_day - timedelta(days=first_day.weekday())
    current_monday = dt - timedelta(days=dt.weekday())
    week_num = (current_monday - first_monday).days // 7 + 1
    return week_num


def calc_weekly_total(data, date_str, baselines=None):
    """
    计算周合计：上一个周的期末数 + 当前周已填天数的合计
    如果没有历史数据，则使用baselines作为起点
    """
    dt = datetime.strptime(date_str, '%Y%m%d')
    current_monday = dt - timedelta(days=dt.weekday())
    prev_week_end = (current_monday - timedelta(days=1)).strftime('%Y%m%d')

    # 上周的周合计（递归）
    if baselines is None:
        baselines = {'weekly': [0] * COL_COUNT, 'monthly': [0] * COL_COUNT}
    prev_weekly = list(baselines['weekly'])  # 默认用基准值
    if prev_week_end in data:
        prev_weekly = calc_weekly_total(data, prev_week_end, baselines)

    # 本周已填日期的合计
    week_dates = get_week_dates(date_str)
    current_week_sum = [0] * COL_COUNT
    for d in week_dates:
        if d in data:
            day = get_day_data(data, d)
            for row in day:
                for c in range(COL_COUNT):
                    v = row[c]
                    if v is not None:
                        try:
                            current_week_sum[c] += int(v)
                        except (ValueError, TypeError):
                            pass

    return [prev_weekly[c] + current_week_sum[c] for c in range(COL_COUNT)]


def calc_monthly_total(data, date_str, baselines=None):
    """
    计算月合计：上个月的月合计 + 当月已填天数的合计
    如果没有历史数据，则使用baselines作为起点
    """
    dt = datetime.strptime(date_str, '%Y%m%d')
    first_of_month = dt.replace(day=1)
    last_of_prev = first_of_month - timedelta(days=1)
    prev_month_end = last_of_prev.strftime('%Y%m%d')

    # 上月月合计
    if baselines is None:
        baselines = {'weekly': [0] * COL_COUNT, 'monthly': [0] * COL_COUNT}
    prev_monthly = list(baselines['monthly'])  # 默认用基准值
    if prev_month_end in data:
        prev_monthly = calc_monthly_total(data, prev_month_end, baselines)

    # 当月已填日期的合计
    month_dates = get_month_dates(date_str)
    current_month_sum = [0] * COL_COUNT
    for d in month_dates:
        if d in data:
            day = get_day_data(data, d)
            for row in day:
                for c in range(COL_COUNT):
                    v = row[c]
                    if v is not None:
                        try:
                            current_month_sum[c] += int(v)
                        except (ValueError, TypeError):
                            pass

    return [prev_monthly[c] + current_month_sum[c] for c in range(COL_COUNT)]


def format_date_with_week(date_str):
    """格式化日期显示：20260808（第二周）"""
    dt = datetime.strptime(date_str, '%Y%m%d')
    week_num = get_week_number(date_str)
    week_names = {1: '第一周', 2: '第二周', 3: '第三周', 4: '第四周', 5: '第五周'}
    return f"{dt.strftime('%Y%m%d')}（{week_names.get(week_num, f'第{week_num}周')}）"


def format_title_with_month(date_str):
    """格式化标题：电子卷宗随案生成中心工作量统计表（8月）"""
    dt = datetime.strptime(date_str, '%Y%m%d')
    return f"电子卷宗随案生成中心工作量统计表（{dt.month}月）"


# === 归档类别管理 ===

def get_default_archive_category():
    """返回每行默认的归档类别列表（16行）"""
    return [arc for _, _, arc in DEPARTMENTS]


def _categories_file():
    """归档类别数据文件"""
    return os.path.join(_app_dir(), 'archive_categories.json')


def load_categories():
    """加载归档类别数据"""
    path = _categories_file()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_categories(cats):
    """保存归档类别数据"""
    path = _categories_file()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cats, f, ensure_ascii=False, indent=2)


def get_day_categories(cats, date_str):
    """获取某天的归档类别列表（16个字符串），无数据则返回默认值"""
    if date_str in cats:
        stored = cats[date_str]
        defaults = get_default_archive_category()
        result = []
        for i in range(len(DEPARTMENTS)):
            if i < len(stored) and stored[i]:
                result.append(stored[i])
            else:
                result.append(defaults[i])
        return result
    return get_default_archive_category()


def set_day_categories(cats, date_str, cat_list):
    """设置某天的归档类别列表"""
    cats[date_str] = cat_list
    save_categories(cats)


# === 基准值管理（初始化功能）===

def _baselines_file():
    """基准值数据文件"""
    return os.path.join(_app_dir(), 'baselines.json')


def load_baselines():
    """加载基准值，返回 {'weekly': [9个值], 'monthly': [9个值]}"""
    path = _baselines_file()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'weekly': [0] * COL_COUNT, 'monthly': [0] * COL_COUNT}


def save_baselines(baselines):
    """保存基准值"""
    path = _baselines_file()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(baselines, f, ensure_ascii=False, indent=2)


def has_any_data():
    """检查是否有之前录入的数据(sqlite有行 或 旧json/bak存在均算有)。
    修复: 旧实现只查json——sqlite迁移把json改名.bak后永远返回False,
    导致每次启动都被误判'首次使用'而弹出初始化窗口。"""
    conn = _db_conn()
    if conn is not None:
        try:
            n = conn.execute("SELECT COUNT(*) FROM daily_reports").fetchone()[0]
            if n > 0:
                return True
        except Exception:
            pass
        finally:
            conn.close()
    # sqlite无数据时, 兼容尚未迁移的旧json(或其.bak)
    return (os.path.exists(_data_file())
            or os.path.exists(_data_file() + '.bak'))


# === 归档数据（按组）===

def get_archive_group_data(day_data):
    """从16行数据中提取3个归档组的合计值，返回 [民事合计, 执行合计, 刑事合计]"""
    result = []
    for _, start, count in ARCHIVE_GROUPS:
        group_sum = 0
        for i in range(start, start + count):
            if i < len(day_data) and day_data[i][8] is not None:
                try:
                    group_sum += int(day_data[i][8])
                except (ValueError, TypeError):
                    pass
        result.append(group_sum)
    return result


def set_archive_group_value(day_data, group_idx, value):
    """将归档值设置到组内第一行，其余行清空"""
    _, start, count = ARCHIVE_GROUPS[group_idx]
    for i in range(start, start + count):
        if i < len(day_data):
            if i == start:
                day_data[i][8] = value
            else:
                day_data[i][8] = None
