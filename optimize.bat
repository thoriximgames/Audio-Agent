@echo off
setlocal
:: Ensure we are in the script's directory
cd /d "%~dp0"

title Audio Optimization Agent

echo ==========================================
echo    Audio Agent: Optimization Tool
echo ==========================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python to use this tool.
    echo Visit: https://www.python.org/
    pause
    exit /b 1
)

:: Run the optimization script
python optimize_audio.py

echo.
echo ==========================================
echo    Process Complete!
echo ==========================================
echo.
pause
