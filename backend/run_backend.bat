@echo off
echo ===================================
echo PCA Backend Server Startup Script
echo ===================================
echo.

cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        echo Make sure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r Requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install packages from Requirements.txt
    echo Installing packages directly...
    pip install Flask Flask-CORS PyJWT python-dotenv Werkzeug numpy pandas scikit-learn matplotlib Pillow
)

echo.
echo Starting Flask server...
python app.py

pause
