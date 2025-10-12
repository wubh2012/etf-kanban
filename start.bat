@echo off
REM 金融数据看板启动脚本 (Windows)

echo 金融数据看板启动脚本
echo =====================

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker未安装，请先安装Docker
    pause
    exit /b 1
)

REM 检查Docker Compose是否安装
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker Compose未安装，请先安装Docker Compose
    pause
    exit /b 1
)

REM 创建数据目录
if not exist "data" mkdir data

REM 构建并启动容器
echo 构建并启动容器...
docker-compose up --build -d

REM 检查容器状态
if %errorlevel% equ 0 (
    echo 应用启动成功!
    echo 访问地址: http://localhost:5000
    echo.
    echo 查看容器状态: docker-compose ps
    echo 查看日志: docker-compose logs -f
    echo 停止应用: docker-compose down
) else (
    echo 应用启动失败，请检查日志
    pause
    exit /b 1
)

pause