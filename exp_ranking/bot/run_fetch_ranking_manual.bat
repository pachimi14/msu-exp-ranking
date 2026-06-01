@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title MSU Ranking - Data Fetch

echo ========================================
echo  MSU Ranking - Data Fetch
echo  (API -^> SQLite + rankings.json)
echo ========================================
echo.

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

"%PYTHON%" main.py
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if %EXIT_CODE% equ 0 (
    echo [OK] Data fetch completed.
    echo   DB:     data\ranking.db
    echo   JSON:   ..\web\public\data\rankings.json
    echo.
    echo To open the site, run:
    echo   ..\..\run_exp_ranking_web.bat
) else (
    echo [ERROR] Failed. exit code=%EXIT_CODE%
    echo Check logs\msu_ranking_bot.log for details.
)

echo.
pause
exit /b %EXIT_CODE%
