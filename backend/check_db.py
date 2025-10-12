import sqlite3
import os

# 连接数据库
db_path = os.path.join(os.path.dirname(__file__), 'etf_kanban.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查index_with_data表结构
print('检查index_with_data表结构:')
cursor.execute('PRAGMA table_info(index_with_data)')
for row in cursor.fetchall():
    print(row)

# 检查示例数据
print('\n检查示例数据:')
cursor.execute('SELECT name, code, etf_code FROM index_with_data LIMIT 3')
for row in cursor.fetchall():
    print(row)

# 关闭连接
conn.close()