@echo off
echo Setting up PCA Project for Python 3.13...

echo.
echo Setting up Backend...
cd backend
echo Creating virtual environment...
py -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Upgrading pip, setuptools, and wheel...
py -m pip install --upgrade pip setuptools wheel
echo Installing Python dependencies (Python 3.13 compatible)...
py -m pip install -r requirements_python313.txt
cd ..

echo.
echo Setting up Frontend...
cd frontend
echo Installing Node.js dependencies...
npm install
cd ..

echo.
echo Setup complete!
echo.
echo To start the project, run: start_project.bat
echo.
pause
