@echo off

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed.
    exit /b 1
) else (
    echo Python is installed.
)

:: Make python virtual environment
echo Creating python virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\Activate

:: Install required packages
echo Installing required python packages
pip install -r requirements.txt

:: Run app
echo Starting SmartSpend
python app.py
