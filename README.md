# 金融数据看板

一个基于Vue.js和Flask的金融数据看板应用，提供实时指数数据展示和分析。该应用采用三栏布局设计，展示指数概览、核心数据表和历史信息。

## 功能特点

- **三栏布局展示**：左侧指数概览区、中间核心数据表、右侧历史信息区
- **实时数据更新**：每5分钟自动刷新数据
- **指数可视化**：通过进度条展示当前点位在支撑位与压力位之间的位置
- **可交互链接**：点击指数代码可直接跳转到东方财富网查看详情
- **响应式设计**：适配不同屏幕尺寸
- **Docker容器化部署**：支持一键部署

## 技术栈

- **前端**：Vue.js + Vite + Element Plus
- **后端**：Python + Flask + SQLite
- **容器化**：Docker + Docker Compose

## 快速开始

### 使用Docker部署（推荐）

```bash
# 使用Docker Compose一键启动
docker-compose up --build -d

# 或使用启动脚本
# Windows用户
start.bat

# Linux/Mac用户
chmod +x start.sh
./start.sh
```

访问 `http://localhost:5000` 查看应用。

### 本地开发

#### 后端设置

```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### 前端设置

```bash
cd frontend
npm install
npm run dev
```

### 本地开发快速启动

#### Windows

```bash
# 运行开发启动脚本
dev-start.bat
```

#### Linux/macOS

```bash
# 给脚本添加执行权限
chmod +x dev-start.sh

# 运行开发启动脚本
./dev-start.sh
```

## 项目结构

```
etf-kanban/
├── backend/               # 后端Flask应用
│   ├── app.py            # 主应用文件
│   ├── database.py       # 数据库初始化
│   ├── requirements.txt  # Python依赖
│   └── .env.example      # 环境变量示例
├── frontend/             # 前端Vue应用
│   ├── src/
│   │   ├── components/   # Vue组件
│   │   ├── views/        # 页面视图
│   │   ├── services/     # API服务
│   │   └── router/       # 路由配置
│   ├── package.json      # Node.js依赖
│   └── vite.config.js    # Vite配置
├── docker/               # Docker相关文件
├── docker-compose.yml    # Docker Compose配置
├── Dockerfile            # Docker镜像构建文件
├── start.bat             # Windows启动脚本
├── start.sh              # Linux/Mac启动脚本
├── dev-start.bat         # Windows开发启动脚本
├── dev-start.sh          # Linux/Mac开发启动脚本
└── README.md             # 项目说明文档
```

## API接口

- `GET /api/dashboard` - 获取看板数据
- `GET /api/indices` - 获取所有指数数据
- `GET /api/indices/<index_code>` - 获取特定指数数据
- `GET /api/indices/<index_code>/core_data` - 获取特定指数的核心数据
- `GET /api/indices/<index_code>/history` - 获取特定指数的历史数据
- `GET /api/health` - 健康检查接口

## 数据库设计

应用使用SQLite数据库，包含以下主要表：

- **indices** - 存储指数基本信息和实时点位数据
- **core_data** - 存储策略点位和基金代码等详细信息
- **history** - 存储近三年最高点和最低点信息

## 部署说明

详细的部署指南请参考 [DEPLOYMENT.md](./DEPLOYMENT.md) 文档。

## 许可证

MIT

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。