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
        # 获取所有指数数据（从合并表中）
        index_cursor = conn.execute('SELECT * FROM index_with_data ORDER BY id')
        index_rows = index_cursor.fetchall()
        
        # 构建数据数组
        data_array = []
        
        for index_row in index_rows:
            index_code = index_row['code']
            
            # 指数数据
            indices = {
                'name': index_row['name'],
                'code': index_code,
                'current_point': index_row['current_point'],
                'change_percent': index_row['change_percent'],
                'support_point': index_row['support_point'],
                'pressure_point': index_row['pressure_point'],
                'progress': index_row['progress']
            }
            
            # 核心数据（现在直接从同一张表获取）
            core_data = {
                'etf_code': index_row['etf_code'],
                'mutual_code': index_row['mutual_code'],
                'support_level': index_row['support_level'],
                'normal_level': index_row['normal_level'],
                'pressure_level': index_row['pressure_level'],
                'sell_level': index_row['sell_level'],
                'other_level': index_row['other_level']
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
        index_cursor = conn.execute('SELECT * FROM index_with_data ORDER BY id')
        indices = []
        for row in index_cursor:
            indices.append({
                'id': row['id'],
                'name': row['name'],
                'code': row['code'],
                'current_point': row['current_point'],
                'change_percent': row['change_percent'],
                'support_point': row['support_point'],
                'pressure_point': row['pressure_point'],
                'progress': row['progress'],
                'etf_code': row['etf_code'],
                'mutual_code': row['mutual_code'],
                'support_level': row['support_level'],
                'normal_level': row['normal_level'],
                'pressure_level': row['pressure_level'],
                'sell_level': row['sell_level'],
                'other_level': row['other_level'],
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
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
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
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level'],
            'updated_at': row['updated_at']
        }
        
        return jsonify(index_data)
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/core_data', methods=['GET'])
def get_index_core_data(index_code):
    """获取特定指数的核心数据（保持向后兼容的API端点）"""
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Index not found'}), 404
        
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

# 数据维护相关API
@app.route('/api/indices', methods=['POST'])
def create_index():
    """创建新指数（包含核心数据）"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('code'):
        return jsonify({'error': 'Name and code are required'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查指数代码是否已存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (data['code'],))
        if cursor.fetchone() is not None:
            return jsonify({'error': 'Index code already exists'}), 400
        
        # 插入新指数（包含核心数据字段）
        cursor = conn.execute('''
        INSERT INTO index_with_data (
            name, code, current_point, change_percent, support_point, pressure_point, progress,
            etf_code, mutual_code, support_level, normal_level, pressure_level, sell_level, other_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['code'],
            data.get('current_point'),
            data.get('change_percent'),
            data.get('support_point'),
            data.get('pressure_point'),
            data.get('progress'),
            data.get('etf_code'),
            data.get('mutual_code'),
            data.get('support_level'),
            data.get('normal_level'),
            data.get('pressure_level'),
            data.get('sell_level'),
            data.get('other_level')
        ))
        
        index_id = cursor.lastrowid
        conn.commit()
        
        # 返回创建的指数数据
        cursor = conn.execute('SELECT * FROM index_with_data WHERE id = ?', (index_id,))
        row = cursor.fetchone()
        
        return jsonify({
            'id': row['id'],
            'name': row['name'],
            'code': row['code'],
            'current_point': row['current_point'],
            'change_percent': row['change_percent'],
            'support_point': row['support_point'],
            'pressure_point': row['pressure_point'],
            'progress': row['progress'],
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level'],
            'updated_at': row['updated_at']
        }), 201
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>', methods=['PUT'])
def update_index(index_code):
    """更新指数数据（包含核心数据）"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 更新指数数据（包含核心数据字段）
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append('name = ?')
            update_values.append(data['name'])
        
        if 'current_point' in data:
            update_fields.append('current_point = ?')
            update_values.append(data['current_point'])
        
        if 'change_percent' in data:
            update_fields.append('change_percent = ?')
            update_values.append(data['change_percent'])
        
        if 'support_point' in data:
            update_fields.append('support_point = ?')
            update_values.append(data['support_point'])
        
        if 'pressure_point' in data:
            update_fields.append('pressure_point = ?')
            update_values.append(data['pressure_point'])
        
        if 'progress' in data:
            update_fields.append('progress = ?')
            update_values.append(data['progress'])
        
        if 'etf_code' in data:
            update_fields.append('etf_code = ?')
            update_values.append(data['etf_code'])
        
        if 'mutual_code' in data:
            update_fields.append('mutual_code = ?')
            update_values.append(data['mutual_code'])
        
        if 'support_level' in data:
            update_fields.append('support_level = ?')
            update_values.append(data['support_level'])
        
        if 'normal_level' in data:
            update_fields.append('normal_level = ?')
            update_values.append(data['normal_level'])
        
        if 'pressure_level' in data:
            update_fields.append('pressure_level = ?')
            update_values.append(data['pressure_level'])
        
        if 'sell_level' in data:
            update_fields.append('sell_level = ?')
            update_values.append(data['sell_level'])
        
        if 'other_level' in data:
            update_fields.append('other_level = ?')
            update_values.append(data['other_level'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(index_code)
        
        conn.execute(f'''
        UPDATE index_with_data SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
        WHERE code = ?
        ''', update_values)
        
        conn.commit()
        
        # 返回更新后的指数数据
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        return jsonify({
            'id': row['id'],
            'name': row['name'],
            'code': row['code'],
            'current_point': row['current_point'],
            'change_percent': row['change_percent'],
            'support_point': row['support_point'],
            'pressure_point': row['pressure_point'],
            'progress': row['progress'],
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level'],
            'updated_at': row['updated_at']
        })
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>', methods=['DELETE'])
def delete_index(index_code):
    """删除指数及其相关数据"""
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 删除相关数据（由于外键约束，需要先删除子表数据）
        conn.execute('DELETE FROM history WHERE index_code = ?', (index_code,))
        conn.execute('DELETE FROM index_with_data WHERE code = ?', (index_code,))
        
        conn.commit()
        
        return jsonify({'message': 'Index deleted successfully'})
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/core_data', methods=['POST'])
def create_core_data(index_code):
    """创建指数的核心数据（保持向后兼容的API端点）"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 更新指数记录中的核心数据字段
        update_fields = []
        update_values = []
        
        if 'etf_code' in data:
            update_fields.append('etf_code = ?')
            update_values.append(data['etf_code'])
        
        if 'mutual_code' in data:
            update_fields.append('mutual_code = ?')
            update_values.append(data['mutual_code'])
        
        if 'support_level' in data:
            update_fields.append('support_level = ?')
            update_values.append(data['support_level'])
        
        if 'normal_level' in data:
            update_fields.append('normal_level = ?')
            update_values.append(data['normal_level'])
        
        if 'pressure_level' in data:
            update_fields.append('pressure_level = ?')
            update_values.append(data['pressure_level'])
        
        if 'sell_level' in data:
            update_fields.append('sell_level = ?')
            update_values.append(data['sell_level'])
        
        if 'other_level' in data:
            update_fields.append('other_level = ?')
            update_values.append(data['other_level'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(index_code)
        
        conn.execute(f'''
        UPDATE index_with_data SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
        WHERE code = ?
        ''', update_values)
        
        conn.commit()
        
        # 返回更新后的核心数据
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        return jsonify({
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level']
        }), 201
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/core_data', methods=['PUT'])
def update_core_data(index_code):
    """更新指数的核心数据（保持向后兼容的API端点）"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 更新指数记录中的核心数据字段
        update_fields = []
        update_values = []
        
        if 'etf_code' in data:
            update_fields.append('etf_code = ?')
            update_values.append(data['etf_code'])
        
        if 'mutual_code' in data:
            update_fields.append('mutual_code = ?')
            update_values.append(data['mutual_code'])
        
        if 'support_level' in data:
            update_fields.append('support_level = ?')
            update_values.append(data['support_level'])
        
        if 'normal_level' in data:
            update_fields.append('normal_level = ?')
            update_values.append(data['normal_level'])
        
        if 'pressure_level' in data:
            update_fields.append('pressure_level = ?')
            update_values.append(data['pressure_level'])
        
        if 'sell_level' in data:
            update_fields.append('sell_level = ?')
            update_values.append(data['sell_level'])
        
        if 'other_level' in data:
            update_fields.append('other_level = ?')
            update_values.append(data['other_level'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(index_code)
        
        conn.execute(f'''
        UPDATE index_with_data SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
        WHERE code = ?
        ''', update_values)
        
        conn.commit()
        
        # 返回更新后的核心数据
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        return jsonify({
            'etf_code': row['etf_code'],
            'mutual_code': row['mutual_code'],
            'support_level': row['support_level'],
            'normal_level': row['normal_level'],
            'pressure_level': row['pressure_level'],
            'sell_level': row['sell_level'],
            'other_level': row['other_level']
        })
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/core_data', methods=['DELETE'])
def delete_core_data(index_code):
    """删除指数的核心数据（将核心数据字段置空）"""
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 将核心数据字段置空
        conn.execute('''
        UPDATE index_with_data 
        SET 
            etf_code = NULL,
            mutual_code = NULL,
            support_level = NULL,
            normal_level = NULL,
            pressure_level = NULL,
            sell_level = NULL,
            other_level = NULL,
            updated_at = CURRENT_TIMESTAMP
        WHERE code = ?
        ''', (index_code,))
        
        conn.commit()
        
        return jsonify({'message': 'Core data deleted successfully'})
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/history', methods=['POST'])
def create_history(index_code):
    """创建指数的历史数据"""
    data = request.get_json()
    
    if not data or not data.get('type') or not data.get('value'):
        return jsonify({'error': 'Type and value are required'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查指数是否存在（使用合并表）
        cursor = conn.execute('SELECT id FROM index_with_data WHERE code = ?', (index_code,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Index not found'}), 404
        
        # 检查是否已有相同类型的历史数据
        cursor = conn.execute('SELECT id FROM history WHERE index_code = ? AND type = ?', (index_code, data['type']))
        if cursor.fetchone() is not None:
            return jsonify({'error': f'History data of type {data["type"]} already exists'}), 400
        
        # 插入历史数据
        conn.execute('''
        INSERT INTO history (index_code, type, value, date, change_percent)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            index_code,
            data['type'],
            data['value'],
            data.get('date'),
            data.get('change_percent')
        ))
        
        conn.commit()
        
        # 返回创建的历史数据
        cursor = conn.execute('SELECT * FROM history WHERE index_code = ? AND type = ?', (index_code, data['type']))
        row = cursor.fetchone()
        
        return jsonify({
            'type': row['type'],
            'value': row['value'],
            'date': row['date'],
            'change_percent': row['change_percent']
        }), 201
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/history/<history_type>', methods=['PUT'])
def update_history(index_code, history_type):
    """更新指数的历史数据"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db_connection()
    
    try:
        # 检查历史数据是否存在
        cursor = conn.execute('SELECT id FROM history WHERE index_code = ? AND type = ?', (index_code, history_type))
        if cursor.fetchone() is None:
            return jsonify({'error': 'History data not found'}), 404
        
        # 更新历史数据
        update_fields = []
        update_values = []
        
        if 'value' in data:
            update_fields.append('value = ?')
            update_values.append(data['value'])
        
        if 'date' in data:
            update_fields.append('date = ?')
            update_values.append(data['date'])
        
        if 'change_percent' in data:
            update_fields.append('change_percent = ?')
            update_values.append(data['change_percent'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(index_code)
        update_values.append(history_type)
        
        conn.execute(f'''
        UPDATE history SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
        WHERE index_code = ? AND type = ?
        ''', update_values)
        
        conn.commit()
        
        # 返回更新后的历史数据
        cursor = conn.execute('SELECT * FROM history WHERE index_code = ? AND type = ?', (index_code, history_type))
        row = cursor.fetchone()
        
        return jsonify({
            'type': row['type'],
            'value': row['value'],
            'date': row['date'],
            'change_percent': row['change_percent']
        })
    
    finally:
        conn.close()

@app.route('/api/indices/<index_code>/history/<history_type>', methods=['DELETE'])
def delete_history(index_code, history_type):
    """删除指数的历史数据"""
    conn = get_db_connection()
    
    try:
        # 检查历史数据是否存在
        cursor = conn.execute('SELECT id FROM history WHERE index_code = ? AND type = ?', (index_code, history_type))
        if cursor.fetchone() is None:
            return jsonify({'error': 'History data not found'}), 404
        
        # 删除历史数据
        conn.execute('DELETE FROM history WHERE index_code = ? AND type = ?', (index_code, history_type))
        
        conn.commit()
        
        return jsonify({'message': 'History data deleted successfully'})
    
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    try:
        conn = get_db_connection()
        cursor = conn.execute('SELECT 1')
        cursor.fetchone()
        conn.close()
        return jsonify({'status': 'healthy'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# 数据库初始化
from database import init_database

# 启动应用
if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 启动Flask服务器
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)