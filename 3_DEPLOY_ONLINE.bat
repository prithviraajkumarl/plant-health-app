@echo off
setlocal EnableDelayedExpansion
title Plant Health App - 2-Month Online Deployment Assistant

cd /d "%~dp0"

echo ======================================================================
echo    PLANT HEALTH DETECTION APP - ONLINE DEPLOYMENT ASSISTANT
echo ======================================================================
echo This assistant helps you deploy the app online for 2+ months for FREE.
echo.
echo Choose your target hosting platform:
echo   [1] Hugging Face Spaces (RECOMMENDED: 100%% Free 24/7, No Sleep, 16 GB RAM)
echo   [2] GitHub Repository (For Render.com / Railway)
echo   [3] Open Step-by-Step Guide in Browser
echo.
set /p "CHOICE=Enter choice (1, 2, or 3): "

if "%CHOICE%"=="3" (
    start docs\HOSTING_FOR_2_MONTHS.md
    exit /b 0
)

:: Ensure git is available
git --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

:: Initialize git repository if not already done
if not exist ".git" (
    echo.
    echo [1/3] Initializing local Git repository...
    git init
    git branch -M main
)

:: Ensure identity is configured
git config user.name >nul 2>&1
if !errorlevel! neq 0 (
    git config user.name "Plant Health Developer"
    git config user.email "developer@planthealth.local"
)

echo [2/3] Staging project files...
git add .
git commit -m "Deploy Plant Health Detection App with Docker & FastAPI" >nul 2>&1

if "%CHOICE%"=="1" (
    echo.
    echo ----------------------------------------------------------------------
    echo  Hugging Face Spaces Deployment Instructions:
    echo ----------------------------------------------------------------------
    echo  1. Create a free Space at: https://huggingface.co/new-space
    echo     - Name: plant-health-app
    echo     - SDK: Docker (Blank)
    echo     - Hardware: Free (2 vCPU, 16 GB RAM)
    echo  2. Copy your Space git URL (e.g., https://huggingface.co/spaces/USERNAME/plant-health-app)
    echo ----------------------------------------------------------------------
    echo.
    set /p "SPACE_URL=Paste your Hugging Face Space Git URL: "
    if "!SPACE_URL!"=="" (
        echo [ERROR] No URL provided. Aborted.
        pause
        exit /b 1
    )
    
    echo.
    echo [3/3] Pushing to Hugging Face Spaces...
    git remote remove space >nul 2>&1
    git remote add space "!SPACE_URL!"
    git push --force space main:main
    
    echo.
    echo ======================================================================
    echo  Deployment initiated!
    echo  Your app will be building and live on Hugging Face in ~2 minutes.
    echo ======================================================================
)

if "%CHOICE%"=="2" (
    echo.
    set /p "GH_URL=Paste your GitHub Repository URL (e.g., https://github.com/USER/repo.git): "
    if "!GH_URL!"=="" (
        echo [ERROR] No URL provided. Aborted.
        pause
        exit /b 1
    )
    echo.
    echo [3/3] Pushing to GitHub...
    git remote remove origin >nul 2>&1
    git remote add origin "!GH_URL!"
    git push -u origin main --force
    echo.
    echo ======================================================================
    echo  Pushed to GitHub! Now connect this repo on https://render.com
    echo ======================================================================
)

pause
exit /b 0
