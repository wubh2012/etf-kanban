import sqlite3
import os

def init_database():
    """初始化SQLite数据库，创建必要的表"""
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'etf_kanban.db')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建合并的指数数据表（包含原indices和core_data的所有字段）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS index_with_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,              -- 指数名称，如"创业板"
        code TEXT UNIQUE NOT NULL,       -- 指数代码，如"399006"
        current_point REAL,              -- 当前点位
        change_percent REAL,             -- 距离大支撑涨跌幅百分比
        support_point REAL,              -- 支撑点位
        pressure_point REAL,             -- 压力点位
        progress REAL,                   -- 在支撑压力位间的百分比位置
        etf_code TEXT,                   -- 场内基金代码
        mutual_code TEXT,                -- 场外基金代码
        support_level TEXT,              -- 支撑点位笔记
        normal_level TEXT,               -- 正常区间笔记
        pressure_level TEXT,             -- 压力点位笔记
        sell_level TEXT,                 -- 卖出点位笔记
        other_level TEXT,                -- 其他信息
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建历史信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        index_code TEXT NOT NULL,        -- 关联的指数代码
        type TEXT NOT NULL,              -- 'three_year_low' 或 'three_year_high'
        value REAL NOT NULL,             -- 点位数值
        date TEXT NOT NULL,              -- 日期 'YYYY-MM-DD'
        change_percent REAL,             -- 涨跌幅百分比
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (index_code) REFERENCES index_with_data(code),
        UNIQUE(index_code, type)         -- 每个指数每种类型只有一条记录
    )
    ''')
    
    # 提交更改
    conn.commit()
    
    # 检查是否需要从旧表迁移数据
    migrate_old_data(cursor)
    
    # 插入示例数据（如果没有数据）
    insert_sample_data(cursor)
    
    # 再次提交
    conn.commit()
    
    # 关闭连接
    conn.close()
    
    print(f"数据库初始化完成: {db_path}")

def migrate_old_data(cursor):
    """从旧表迁移数据到新表"""
    # 检查旧表是否存在
    try:
        cursor.execute("SELECT COUNT(*) FROM indices")
        has_old_data = cursor.fetchone()[0] > 0
    except sqlite3.OperationalError:
        has_old_data = False
    
    if not has_old_data:
        return
    
    print("检测到旧表数据，开始迁移...")
    
    # 迁移数据
    try:
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM index_with_data")
        if cursor.fetchone()[0] == 0:
            # 先插入指数数据
            cursor.execute('''
            INSERT INTO index_with_data (
                name, code, current_point, change_percent, support_point, 
                pressure_point, progress, updated_at, created_at
            )
            SELECT 
                name, code, current_point, change_percent, support_point, 
                pressure_point, progress, updated_at, created_at
            FROM indices
            ''')
            
            # 更新核心数据
            cursor.execute('''
            UPDATE index_with_data
            SET 
                etf_code = core_data.etf_code,
                mutual_code = core_data.mutual_code,
                support_level = core_data.support_level,
                normal_level = core_data.normal_level,
                pressure_level = core_data.pressure_level,
                sell_level = core_data.sell_level,
                other_level = core_data.other_level,
                updated_at = CURRENT_TIMESTAMP
            FROM core_data
            WHERE index_with_data.code = core_data.index_code
            ''')
            
            # 更新历史表的外键引用
            cursor.execute('''
            UPDATE history
            SET updated_at = CURRENT_TIMESTAMP
            WHERE index_code IN (SELECT code FROM index_with_data)
            ''')
            
            print("数据迁移完成")
        else:
            print("新表已有数据，跳过迁移")
    except Exception as e:
        print(f"数据迁移出错: {e}")

def insert_sample_data(cursor):
    """插入示例数据"""
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM index_with_data")
    if cursor.fetchone()[0] > 0:
        print("数据库已有数据，跳过示例数据插入")
        return
    
    # 插入合并的指数数据
    index_with_data = [
        ("创业板", "399006", 2227, -21.42, 1750, 3300, 50.25, 
         "159915", "110026",
         "1700-1750 放个明牌，创业板指1700-1750之间会买入一笔 2023年12月18日",
         "小支撑位 12330",
         "第一压力位 12100; 第二压力位 13200",
         "卖出点位 1、12300；2.13500 2023年12月18日",
         "其他类致敬点位"),
        ("上证指数", "000001", 3100, -15.3, 2800, 3500, 40.0, 
         "510300", "000311",
         "2800-2850 上证指数2800-2850之间会买入一笔 2023年12月18日",
         "小支撑位 3000",
         "第一压力位 3200; 第二压力位 3400",
         "卖出点位 1、3200；2.3400 2023年12月18日",
         "其他类致敬点位"),
        ("沪深300", "000300", 3800, -18.7, 3400, 4200, 45.0, 
         "510300", "160706",
         "3400-3450 沪深300指数3400-3450之间会买入一笔 2023年12月18日",
         "小支撑位 3600",
         "第一压力位 3900; 第二压力位 4100",
         "卖出点位 1、3900；2.4100 2023年12月18日",
         "其他类致敬点位")
    ]
    
    cursor.executemany('''
    INSERT INTO index_with_data (
        name, code, current_point, change_percent, support_point, pressure_point, progress, 
        etf_code, mutual_code, support_level, normal_level, pressure_level, sell_level, other_level
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', index_with_data)
    
    # 插入历史数据
    history_data = [
        ("399006", "three_year_low", 1433, "2024-02-05", 50.2),
        ("399006", "three_year_high", 3576, "2021-07-22", -38),
        ("000001", "three_year_low", 2646, "2020-03-23", 17.1),
        ("000001", "three_year_high", 3731, "2021-02-18", -16.9),
        ("000300", "three_year_low", 3503, "2020-03-23", 8.4),
        ("000300", "three_year_high", 5930, "2021-02-18", -35.9)
    ]
    
    cursor.executemany('''
    INSERT INTO history (index_code, type, value, date, change_percent)
    VALUES (?, ?, ?, ?, ?)
    ''', history_data)
    
    print("示例数据插入完成")

if __name__ == "__main__":
    init_database()