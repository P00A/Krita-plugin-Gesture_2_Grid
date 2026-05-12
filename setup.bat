@echo off
REM Setup script for Gesture-to-Grid Krita Plugin
REM This script creates a Python virtual environment with OpenCV pre-installed
REM Run this batch file once after installing the plugin

setlocal enabledelayedexpansion

echo ========================================
echo Gesture-to-Grid Plugin Setup
echo ========================================
echo.

REM Get the directory where this batch file is located
set PLUGIN_DIR=%~dp0
cd /d "%PLUGIN_DIR%"

REM Find a usable Python executable
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed or not available in PATH.
        echo Install Python 3 and retry.
        pause
        exit /b 1
    ) else (
        set "PYTHON_EXE=py -3"
    )
) else (
    set "PYTHON_EXE=python"
)

REM Check if python_env already exists
if exist "python_env" (
    echo python_env folder already exists. Reusing it.
) else (
    echo Creating Python virtual environment...
    %PYTHON_EXE% -m venv python_env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo Make sure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

echo.
echo Installing OpenCV and dependencies...
call python_env\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
call python_env\Scripts\python.exe -m pip install opencv-python numpy
if errorlevel 1 (
    echo ERROR: Failed to install packages.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The plugin is now ready to use in Krita.
echo Restart Krita if it was running, then try the Generate Grid button.
echo.
pause
