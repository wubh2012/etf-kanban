import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置
app.config['DEBUG'] = os.getenv('FLASK_ENV', 'production') == 'development'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///etf_kanban.db')

def get_db_connection():
    """获取数据库连接"""
    db_path = os.path.join(os.path.dirname(__file__), 'etf_kanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
    return conn

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """获取看板数据"""
    conn = get_db_connection()
    
    try:
        # 获取所有指数代码
        indices_cursor = conn.execute('SELECT code FROM indices ORDER BY id')
        index_codes = [row['code'] for row in indices_cursor]
        
        # 构建数据数组
        data_array = []
        
        for index_code in index_codes:
            # 获取指数数据
            cursor = conn.execute('SELECT * FROM indices WHERE code = ?', (index_code,))
            index_row = cursor.fetchone()
            
            if index_row is None:
                continue
                
            indices = {
                'name': index_row['name'],
                'code': index_row['code'],
                'current_point': index_row['current_point'],
                'change_percent': index_row['change_percent'],
                'support_point': index_row['support_point'],
                'pressure_point': index_row['pressure_point'],
                'progress': index_row['progress']
            }
            
            # 获取核心数据
            cursor = conn.execute('SELECT * FROM core_data WHERE index_code = ?', (index_code,))
            core_row = cursor.fetchone()
            
            core_data = {}
            if core_row is not None:
                core_data = {
                    'etf_code': core_row['etf_code'],
                    'mutual_code': core_row['mutual_code'],
                    'support_level': core_row['support_level'],
                    'normal_level': core_row['normal_level'],
                    'pressure_level': core_row['pressure_level'],
                    'sell_level': core_row['sell_level'],
                    'other_level': core_row['other_level']
                }
            
            # 获取历史数据
            history_cursor = conn.execute('SELECT * FROM history WHERE index_code = ?', (index_code,))
            history_rows = history_cursor.fetchall()
            
            history = {}
            for row in history_rows:
                if row['type'] == 'three_year_low':
                    history['three_year_low'] = {
                        'value': row['value'],
                        'date': row['date'],
                        'rise_from_low': row['change_percent']
                    }
                elif row['type'] == 'three_year_high':
                    history['three_year_high'] = {
                        'value': row['value'],
                        'date': row['date'],
                        'drop_from_high': row['change_percent']
                    }
            
            # 添加到数据数组
            data_array.append({
                'indices': indices,
                'core_data': core_data,
                'history': history
            })
        
        # 构建响应数据
        response = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': data_array
        }
        
        return jsonify(response)
    
    finally:
        conn.close()

@app.route('/api/indices', methods=['GET'])
def get_indices():
    """获取所有指数数据"""
    conn = get_db_connection()
    
    try:
        indices_cursor = conn.execute('SELECT * FROM indices ORDER BY id')
        indices = []
        for row in indices_cursor:
            indices.append({
                'id': row['id'],
                'name': row['name'],
                'code': row['code'],
                'current_point': row['current_point'],
                'change_percent': row['change_percent'],
                'support_point': row['support_point'],
                'pressure_point': row['pressure_point'],
                'progress': row['progress'],
                'updated_at': row['updated_at']
            })
        
        return jsonify(indices)
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>', methods=['GET'])
def get_index(index_code):
    """获取特定指数数据"""
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('SELECT * FROM indices WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Index not found'}), 404
        
        index_data = {
            'id': row['id'],
            'name': row['name'],
            'code': row['code'],
            'current_point': row['current_point'],
            'change_percent': row['change_percent'],
            'support_point': row['support_point'],
            'pressure_point': row['pressure_point'],
            'progress': row['progress'],
            'updated_at': row['updated_at']
        }
        
        return jsonify(index_data)
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/core_data', methods=['GET'])
def get_index_core_data(index_code):
    """获取特定指数的核心数据"""
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('SELECT * FROM core_data WHERE index_code = ?', (index_code,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Core data not found'}), 404
        
        core_data = {
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level']
        }
        
        return jsonify(core_data)
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/history', methods=['GET'])
def get_index_history(index_code):
    """获取特定指数的历史数据"""
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('SELECT * FROM history WHERE index_code = ?', (index_code,))
        rows = cursor.fetchall()
        
        if not rows:
            return jsonify({'error': 'History data not found'}), 404
        
        history = {}
        for row in rows:
            history[row['type']] = {
                'value': row['value'],
                'date': row['date'],
                'change_percent': row['change_percent']
            }
        
        return jsonify(history)
    
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# 初始化数据库
def init_db():
    """初始化数据库"""
    from database import init_database
    init_database()

if __name__ == '__main__':
    # 确保数据库已初始化
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'etf_kanban.db')):
        init_db()
    
    # 启动Flask应用
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    app.run(host=host, port=port, debug=app.config['DEBUG'])