@echo off
REM Financial Dashboard Local Development Startup Script (Windows)

echo Financial Dashboard Local Development Startup Script
echo ==================================================

REM Start backend
echo Starting backend service...
cd backend
start "Backend" cmd /k "python app.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend service...
cd ../frontend
start "Frontend" cmd /k "npm run dev"

echo.
echo Backend service: http://localhost:5000
echo Frontend service: http://localhost:8080
echo.
echo Press any key to close this window...
pause >nul