@echo off
echo ========================================
echo   金融智能推荐系统启动脚本
echo ========================================
echo.

echo 1. 启动Django后端服务器...
cd backend
start cmd /k "python manage.py runserver"
cd ..

echo 2. 启动Vue前端开发服务器...
cd frontend
start cmd /k "npm run serve"
cd ..

echo.
echo 系统正在启动中...
echo 后端服务: http://127.0.0.1:8000
echo 前端服务: http://localhost:8080
echo.
echo 请等待两个服务完全启动后访问前端地址。
pause
