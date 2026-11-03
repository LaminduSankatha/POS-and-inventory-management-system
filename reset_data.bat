@echo off
title Reset Tool - Disodi Stores POS
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo.
    echo The project's Python environment was not found.
    echo Start run.bat once first so it can be created, then try again.
    echo.
    pause
    exit /b 1
)

"venv\Scripts\python.exe" "%~dp0reset_data.py"

echo.
pause