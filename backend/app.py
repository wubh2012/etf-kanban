# 标准库导入
import os
import time
import atexit
import logging
from datetime import datetime

# 第三方库导入
import sqlite3
import requests
import random
import pytz
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持

# 配置
app.config['DEBUG'] = os.getenv('FLASK_ENV', 'production') == 'development'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///etf_kanban.db')

# 设置中国时区
china_tz = pytz.timezone('Asia/Shanghai')

# User-Agent列表，用于随机选择
USER_AGENTS = [
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)', 
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)', 
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)', 
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)', 
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1', 
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6', 
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11', 
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko', 
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0', 
]

# 指数相关字段定义
INDEX_FIELDS = [
    'id', 'name', 'code', 'order_no', 'current_point', 'change_percent',
    'support_point', 'pressure_point', 'progress', 'etf_code', 'mutual_code',
    'support_level', 'normal_level', 'pressure_level', 'sell_level', 
    'other_level', 'updated_at'
]

def get_china_time():
    """获取中国时区的当前时间"""
    return datetime.now(china_tz)

def get_db_connection():
    """获取数据库连接"""
    db_path = os.path.join(os.path.dirname(__file__), 'etf_kanban.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
    return conn


def calculate_change_percent(current_point, support_point):
    """
    计算距离大支撑涨跌幅百分比
    参数:
        current_point: 当前点位
        support_point: 支撑点位
    返回:
        涨跌幅百分比
    """
    if current_point is None or support_point is None or support_point == 0:
        return None
    
    change_percent = ((current_point - support_point) / support_point) * 100
    return round(change_percent, 2)

def update_history_data(conn, index_code, current_point):
    """
    更新历史数据表，检查当前点位是否突破历史最高点或最低点
    参数:
        conn: 数据库连接
        index_code: 指数代码
        current_point: 当前点位
    """
    try:
        # 获取历史最高点和最低点
        cursor = conn.execute('SELECT type, value FROM history WHERE index_code = ?', (index_code,))
        history_data = {row['type']: row['value'] for row in cursor.fetchall()}
        
        current_date = get_china_time().strftime('%Y-%m-%d')
        
        # 检查是否突破历史最高点
        if 'three_year_high' in history_data:
            if current_point > history_data['three_year_high']:
                # 计算从最高点下跌的幅度
                change_percent = ((current_point - history_data['three_year_high']) / history_data['three_year_high']) * 100
                # 更新历史最高点
                conn.execute('''
                UPDATE history 
                SET value = ?, date = ?, change_percent = ?, updated_at = ?
                WHERE index_code = ? AND type = 'three_year_high'
                ''', (current_point, current_date, round(change_percent, 2), get_china_time().strftime('%Y-%m-%d %H:%M:%S'), index_code))
                logger.info(f"指数 {index_code} 突破历史最高点，更新为 {current_point}")
        else:
            # 如果没有历史最高点记录，则创建一个
            conn.execute('''
            INSERT INTO history (index_code, type, value, date, change_percent)
            VALUES (?, 'three_year_high', ?, ?, 0)
            ''', (index_code, current_point, current_date))
        
        # 检查是否突破历史最低点
        if 'three_year_low' in history_data:
            if current_point < history_data['three_year_low']:
                # 计算从最低点上涨的幅度
                change_percent = ((current_point - history_data['three_year_low']) / history_data['three_year_low']) * 100
                # 更新历史最低点
                conn.execute('''
                UPDATE history 
                SET value = ?, date = ?, change_percent = ?, updated_at = ?
                WHERE index_code = ? AND type = 'three_year_low'
                ''', (current_point, current_date, round(change_percent, 2), get_china_time().strftime('%Y-%m-%d %H:%M:%S'), index_code))
                logger.info(f"指数 {index_code} 突破历史最低点，更新为 {current_point}")
        else:
            # 如果没有历史最低点记录，则创建一个
            conn.execute('''
            INSERT INTO history (index_code, type, value, date, change_percent)
            VALUES (?, 'three_year_low', ?, ?, 0)
            ''', (index_code, current_point, current_date))
            
    except Exception as e:
        logger.error(f"更新指数 {index_code} 历史数据失败: {str(e)}")

def update_index_realtime_data(index_code):
    """
    更新指定指数的实时数据
    参数:
        index_code: 指数代码
    返回:
        更新是否成功
    """
    # 获取实时数据
    realtime_data = get_realtime_index_data(index_code)
    
    if realtime_data and realtime_data['success']:
        conn = get_db_connection()
        try:
            # 获取支撑点位
            cursor = conn.execute('SELECT support_point FROM index_with_data WHERE code = ?', (index_code,))
            row = cursor.fetchone()
            
            if row is None:
                logger.error(f"未找到指数 {index_code} 的支撑点位")
                return False
                
            support_point = row['support_point']
            current_point = realtime_data['current_point']
            
            # 计算涨跌幅百分比
            # change_percent = calculate_change_percent(current_point, support_point)
            
            # 更新数据库中的当前点位和涨跌幅
            conn.execute('''
            UPDATE index_with_data 
            SET current_point = ?, change_percent = ?, updated_at = ?
            WHERE code = ?
            ''', (current_point, change_percent, get_china_time().strftime('%Y-%m-%d %H:%M:%S'), index_code))
            
            # 更新历史数据表
            # update_history_data(conn, index_code, current_point)
            
            conn.commit()
            logger.info(f"成功更新指数 {index_code} 的实时数据: 当前点位={current_point}, 涨跌幅={change_percent}%")
            return True
            
        except Exception as e:
            logger.error(f"更新指数 {index_code} 数据库记录失败: {str(e)}")
            return False
        finally:
            conn.close()
    
    return False

def update_all_indices_data():
    """
    更新所有指数的实时数据
    """
    logger.info("开始定时更新所有指数数据...")
    
    conn = get_db_connection()
    try:
        # 获取所有指数代码
        cursor = conn.execute('SELECT code FROM index_with_data')
        index_codes = [row['code'] for row in cursor.fetchall()]
        
        success_count = 0
        total_count = len(index_codes)
        
        # 更新每个指数的数据
        for index_code in index_codes:
            
            # 随机等待1-5秒钟，避免请求太频繁
            time.sleep(random.uniform(3, 10))
            if update_index_realtime_data(index_code):
                success_count += 1
        
        logger.info(f"定时更新完成: 成功更新 {success_count}/{total_count} 个指数数据")
        
    except Exception as e:
        logger.error(f"定时更新所有指数数据失败: {str(e)}")
    finally:
        conn.close()

def start_scheduler():
    """
    启动定时任务调度器
    """
    # 从环境变量获取配置
    scheduler_enabled = os.getenv('SCHEDULER_ENABLED', 'false').lower() == 'true'
    update_interval = int(os.getenv('UPDATE_INTERVAL_MINUTES', '10'))
    
    if not scheduler_enabled:
        logger.info("定时任务已禁用")
        return
    
    logger.info(f"启动定时任务调度器，更新间隔: {update_interval} 分钟")
    
    scheduler = BackgroundScheduler()
    
    # 添加定时任务，每隔指定分钟执行一次
    scheduler.add_job(
        func=update_all_indices_data,
        trigger=IntervalTrigger(minutes=update_interval),
        id='update_indices_data',
        name='更新所有指数数据',
        replace_existing=True
    )
    
    # 启动调度器
    scheduler.start()
    
    # 注册退出函数，确保应用退出时关闭调度器
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler

def get_code_prefix(stock_code):
    """
    根据股票代码判断交易所前缀（sz或sh）
    :param stock_code: 股票代码（字符串，如"399006"、"600000"）
    :return: 交易所前缀"sz"或"sh"
    """
    if not stock_code or len(stock_code) < 3:
        return None  # 无效代码
    
    # 取前3位判断
    prefix = stock_code[:3]
    # 特殊代码判断
    if stock_code.upper().startswith('HS'):
        return "hk"
    if stock_code.upper() == '00700':
        return "r_hk"
    # 深圳交易所规则
    if prefix in ["395", "399"]:
        return "sz"
    # 上海交易所规则
    elif prefix in ["000", "001"]:
        return "s_sh"
    else:
        return "s_sh"  # 无法识别

@app.route('/get/indexdata/<index_code>', methods=['GET'])
def get_realtime_index_data(index_code):
    """
    根据指数代码使用不同API获取实时数据
    对于H30533、GDAXI、HSHCI使用东方财富API，其他使用腾讯财经API
    """
    try:
        # 特殊指数使用东方财富API
        if index_code.upper() in ['H30533', 'GDAXI', 'HSHCI']:
            return get_realtime_index_data_eastmoney(index_code)
        
        # 其他指数使用腾讯财经API
        # 尝试使用腾讯财经API
        prefix = get_code_prefix(index_code)
        url = f"http://qt.gtimg.cn/q={prefix}{index_code}"
        
        # 上证：
        # http://qt.gtimg.cn/q=sh000001
        # 深圳：
        # http://qt.gtimg.cn/q=sz399006
        # 港股指数：
        # http://qt.gtimg.cn/q=hkHSTECH
        # 港股股票：
        # http://qt.gtimg.cn/q=r_hk00700
        # 美股股票
        # http://qt.gtimg.cn/q=r_usAAPL

        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'http://finance.qq.com',
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.encoding = 'gbk'
        logger.info(f"指数 {index_code} API返回: {response.text}")
        if response.status_code == 200 and response.text.startswith('v_'):
            data_part = response.text.split('"')[1]
            data_items = data_part.split('~')
            
            if len(data_items) >= 4 and data_items[3] and data_items[4]:
                current_point = float(data_items[3])
                logger.info(f"指数 {index_code} 当前点位: {current_point}")
                return {
                    'current_point': current_point,
                    'success': True
                }
        
        return None
    except Exception as e:
        logger.error(f"API获取指数 {index_code} 数据异常: {str(e)}")
        return None


def get_realtime_index_data_eastmoney(index_code):
    """
    使用东方财富API获取指数数据
    参数:
        index_code: 指数代码 (H30533, GDAXI, HSHCI等)
    返回:
        包含当前点位和成功状态的字典
    """
    try:
        # 构造东方财富API的secid参数
        secid_map = {
            'H30533': '2.H30533',  # 需要确认实际的secid映射
            'GDAXI': '100.GDAXI',    # 德国DAX指数
            'HSHCI': '124.HSHCI'     # 恒生医疗保健指数
        }
        
        # 获取secid，如果不在映射中则使用默认格式
        secid = secid_map.get(index_code.upper(), f'124.{index_code}')
        
        # 构造API URL
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f57,f58,f169,f170"
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://quote.eastmoney.com/',
        }
        
        response = requests.get(url, timeout=10, headers=headers)
        response.encoding = 'utf-8'
        logger.info(f"东方财富API返回 {index_code}: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查返回数据是否成功
            if data.get('rc') == 0 and data.get('data'):
                # f43字段是最新的点位，需要除以100
                current_point = float(data['data']['f43']) / 100
                logger.info(f"指数 {index_code} 当前点位: {current_point}")
                return {
                    'current_point': current_point,
                    'success': True
                }
        
        return None
    except Exception as e:
        logger.error(f"东方财富API获取指数 {index_code} 数据异常: {str(e)}")
        return None
        
@app.route('/', methods=['GET'])
def home():
    """首页"""
    return jsonify({'status': 'healthy'})


# 通用的数据库行转字典函数
def row_to_dict(row, fields):
    """将数据库行转换为指定字段的字典"""
    return {field: row[field] for field in fields if field in row}



@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """获取看板数据"""
    # 检查是否需要获取实时数据
    refresh_realtime = request.args.get('refresh', 'false').lower() == 'true'
    # logger.info(f"get_dashboard_data 请求参数: {request.args.get('refresh')}")

    conn = get_db_connection()
    
    try:
        # 获取所有指数数据（从合并表中）
        index_cursor = conn.execute('SELECT * FROM index_with_data ORDER BY order_no')
        index_rows = index_cursor.fetchall()
        
        # 构建数据数组
        data_array = []
        
        for index_row in index_rows:
            index_code = index_row['code']
            
            # 如果需要获取实时数据，尝试更新当前指数的数据
            current_point = index_row['current_point']
            change_percent = index_row['change_percent']
            
            if refresh_realtime:
                realtime_data = get_realtime_index_data(index_code)
                if realtime_data and realtime_data['success']:
                    current_point = realtime_data['current_point']
                    
            
            # 指数数据
            indices = {
                'name': index_row['name'],
                'code': index_code,
                'current_point': current_point,
                'change_percent': change_percent,
                'support_point': index_row['support_point'],
                'pressure_point': index_row['pressure_point'],
                'progress': index_row['progress'],
                'updated_at': index_row['updated_at']
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
            'data': data_array,
            'realtime_data': refresh_realtime
        }
        
        return jsonify(response)
    
    finally:
        conn.close()

@app.route('/api/indices', methods=['GET'])
def get_indices():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM index_with_data ORDER BY order_no ASC")
    indices = cursor.fetchall()
    conn.close()
    
    # 将 Row 对象列表直接转换为字典列表
    indices_list = [dict(row) for row in indices]
    
    logger.info(f"=== 总共返回 {len(indices)} 条记录 ===")
    return jsonify(indices_list)

@app.route('/api/indices/<index_code>', methods=['GET'])
def get_index(index_code):
    """获取特定指数数据"""
    conn = get_db_connection()
    
    try:
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': '指数信息未找到'}), 404
        
        # 定义需要返回的字段列表
        fields = [
            'id', 'name', 'code', 'order_no', 'current_point', 'change_percent',
            'support_point', 'pressure_point', 'progress', 'etf_code', 'mutual_code',
            'support_level', 'normal_level', 'pressure_level', 'sell_level', 
            'other_level', 'updated_at'
        ]
        
        # 使用字典推导式构建返回数据
        index_data = {field: row[field] for field in fields if field in row}
        
        return jsonify(index_data)
    
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
        
        # 如果没有指定排序，则设置为最大排序值+1
        if 'order_no' not in data:
            cursor = conn.execute('SELECT MAX(order_no) FROM index_with_data')
            max_sort = cursor.fetchone()[0] or 0
            data['order_no'] = max_sort + 1
        
        # 插入新指数（包含核心数据字段）
        cursor = conn.execute('''
        INSERT INTO index_with_data (
            name, code, order_no, current_point, change_percent, support_point, pressure_point, progress,
            etf_code, mutual_code, support_level, normal_level, pressure_level, sell_level, other_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['code'],
            data.get('order_no'),
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
        
        return jsonify(row_to_dict(row, INDEX_FIELDS)), 201
    
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
        
        # 使用字段列表和循环来构建更新语句
        for field in INDEX_FIELDS:
            if field in data:
                if field == 'updated_at':
                    update_fields.append(f'{field} = ?')
                    update_values.append(get_china_time().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    update_fields.append(f'{field} = ?')
                    update_values.append(data[field])
            
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(index_code)
        
        sql = f'''
        UPDATE index_with_data SET {', '.join(update_fields)}
        WHERE code = ?
        '''
        logger.info(f"执行的SQL语句: {sql}, 参数: {update_values}")
        conn.execute(sql, update_values)
        
        conn.commit()
        
        # 返回更新后的指数数据
        cursor = conn.execute('SELECT * FROM index_with_data WHERE code = ?', (index_code,))
        row = cursor.fetchone()
        
        return jsonify(row_to_dict(row, INDEX_FIELDS))
    
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
        
        # 打印待执行的SQL语句
        sql = f'''
        UPDATE history SET {', '.join(update_fields)}, updated_at = ?
        WHERE index_code = ? AND type = ?
        '''
        # 正确的参数顺序：先是要更新的字段值，然后是updated_at时间戳，最后是WHERE条件的参数
        params = update_values + [get_china_time().strftime('%Y-%m-%d %H:%M:%S'), index_code, history_type]
        print(f"执行的SQL语句: {sql}")
        print(f"参数: {params}")
        conn.execute(sql, params)
        
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

@app.route('/api/update-all-indices', methods=['POST'])
def trigger_update_all_indices():
    """手动触发更新所有指数数据的定时任务"""
    try:
        update_all_indices_data()
        return jsonify({'status': 'success', 'message': '已触发更新所有指数数据'})
    except Exception as e:
        logger.error(f"手动触发更新所有指数数据失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 数据库初始化
from database import init_database

# 启动应用
if __name__ == '__main__':
    # 检查数据库文件是否存在，如果不存在才初始化数据库
    db_path = os.path.join(os.path.dirname(__file__), 'etf_kanban.db')
    if not os.path.exists(db_path):
        print("数据库文件不存在，开始初始化数据库...")
        init_database()
    else:
        print("数据库文件已存在，跳过初始化")
    
    # 启动定时任务调度器
    scheduler = start_scheduler()
    
    # 启动Flask服务器
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)