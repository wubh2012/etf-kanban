# ETF看板定时任务功能

## 功能概述

ETF看板应用现在支持定时任务功能，可以自动获取指数的当前点位，并更新数据库中的`current_point`和`change_percent`字段。

## 功能特点

1. **自动更新**：定时获取所有指数的实时数据
2. **计算涨跌幅**：根据当前点位和支撑点位自动计算距离大支撑涨跌幅百分比
3. **可配置间隔**：可以通过环境变量配置更新间隔时间
4. **可启用/禁用**：可以通过环境变量启用或禁用定时任务

## 配置说明

在`.env`文件中添加以下配置：

```env
# 定时任务配置
SCHEDULER_ENABLED=true          # 启用定时任务
UPDATE_INTERVAL_MINUTES=10      # 更新间隔（分钟）
```

### 配置参数说明

- `SCHEDULER_ENABLED`: 设置为`true`启用定时任务，设置为`false`禁用
- `UPDATE_INTERVAL_MINUTES`: 设置更新间隔时间，单位为分钟，默认为10分钟

## 使用方法

### 启动应用

```bash
cd backend
python app.py
```

应用启动后，会自动启动定时任务调度器（如果`SCHEDULER_ENABLED=true`），并按照配置的间隔时间自动更新所有指数数据。

### 手动触发更新

应用提供了一个API端点，可以手动触发更新所有指数数据：

```bash
curl -X POST http://localhost:5000/api/update-all-indices
```

或者在PowerShell中：

```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/update-all-indices" -Method POST
```

## 技术实现

1. **APScheduler库**：使用APScheduler库实现定时任务功能
2. **BackgroundScheduler**：使用后台调度器，不影响Flask应用的正常运行
3. **IntervalTrigger**：使用间隔触发器，按照指定时间间隔执行任务
4. **自动计算涨跌幅**：根据公式`((当前点位 - 支撑点位) / 支撑点位) * 100`计算涨跌幅百分比

## 日志记录

定时任务的执行情况会记录在应用日志中，包括：

- 任务开始执行的时间
- 每个指数数据更新的结果
- 成功更新的指数数量
- 任务完成的时间

## 注意事项

1. 确保网络连接正常，以便能够获取实时数据
2. 如果某个指数的数据获取失败，不会影响其他指数的更新
3. 定时任务会在应用启动时自动启动，在应用关闭时自动停止
4. 建议根据实际需求调整更新间隔时间，避免过于频繁的请求导致API限制

## 故障排除

如果定时任务没有正常工作，请检查：

1. `.env`文件中的配置是否正确
2. 应用日志中是否有错误信息
3. 网络连接是否正常
4. 是否可以手动触发更新任务

## 测试

项目提供了一个测试脚本`test_scheduler.py`，可以用来测试定时任务功能：

```bash
python test_scheduler.py
```

这个脚本会执行一次更新所有指数数据的操作，并显示更新前后的数据对比。