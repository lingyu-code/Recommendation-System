@echo off
echo 启动金融智能推荐系统...

echo 1. 启动后端Django服务器...
start cmd /k "cd /d D:\Users\Lean2023\Desktop\E-commerce_finance\CRM\backend && python manage.py runserver"

timeout /t 5 /nobreak >nul

echo 2. 启动前端Vue开发服务器...
start cmd /k "cd /d D:\Users\Lean2023\Desktop\E-commerce_finance\CRM\frontend && npm run dev"

echo.
echo 系统启动完成！
echo 后端服务器: http://127.0.0.1:8000
echo 前端应用: 请查看前端终端输出的地址
echo.
echo 按任意键退出此窗口...
pause >nul
