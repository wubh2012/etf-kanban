# 多阶段构建Dockerfile

# 阶段1: 构建前端
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# 复制前端package文件并安装依赖
COPY frontend/package*.json ./
RUN npm ci

# 复制前端源代码并构建
COPY frontend/ ./
RUN npm run build && \
    # 构建完成后删除node_modules节省空间
    rm -rf node_modules

# 阶段2: 构建后端
FROM python:3.9-slim AS backend

WORKDIR /app

# 复制后端依赖文件
COPY backend/requirements.txt requirements.txt

# 安装系统依赖和Python依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# 复制后端源代码
COPY backend/ ./

# 确保python3命令可用
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    # 安装Python运行时依赖
    apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 阶段3: Nginx服务器
FROM nginx:alpine AS production

# 安装curl用于健康检查和Python环境
RUN apk add --no-cache curl python3 py3-pip

# 从前端构建阶段复制构建产物到Nginx静态文件目录
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从后端构建阶段复制应用文件
COPY --from=backend /app /app

# 安装Python依赖
RUN pip3 install --break-system-packages --no-cache-dir -r /app/requirements.txt

# 创建非root用户并设置权限
RUN addgroup -g 1001 -S app &&\
    adduser -u 1001 -S app -G app &&\
    chown -R app:app /app &&\
    chown -R app:app /usr/share/nginx/html &&\
    # 修复Nginx缓存目录权限问题
    mkdir -p /var/cache/nginx &&\
    chown -R app:app /var/cache/nginx &&\
    # 修复Nginx PID文件权限问题
    touch /run/nginx.pid &&\
    chown app:app /run/nginx.pid

# 切换到非root用户
USER app

# 设置工作目录
WORKDIR /app

# 暴露端口 (Nginx默认80端口)
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/api/health || exit 1

# 启动命令 (同时启动Nginx和后端服务)
CMD ["sh", "-c", "python3 app.py & nginx -g 'daemon off;'"]