@echo off
setlocal EnableDelayedExpansion
title Plant Health Detection App - Local Network Mode

:: Navigate to project directory
cd /d "%~dp0"

echo ======================================================================
echo    PLANT HEALTH DETECTION APP - INITIALIZING LOCAL NETWORK MODE
echo ======================================================================

:: 1. Detect Python
set "PY_EXE="
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_EXE=python"
) else (
    py -0 >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_EXE=py"
    ) else (
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        ) else if exist "%ProgramFiles%\Python312\python.exe" (
            set "PY_EXE=%ProgramFiles%\Python312\python.exe"
        )
    )
)

if "!PY_EXE!"=="" (
    echo [ERROR] Python was not found on your system.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: 2. Check / Create Virtual Environment
if not exist "app\.venv\Scripts\python.exe" (
    echo.
    echo [Setup 1/3] Creating virtual environment in app\.venv...
    "!PY_EXE!" -m venv app\.venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    
    echo [Setup 2/3] Installing requirements from app\requirements.txt...
    app\.venv\Scripts\python.exe -m pip install --upgrade pip
    app\.venv\Scripts\python.exe -m pip install -r app\requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo [Setup 3/3] Dependencies installed successfully.
    echo.
)

:: 3. Run Local Server
app\.venv\Scripts\python.exe app\tools\run_local.py

:: Cleanup on exit
if exist "app\runtime\connection.json" del /Q "app\runtime\connection.json" >nul 2>&1
exit /b 0
