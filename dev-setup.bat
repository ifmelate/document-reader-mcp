@echo off
REM Development setup script for Windows
REM This script sets up the development environment for document-reader-mcp

echo ========================================
echo document-reader-mcp Development Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    exit /b 1
)

echo [1/4] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
)

echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    exit /b 1
)

echo [3/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo [4/4] Installing package in development mode...
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install package
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To activate the virtual environment in the future:
echo   .venv\Scripts\activate.bat
echo.
echo To run the server:
echo   python -m server.main
echo.


