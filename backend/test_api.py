#!/usr/bin/env python3
"""
API测试脚本
用于验证后端API接口是否正常工作
"""

import requests
import json
import sys

def test_api(base_url="http://localhost:5000"):
    """测试API接口"""
    
    # 测试健康检查接口
    print("测试健康检查接口...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✓ 健康检查接口正常")
            print(f"  响应: {response.json()}")
        else:
            print(f"✗ 健康检查接口异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 健康检查接口请求失败: {e}")
        return False
    
    # 测试看板数据接口
    print("\n测试看板数据接口...")
    try:
        response = requests.get(f"{base_url}/api/dashboard")
        if response.status_code == 200:
            print("✓ 看板数据接口正常")
            data = response.json()
            
            # 检查数据结构
            required_keys = ['timestamp', 'indices', 'core_data', 'history']
            for key in required_keys:
                if key not in data:
                    print(f"✗ 看板数据缺少必要字段: {key}")
                    return False
            
            print(f"  时间戳: {data['timestamp']}")
            print(f"  指数数量: {len(data['indices'])}")
            print(f"  核心数据数量: {len(data['core_data'])}")
            print(f"  历史数据数量: {len(data['history'])}")
            
            # 打印第一个指数的信息
            if data['indices']:
                index = data['indices'][0]
                print(f"  第一个指数: {index['name']} ({index['code']}) - {index['current_point']}")
        else:
            print(f"✗ 看板数据接口异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 看板数据接口请求失败: {e}")
        return False
    
    # 测试指数列表接口
    print("\n测试指数列表接口...")
    try:
        response = requests.get(f"{base_url}/api/indices")
        if response.status_code == 200:
            print("✓ 指数列表接口正常")
            indices = response.json()
            print(f"  指数数量: {len(indices)}")
        else:
            print(f"✗ 指数列表接口异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 指数列表接口请求失败: {e}")
        return False
    
    print("\n所有API接口测试通过!")
    return True

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    success = test_api(base_url)
    sys.exit(0 if success else 1)