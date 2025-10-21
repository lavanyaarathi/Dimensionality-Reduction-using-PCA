@echo off
echo Setting up PCA Project...

echo.
echo Setting up Backend...
cd backend
echo Creating virtual environment...
py -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing Python dependencies...
py -m pip install -r Requirements.txt
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