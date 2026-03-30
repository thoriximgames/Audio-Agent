@echo off
setlocal
:: Ensure we are in the script's directory
cd /d "%~dp0"

title Audio Project Health Check

echo ==========================================
echo    Audio Agent: Project Analyzer
echo ==========================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python to use this tool.
    pause
    exit /b 1
)

:: Run the analyzer script
python project_analyzer.py

echo.
echo ==========================================
echo    Analysis Complete!
echo ==========================================
echo.
pause
