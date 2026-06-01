@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title MSU EXP Ranking - Web

echo ========================================
echo  MSU EXP Ranking - Web
echo ========================================
echo.

start "MSU EXP Ranking Web" cmd /k "%~dp0exp_ranking\web\run_web_dev_manual.bat"
exit /b 0
