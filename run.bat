@echo off

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -e .
    exit /b 1
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
latex-selector
