@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title MSN EXP Ranking - Web

echo ========================================
echo  MSN EXP Ranking - Web (dev server)
echo ========================================
echo.

where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] npm not found. Install Node.js first.
    pause
    exit /b 1
)

if not exist "node_modules\" (
    echo Installing npm packages...
    call npm install
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] npm install failed.
        pause
        exit /b 1
    )
)

if not exist "public\data\rankings.json" (
    echo [WARN] public\data\rankings.json not found.
    echo Run data fetch first:
    echo   ..\..\run_exp_ranking_fetch.bat
    echo.
)

echo Starting Vite dev server...
echo.
echo   URL: http://localhost:5173/
echo.
echo Keep this window open while using the site.
echo Press Ctrl+C to stop the server.
echo.

start "" "http://localhost:5173/"
call npm run dev
set "EXIT_CODE=%ERRORLEVEL%"

echo.
pause
exit /b %EXIT_CODE%
