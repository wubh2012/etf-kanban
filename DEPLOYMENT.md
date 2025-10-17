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

目标：在一台 Linux 服务器上，后端使用 Gunicorn 运行 Flask 应用，前端由 Nginx 托管静态资源并反向代理后端 API。

**总体架构**
- 前端：Vite 构建生成 `frontend/dist`，Nginx 直接托管静态文件。
- 后端：Gunicorn 在本机回环地址 `127.0.0.1:8100` 监听，Nginx 将 `/api` 代理到此地址。
- 数据库：SQLite 文件位于 `backend/etf_kanban.db`。
- 定时更新：用系统定时器（cron 或 systemd timer）调用接口 `/api/update-all-indices`。

**环境准备**
- 安装基础组件（Ubuntu 示例）：
  - `sudo apt update && sudo apt install -y python3 python3-venv python3-pip nginx curl`
- 安装 Node.js（18/20 LTS）：
  - `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs`
- 代码目录（示例）：
  - `sudo mkdir -p /opt/etf-kanban && sudo chown -R $USER:$USER /opt/etf-kanban`
  - 将项目上传或 `git clone` 到 `/opt/etf-kanban`

**后端部署（Gunicorn）**
- 创建虚拟环境并安装依赖：
  - `cd /opt/etf-kanban`
  - `python3 -m venv venv && source venv/bin/activate`
  - `pip install -r backend/requirements.txt`
  - `pip install gunicorn`
- 生产环境变量（两选一）：
  - 使用 `backend/.env.production`（推荐）：`FLASK_ENV=production`、`SCHEDULER_ENABLED=false` 等；或
  - 直接用 `backend/.env` 存放生产值。
- 初始化数据库（首次部署）：
  - `python backend/app.py` 启动后看到“数据库文件不存在，开始初始化数据库…”，再 `Ctrl+C` 退出。
- 测试运行：
  - `gunicorn --bind 127.0.0.1:8100 backend.app:app`
  - 验证健康：`curl http://127.0.0.1:8100/api/health`

**作为服务运行（systemd）**
- 创建 `/etc/systemd/system/etf-kanban-backend.service`：
```
[Unit]
Description=ETF Kanban Backend (Gunicorn)
After=network.target

[Service]
WorkingDirectory=/opt/etf-kanban
EnvironmentFile=/opt/etf-kanban/backend/.env.production
ExecStart=/opt/etf-kanban/venv/bin/gunicorn --bind 127.0.0.1:8100 --workers 2 backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
- 启动与验证：
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable --now etf-kanban-backend`
  - `journalctl -u etf-kanban-backend -f`
  - `curl http://127.0.0.1:8100/api/health`
- 权限注意：确保服务用户对 `backend/etf_kanban.db` 有写权限：
  - `sudo chown -R www-data:www-data /opt/etf-kanban/backend`
  - SQLite 并发有限，`--workers` 建议 1–2。

**前端部署（Nginx）**
- 构建前端：
  - `cd /opt/etf-kanban/frontend`
  - `npm ci` 或 `npm install`
  - `npm run build`（生成 `dist`）
- 发布静态文件：
  - `sudo mkdir -p /var/www/etf-kanban`
  - `sudo cp -r dist/* /var/www/etf-kanban/`
- Nginx 站点 `/etc/nginx/sites-available/etf-kanban`：
```
server {
    listen 80;
    server_name your.domain.com;  # 替换为域名或服务器IP

    root /var/www/etf-kanban;
    index index.html;

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 反向代理后端 API
    location /api {
        proxy_pass http://127.0.0.1:8100;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- 启用并重载：
  - `sudo ln -s /etc/nginx/sites-available/etf-kanban /etc/nginx/sites-enabled/`
  - `sudo nginx -t && sudo systemctl reload nginx`
- 前端 `.env.production` 已设置 `VITE_API_BASE_URL=/api`，构建后请求将走 Nginx 的 `/api` 代理。

**定时更新（推荐外部定时器）**
- cron（每 15 分钟）：
  - `crontab -e` 添加：
    - `*/15 * * * * curl -s -X POST http://127.0.0.1:8100/api/update-all-indices >/dev/null 2>&1`
- 或 systemd 定时器：
  - `/etc/systemd/system/etf-kanban-update.service`：
```
[Unit]
Description=ETF Kanban manual update trigger

[Service]
Type=oneshot
ExecStart=/usr/bin/curl -s -X POST http://127.0.0.1:8000/api/update-all-indices
```
  - `/etc/systemd/system/etf-kanban-update.timer`：
```
[Unit]
Description=Run ETF Kanban update every 15 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
```
  - 启用：`sudo systemctl daemon-reload && sudo systemctl enable --now etf-kanban-update.timer`

**注意事项**
- Gunicorn 监听地址与端口由 `--bind` 控制，不依赖 `.env` 中的 `API_HOST/PORT`。
- SQLite 写锁：高并发写入可能出现 `database is locked`，控制并发和任务频率。
- 权限：确保服务用户可写 `backend/etf_kanban.db` 与日志目录。
- HTTPS：使用 Let’s Encrypt：`sudo apt install certbot python3-certbot-nginx && sudo certbot --nginx -d your.domain.com`。
- 前端环境：生产用 `frontend/.env.production` 设置 `VITE_API_BASE_URL=/api`；若不走反代，改为完整后端地址。

**故障排查**
- `ModuleNotFoundError: No module named backend`：在项目根运行 Gunicorn，或用 `--chdir backend app:app`。
- `.env` 未生效：systemd 使用 `EnvironmentFile` 指定；或直接将生产配置命名为 `backend/.env`。
- 端口占用：`sudo lsof -i :8100` 查占用并处理。
- Nginx 无法访问后端：检查反代地址与防火墙、SELinux 状态。


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