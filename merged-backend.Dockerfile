# 合并后的Dockerfile（将阶段2和阶段3合并）
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

# 合并阶段: 后端构建和生产环境
FROM python:3.9-slim

# 安装系统依赖（包括Nginx和健康检查工具）
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 设置工作目录
WORKDIR /app

# 复制后端依赖文件
COPY backend/requirements.txt requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端源代码
COPY backend/ ./

# 确保python3命令可用
RUN ln -sf /usr/bin/python3 /usr/bin/python

# 从前端构建阶段复制构建产物到Nginx静态文件目录
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 设置权限
RUN chown -R appuser:appgroup /app && \
    chown -R appuser:appgroup /usr/share/nginx/html && \
    # 修复Nginx缓存目录权限问题
    mkdir -p /var/cache/nginx /var/lib/nginx /var/log/nginx && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chown -R appuser:appgroup /var/lib/nginx && \
    chown -R appuser:appgroup /var/log/nginx && \
    # 修复Nginx PID文件权限问题
    touch /run/nginx.pid && \
    chown appuser:appgroup /run/nginx.pid

# 切换到非root用户
USER appuser

# 设置工作目录
WORKDIR /app

# 暴露端口 (Nginx默认80端口)
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/api/health || exit 1

# 启动命令 (同时启动Nginx和后端服务)
CMD ["sh", "-c", "python app.py & nginx -g 'daemon off;'"]