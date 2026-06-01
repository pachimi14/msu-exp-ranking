@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call "%~dp0exp_ranking\bot\run_inject_dummy_gains.bat"
exit /b %ERRORLEVEL%
