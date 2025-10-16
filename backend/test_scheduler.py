#!/usr/bin/env python3
"""
测试定时任务功能的脚本
"""

import os
import sys
import time
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import update_all_indices_data, get_db_connection

def test_update_all_indices():
    """测试更新所有指数数据的功能"""
    print(f"开始测试更新所有指数数据... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取更新前的数据
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT code, current_point, change_percent FROM index_with_data ORDER BY code LIMIT 5')
        before_data = cursor.fetchall()
        print("更新前的数据（前5条）:")
        for row in before_data:
            print(f"  {row['code']}: 当前点位={row['current_point']}, 涨跌幅={row['change_percent']}%")
    finally:
        conn.close()
    
    # 执行更新
    print("\n执行更新...")
    result = update_all_indices_data()
    print(f"更新完成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取更新后的数据
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT code, current_point, change_percent FROM index_with_data ORDER BY code LIMIT 5')
        after_data = cursor.fetchall()
        print("\n更新后的数据（前5条）:")
        for row in after_data:
            print(f"  {row['code']}: 当前点位={row['current_point']}, 涨跌幅={row['change_percent']}%")
    finally:
        conn.close()
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_update_all_indices()