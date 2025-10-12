# 金融数据看板部署指南

本文档提供了金融数据看板应用的详细部署和使用说明。

## 目录

1. [系统要求](#系统要求)
2. [快速部署](#快速部署)
3. [手动部署](#手动部署)
4. [开发环境设置](#开发环境设置)
5. [API接口文档](#api接口文档)
6. [常见问题](#常见问题)

## 系统要求

- Docker 20.10+
- Docker Compose 1.29+
- 至少2GB可用内存
- 至少1GB可用磁盘空间

## 快速部署

### 使用启动脚本

#### Windows用户

1. 双击运行 `start.bat` 文件
2. 等待脚本执行完成
3. 在浏览器中访问 `http://localhost:5000`

#### Linux/Mac用户

1. 在终端中运行：
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
2. 等待脚本执行完成
3. 在浏览器中访问 `http://localhost:5000`

### 使用Docker Compose

1. 确保Docker和Docker Compose已安装
2. 在项目根目录运行：
   ```bash
   docker-compose up --build -d
   ```
3. 在浏览器中访问 `http://localhost:5000`

## 手动部署

### 后端部署

1. 进入后端目录：
   ```bash
   cd backend
   ```

2. 创建Python虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 初始化数据库：
   ```bash
   python database.py
   ```

5. 启动后端服务：
   ```bash
   python app.py
   ```

### 前端部署

1. 进入前端目录：
   ```bash
   cd frontend
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动开发服务器：
   ```bash
   npm run serve
   ```

4. 或构建生产版本：
   ```bash
   npm run build
   ```

## 开发环境设置

### 后端开发

1. 安装Python 3.9+
2. 安装依赖：`pip install -r requirements.txt`
3. 复制环境变量文件：`cp .env.example .env`
4. 根据需要修改`.env`文件中的配置
5. 初始化数据库：`python database.py`
6. 启动开发服务器：`python app.py`

### 前端开发

1. 安装Node.js 16+
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm run serve`
4. 访问 `http://localhost:8080`

## API接口文档

### 健康检查

- **URL**: `/api/health`
- **方法**: GET
- **响应示例**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-10-11 22:30:00"
  }
  ```

### 获取看板数据

- **URL**: `/api/dashboard`
- **方法**: GET
- **响应示例**:
  ```json
  {
    "timestamp": "2025-10-11 22:30:00",
    "indices": [
      {
        "id": 1,
        "name": "创业板",
        "code": "399006",
        "current_point": 2227,
        "change_percent": -21.42,
        "support_point": 1750,
        "pressure_point": 3300,
        "progress": 50.25,
        "updated_at": "2025-10-11 22:30:00"
      }
    ],
    "core_data": {
      "399006": {
        "etf_code": "159915",
        "mutual_code": "110026",
        "support_level": "1700-1750 放个明牌，创业板指1700-1750之间会买入一笔 2023年12月18日",
        "normal_level": "小支撑位 12330",
        "pressure_level": "第一压力位 12100; 第二压力位 13200",
        "sell_level": "卖出点位 1、12300；2.13500 2023年12月18日",
        "other_level": "其他类致敬点位"
      }
    },
    "history": {
      "399006": {
        "three_year_low": {
          "value": 1433,
          "date": "2024-02-05",
          "change_percent": 50.2
        },
        "three_year_high": {
          "value": 3576,
          "date": "2021-07-22",
          "change_percent": -38
        }
      }
    }
  }
  ```

### 获取指数列表

- **URL**: `/api/indices`
- **方法**: GET
- **响应示例**: 看板数据接口中的indices数组

### 获取特定指数数据

- **URL**: `/api/indices/<index_code>`
- **方法**: GET
- **参数**: 
  - `index_code`: 指数代码，如"399006"
- **响应示例**: 看板数据接口中特定指数的数据

### 获取特定指数的核心数据

- **URL**: `/api/indices/<index_code>/core_data`
- **方法**: GET
- **参数**: 
  - `index_code`: 指数代码，如"399006"
- **响应示例**: 看板数据接口中特定指数的核心数据

### 获取特定指数的历史数据

- **URL**: `/api/indices/<index_code>/history`
- **方法**: GET
- **参数**: 
  - `index_code`: 指数代码，如"399006"
- **响应示例**: 看板数据接口中特定指数的历史数据

## 常见问题

### Q: 如何修改数据源？

A: 目前应用使用SQLite数据库存储静态数据。要修改数据源，可以：

1. 直接修改SQLite数据库中的数据
2. 修改`backend/app.py`中的数据获取逻辑，集成外部API（如Tushare）

### Q: 如何自定义前端样式？

A: 前端使用Vue 3和Element Plus组件库。要自定义样式：

1. 修改`frontend/src/components/`中的组件文件
2. 添加全局样式到`frontend/src/App.vue`
3. 修改Element Plus主题配置

### Q: 如何添加新的指数？

A: 要添加新指数：

1. 在SQLite数据库的`indices`表中添加新记录
2. 在`core_data`表中添加对应的核心数据
3. 在`history`表中添加对应的历史数据

### Q: 如何设置定时更新数据？

A: 要实现定时数据更新：

1. 修改后端代码，添加定时任务（如使用APScheduler）
2. 集成外部数据源API（如Tushare）
3. 设置合理的更新频率，避免频繁请求

### Q: 如何部署到生产环境？

A: 生产环境部署建议：

1. 使用Docker Compose进行容器化部署
2. 配置反向代理（如Nginx）
3. 设置SSL证书启用HTTPS
4. 配置数据备份策略
5. 设置监控和日志收集