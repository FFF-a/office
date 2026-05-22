@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在推送到 GitHub ...
git add -A
git commit -m "deploy: update" 2>nul
git push origin main
if errorlevel 1 (
    echo.
    echo 推送失败：请开 VPN/代理后重新双击本文件
    echo 或用手机热点再试
) else (
    echo.
    echo 推送成功！打开 Actions 查看自动部署：
    start https://github.com/FFF-a/office/actions
)
pause
