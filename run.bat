@echo off
setlocal
title Family Grocery POS
cd /d "%~dp0"

set PY=python
where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo Python was not found. Install it from https://www.python.org/downloads/windows/
        echo and tick "Add Python to PATH" during installation, then run this file again.
        pause
        exit /b 1
    ) else (
        set PY=py
    )
)

if not exist "venv\Scripts\python.exe" (
    echo First run: creating a private Python environment...
    %PY% -m venv venv
)

call "venv\Scripts\activate.bat"

echo Checking packages (this is fast when everything is already installed)...
python -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo Could not install required packages.
    echo Connect to the internet once and start again.
    pause
    exit /b 1
)

if not exist "database\grocery.db" (
    echo Creating the local database with sample data...
    python init_db.py
)

echo.
echo  Starting the Grocery POS system...
echo  Your browser will open at http://127.0.0.1:5000
echo  Keep this window OPEN while using the system. Close it to stop.
echo.
start "" cmd /c "timeout /t 3 /nobreak >nul & start "" http://127.0.0.1:5000"
python app.py
pause