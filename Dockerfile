# 多阶段构建Dockerfile

# 阶段1: 构建前端
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# 复制前端package文件
COPY frontend/package*.json ./

# 安装前端依赖
RUN npm ci

# 复制前端源代码
COPY frontend/ ./

# 构建前端
RUN npm run build

# 阶段2: 构建后端
FROM python:3.9-slim AS backend

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt ./

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端源代码
COPY backend/ ./

# 从前端构建阶段复制构建产物
COPY --from=frontend-build /app/frontend/dist ./static

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动命令
CMD ["python", "app.py"]