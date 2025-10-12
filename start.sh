#!/bin/bash

# 金融数据看板启动脚本

echo "金融数据看板启动脚本"
echo "====================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建数据目录
mkdir -p data

# 构建并启动容器
echo "构建并启动容器..."
docker-compose up --build -d

# 检查容器状态
if [ $? -eq 0 ]; then
    echo "应用启动成功!"
    echo "访问地址: http://localhost:5000"
    echo ""
    echo "查看容器状态: docker-compose ps"
    echo "查看日志: docker-compose logs -f"
    echo "停止应用: docker-compose down"
else
    echo "应用启动失败，请检查日志"
    exit 1
fi