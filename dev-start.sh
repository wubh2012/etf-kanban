#!/bin/bash

# 金融数据看板本地开发启动脚本

echo "金融数据看板本地开发启动脚本"
echo "============================"

# 启动后端
echo "启动后端服务..."
cd backend
gnome-terminal -- bash -c "python app.py; exec bash" 2>/dev/null || xterm -e "python app.py" &

# 等待后端启动
sleep 3

# 启动前端
echo "启动前端服务..."
cd ../frontend
gnome-terminal -- bash -c "npm run dev; exec bash" 2>/dev/null || xterm -e "npm run dev" &

echo ""
echo "后端服务: http://localhost:5000"
echo "前端服务: http://localhost:8080"
echo ""
echo "按Ctrl+C停止服务"